/*
 * Concurrent Image Processing Pipeline
 * Operating Systems Course Project
 *
 * Single-file implementation demonstrating:
 * fork(), waitpid(), POSIX shared memory, POSIX semaphores,
 * producer-consumer synchronization, and multi-process coordination.
 */

#include <opencv2/opencv.hpp>

#include <cerrno>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <semaphore.h>
#include <unistd.h>

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

static const int CHUNK_ROWS = 16;
static const int NUM_SLOTS = 8;
static const int MAX_WORKERS = 8;
static const int CHANNELS = 3;

static const char* SHM_NAME = "/img_pipeline_shm";
static const char* SEM_EMPTY_NAME = "/img_pipeline_empty";
static const char* SEM_WORK_NAME = "/img_pipeline_work";
static const char* SEM_DONE_NAME = "/img_pipeline_done";

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

enum SlotState {
    SLOT_FREE = 0,
    SLOT_READY = 1,
    SLOT_DONE = 2
};

enum ProcessRole {
    ROLE_SUPERVISOR = 0,
    ROLE_PRODUCER = 1,
    ROLE_WORKER = 2,
    ROLE_COLLECTOR = 3
};

enum FilterType {
    FILTER_GRAYSCALE = 0,
    FILTER_INVERT = 1
};

// ---------------------------------------------------------------------------
// Shared structures (stored in POSIX shared memory)
// ---------------------------------------------------------------------------

struct SharedHeader {
    int width;
    int height;
    int channels;
    int chunk_rows;
    int total_chunks;
    int num_slots;
    int num_workers;
    int producer_finished;
    int chunks_done;          // collector increments when a chunk is saved
    int filter_type;          // FilterType, shared so all workers use the same filter
    int worker_stats[MAX_WORKERS];
};

// Slot header lives in shared memory; pixel bytes follow immediately after.
struct ChunkSlotHeader {
    volatile int state;
    int chunk_id;
    int start_row;
    int row_count;
};

// ---------------------------------------------------------------------------
// Globals used after mmap (each process maps the same region)
// ---------------------------------------------------------------------------

static SharedHeader* g_header = nullptr;
static unsigned char* g_slots_base = nullptr;
static size_t g_slot_stride = 0;
static size_t g_payload_bytes = 0;

static sem_t* g_sem_empty = nullptr;
static sem_t* g_sem_work = nullptr;
static sem_t* g_sem_done = nullptr;

// ---------------------------------------------------------------------------
// Helper: slot access
// ---------------------------------------------------------------------------

static ChunkSlotHeader* slot_at(int index) {
    return reinterpret_cast<ChunkSlotHeader*>(g_slots_base + index * g_slot_stride);
}

static unsigned char* slot_data(ChunkSlotHeader* slot) {
    return reinterpret_cast<unsigned char*>(slot) + sizeof(ChunkSlotHeader);
}

static size_t compute_shm_size(int width) {
    g_payload_bytes = static_cast<size_t>(CHUNK_ROWS) * width * CHANNELS;
    g_slot_stride = sizeof(ChunkSlotHeader) + g_payload_bytes;
    return sizeof(SharedHeader) + g_slot_stride * NUM_SLOTS;
}

// ---------------------------------------------------------------------------
// Helper: cleanup IPC objects (supervisor only should unlink)
// ---------------------------------------------------------------------------

static void cleanup_ipc(bool unlink_objects) {
    if (g_sem_empty) {
        sem_close(g_sem_empty);
        g_sem_empty = nullptr;
    }
    if (g_sem_work) {
        sem_close(g_sem_work);
        g_sem_work = nullptr;
    }
    if (g_sem_done) {
        sem_close(g_sem_done);
        g_sem_done = nullptr;
    }

    if (unlink_objects) {
        sem_unlink(SEM_EMPTY_NAME);
        sem_unlink(SEM_WORK_NAME);
        sem_unlink(SEM_DONE_NAME);
        shm_unlink(SHM_NAME);
    }
}

static void die(const char* msg) {
    perror(msg);
    cleanup_ipc(false);
    std::exit(1);
}

// ---------------------------------------------------------------------------
// Helper: find slot by state (linear scan over fixed slot count)
// ---------------------------------------------------------------------------

static int find_slot_with_state(int wanted_state) {
    for (int i = 0; i < NUM_SLOTS; ++i) {
        ChunkSlotHeader* slot = slot_at(i);
        if (slot->state == wanted_state) {
            return i;
        }
    }
    return -1;
}

static bool any_slot_with_state(int wanted_state) {
    return find_slot_with_state(wanted_state) >= 0;
}

// ---------------------------------------------------------------------------
// Image filters (applied in-place by workers)
// ---------------------------------------------------------------------------

static void apply_grayscale(unsigned char* data, int row_count, int width) {
    int pixels = row_count * width;
    for (int i = 0; i < pixels; ++i) {
        unsigned char* px = data + i * CHANNELS;
        int b = px[0];
        int g = px[1];
        int r = px[2];
        unsigned char gray = static_cast<unsigned char>((b + g + r) / 3);
        px[0] = gray;
        px[1] = gray;
        px[2] = gray;
    }
}

static void apply_invert(unsigned char* data, int row_count, int width) {
    int pixels = row_count * width;
    for (int i = 0; i < pixels; ++i) {
        unsigned char* px = data + i * CHANNELS;
        px[0] = static_cast<unsigned char>(255 - px[0]);
        px[1] = static_cast<unsigned char>(255 - px[1]);
        px[2] = static_cast<unsigned char>(255 - px[2]);
    }
}

static void apply_filter(FilterType filter, unsigned char* data, int row_count, int width) {
    switch (filter) {
        case FILTER_GRAYSCALE:
            apply_grayscale(data, row_count, width);
            break;
        case FILTER_INVERT:
            apply_invert(data, row_count, width);
            break;
    }
}

static const char* filter_to_string(FilterType filter) {
    switch (filter) {
        case FILTER_GRAYSCALE:
            return "grayscale";
        case FILTER_INVERT:
            return "invert";
        default:
            return "unknown";
    }
}

static bool parse_filter_name(const char* name, FilterType* out) {
    if (std::strcmp(name, "grayscale") == 0 || std::strcmp(name, "gray") == 0) {
        *out = FILTER_GRAYSCALE;
        return true;
    }
    if (std::strcmp(name, "invert") == 0) {
        *out = FILTER_INVERT;
        return true;
    }
    return false;
}

static bool is_positive_int_string(const char* s) {
    if (s == nullptr || *s == '\0') {
        return false;
    }
    for (const char* p = s; *p != '\0'; ++p) {
        if (*p < '0' || *p > '9') {
            return false;
        }
    }
    return true;
}

// ---------------------------------------------------------------------------
// Count how many chunks a worker is responsible for
// ---------------------------------------------------------------------------

static int chunks_for_worker(int worker_id, int num_workers, int total_chunks) {
    int count = 0;
    for (int c = 0; c < total_chunks; ++c) {
        if (c % num_workers == worker_id) {
            ++count;
        }
    }
    return count;
}

// ---------------------------------------------------------------------------
// Producer process
// ---------------------------------------------------------------------------

static void run_producer(const char* input_path) {
    cv::Mat image = cv::imread(input_path, cv::IMREAD_COLOR);
    if (image.empty()) {
        std::cerr << "[Producer] Failed to read image: " << input_path << std::endl;
        std::exit(1);
    }

    if (image.cols != g_header->width || image.rows != g_header->height) {
        std::cerr << "[Producer] Image size mismatch with shared header." << std::endl;
        std::exit(1);
    }

    int width = g_header->width;
    int total_chunks = g_header->total_chunks;

    for (int chunk_id = 0; chunk_id < total_chunks; ++chunk_id) {
        if (sem_wait(g_sem_empty) != 0) {
            die("sem_wait(sem_empty) in producer");
        }

        int slot_index = -1;
        for (int attempt = 0; attempt < 1000; ++attempt) {
            slot_index = find_slot_with_state(SLOT_FREE);
            if (slot_index >= 0) {
                break;
            }
            usleep(1000);
        }

        if (slot_index < 0) {
            sem_post(g_sem_empty);
            std::cerr << "[Producer] No FREE slot found." << std::endl;
            std::exit(1);
        }

        ChunkSlotHeader* slot = slot_at(slot_index);
        int start_row = chunk_id * g_header->chunk_rows;
        int row_count = g_header->chunk_rows;
        if (start_row + row_count > g_header->height) {
            row_count = g_header->height - start_row;
        }

        slot->chunk_id = chunk_id;
        slot->start_row = start_row;
        slot->row_count = row_count;

        unsigned char* dest = slot_data(slot);
        for (int r = 0; r < row_count; ++r) {
            const unsigned char* src_row = image.ptr<unsigned char>(start_row + r);
            std::memcpy(dest + static_cast<size_t>(r) * width * CHANNELS,
                        src_row,
                        static_cast<size_t>(width) * CHANNELS);
        }

        slot->state = SLOT_READY;

        if (sem_post(g_sem_work) != 0) {
            die("sem_post(sem_work) in producer");
        }
    }

    g_header->producer_finished = 1;
    std::cout << "[Producer] Finished sending " << total_chunks << " chunks." << std::endl;
    std::exit(0);
}

// ---------------------------------------------------------------------------
// Worker process
// ---------------------------------------------------------------------------

static void run_worker(int worker_id) {
    int num_workers = g_header->num_workers;
    int total_chunks = g_header->total_chunks;
    int target = chunks_for_worker(worker_id, num_workers, total_chunks);
    int processed = 0;

    while (processed < target) {
        if (sem_wait(g_sem_work) != 0) {
            die("sem_wait(sem_work) in worker");
        }

        int slot_index = find_slot_with_state(SLOT_READY);

        if (slot_index < 0) {
            sem_post(g_sem_work);
            if (g_header->producer_finished && !any_slot_with_state(SLOT_READY)) {
                usleep(2000);
            }
            continue;
        }

        ChunkSlotHeader* slot = slot_at(slot_index);

        if (slot->chunk_id % num_workers != worker_id) {
            sem_post(g_sem_work);
            usleep(1000);
            continue;
        }

        FilterType filter = static_cast<FilterType>(g_header->filter_type);
        apply_filter(filter, slot_data(slot), slot->row_count, g_header->width);

        slot->state = SLOT_DONE;
        g_header->worker_stats[worker_id]++;
        ++processed;

        if (sem_post(g_sem_done) != 0) {
            die("sem_post(sem_done) in worker");
        }
    }

    std::cout << "[Worker " << worker_id << "] Processed " << processed << " chunks." << std::endl;
    std::exit(0);
}

// ---------------------------------------------------------------------------
// Collector process
// ---------------------------------------------------------------------------

static void run_collector(const char* output_path) {
    cv::Mat output(g_header->height, g_header->width, CV_8UC3);
    output.setTo(cv::Scalar(0, 0, 0));

    int width = g_header->width;
    int total_chunks = g_header->total_chunks;
    int collected = 0;

    while (collected < total_chunks) {
        if (sem_wait(g_sem_done) != 0) {
            die("sem_wait(sem_done) in collector");
        }

        int slot_index = find_slot_with_state(SLOT_DONE);
        if (slot_index < 0) {
            sem_post(g_sem_done);
            usleep(1000);
            continue;
        }

        ChunkSlotHeader* slot = slot_at(slot_index);
        unsigned char* src = slot_data(slot);
        int start_row = slot->start_row;
        int row_count = slot->row_count;

        for (int r = 0; r < row_count; ++r) {
            unsigned char* dst_row = output.ptr<unsigned char>(start_row + r);
            std::memcpy(dst_row,
                        src + static_cast<size_t>(r) * width * CHANNELS,
                        static_cast<size_t>(width) * CHANNELS);
        }

        slot->state = SLOT_FREE;
        g_header->chunks_done++;
        ++collected;

        if (sem_post(g_sem_empty) != 0) {
            die("sem_post(sem_empty) in collector");
        }
    }

    if (!cv::imwrite(output_path, output)) {
        std::cerr << "[Collector] Failed to write output: " << output_path << std::endl;
        std::exit(1);
    }

    std::cout << "[Collector] Saved image to " << output_path << std::endl;
    std::exit(0);
}

// ---------------------------------------------------------------------------
// Map shared memory and open semaphores (all processes)
// ---------------------------------------------------------------------------

static void attach_ipc() {
    int fd = shm_open(SHM_NAME, O_RDWR, 0666);
    if (fd < 0) {
        die("shm_open (attach)");
    }

    struct stat st;
    if (fstat(fd, &st) != 0) {
        die("fstat");
    }

    void* addr = mmap(nullptr, st.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    close(fd);

    if (addr == MAP_FAILED) {
        die("mmap");
    }

    g_header = static_cast<SharedHeader*>(addr);
    g_slots_base = reinterpret_cast<unsigned char*>(g_header + 1);
    compute_shm_size(g_header->width);

    g_sem_empty = sem_open(SEM_EMPTY_NAME, 0);
    g_sem_work = sem_open(SEM_WORK_NAME, 0);
    g_sem_done = sem_open(SEM_DONE_NAME, 0);

    if (g_sem_empty == SEM_FAILED || g_sem_work == SEM_FAILED || g_sem_done == SEM_FAILED) {
        die("sem_open (attach)");
    }
}

// ---------------------------------------------------------------------------
// Supervisor: create IPC, fork children, wait, print summary
// ---------------------------------------------------------------------------

static int run_supervisor(const char* input_path,
                          const char* output_path,
                          int num_workers,
                          FilterType filter) {
    cv::Mat probe = cv::imread(input_path, cv::IMREAD_COLOR);
    if (probe.empty()) {
        std::cerr << "Error: cannot read input image: " << input_path << std::endl;
        return 1;
    }

    int width = probe.cols;
    int height = probe.rows;
    probe.release();

    int total_chunks = (height + CHUNK_ROWS - 1) / CHUNK_ROWS;
    size_t shm_size = compute_shm_size(width);

    // Remove stale IPC from a previous crashed run
    shm_unlink(SHM_NAME);
    sem_unlink(SEM_EMPTY_NAME);
    sem_unlink(SEM_WORK_NAME);
    sem_unlink(SEM_DONE_NAME);

    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (fd < 0) {
        die("shm_open (create)");
    }

    if (ftruncate(fd, static_cast<off_t>(shm_size)) != 0) {
        die("ftruncate");
    }

    void* addr = mmap(nullptr, shm_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    close(fd);

    if (addr == MAP_FAILED) {
        die("mmap (supervisor)");
    }

    std::memset(addr, 0, shm_size);
    g_header = static_cast<SharedHeader*>(addr);
    g_slots_base = reinterpret_cast<unsigned char*>(g_header + 1);

    g_header->width = width;
    g_header->height = height;
    g_header->channels = CHANNELS;
    g_header->chunk_rows = CHUNK_ROWS;
    g_header->total_chunks = total_chunks;
    g_header->num_slots = NUM_SLOTS;
    g_header->num_workers = num_workers;
    g_header->producer_finished = 0;
    g_header->chunks_done = 0;
    g_header->filter_type = static_cast<int>(filter);

    for (int i = 0; i < MAX_WORKERS; ++i) {
        g_header->worker_stats[i] = 0;
    }

    for (int i = 0; i < NUM_SLOTS; ++i) {
        slot_at(i)->state = SLOT_FREE;
    }

    g_sem_empty = sem_open(SEM_EMPTY_NAME, O_CREAT | O_EXCL, 0666, NUM_SLOTS);
    g_sem_work = sem_open(SEM_WORK_NAME, O_CREAT | O_EXCL, 0666, 0);
    g_sem_done = sem_open(SEM_DONE_NAME, O_CREAT | O_EXCL, 0666, 0);

    if (g_sem_empty == SEM_FAILED || g_sem_work == SEM_FAILED || g_sem_done == SEM_FAILED) {
        die("sem_open (create)");
    }

    auto t0 = std::chrono::steady_clock::now();

    // Flush before fork(): otherwise buffered stdout is duplicated in each child.
    std::cout.flush();
    std::cerr.flush();
    fflush(stdout);
    fflush(stderr);

    pid_t producer_pid = fork();
    if (producer_pid < 0) {
        die("fork producer");
    }
    if (producer_pid == 0) {
        attach_ipc();
        run_producer(input_path);
    }

    std::vector<pid_t> worker_pids(static_cast<size_t>(num_workers));
    for (int w = 0; w < num_workers; ++w) {
        pid_t wp = fork();
        if (wp < 0) {
            die("fork worker");
        }
        if (wp == 0) {
            attach_ipc();
            run_worker(w);
        }
        worker_pids[static_cast<size_t>(w)] = wp;
    }

    pid_t collector_pid = fork();
    if (collector_pid < 0) {
        die("fork collector");
    }
    if (collector_pid == 0) {
        attach_ipc();
        run_collector(output_path);
    }

    int status = 0;
    waitpid(producer_pid, &status, 0);
    for (pid_t wp : worker_pids) {
        waitpid(wp, &status, 0);
    }
    waitpid(collector_pid, &status, 0);

    auto t1 = std::chrono::steady_clock::now();
    double elapsed_sec = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "\n========== Pipeline Summary ==========\n";
    std::cout << "Image size      : " << width << " x " << height << " (BGR)\n";
    std::cout << "Chunk rows      : " << CHUNK_ROWS << "\n";
    std::cout << "Total chunks    : " << total_chunks << "\n";
    std::cout << "Buffer slots    : " << NUM_SLOTS << "\n";
    std::cout << "Filter          : " << filter_to_string(filter) << "\n";
    std::cout << "Workers         : " << num_workers << "\n";
    for (int w = 0; w < num_workers; ++w) {
        std::cout << "  Worker " << w << " chunks : " << g_header->worker_stats[w] << "\n";
    }
    std::cout << "Chunks collected: " << g_header->chunks_done << "\n";
    std::cout << "Elapsed time    : " << elapsed_sec << " s\n";
    std::cout << "Output saved to : " << output_path << "\n";
    std::cout << "======================================\n";

    munmap(addr, shm_size);
    cleanup_ipc(true);
    return 0;
}

// ---------------------------------------------------------------------------
// main: parse CLI and start supervisor
// ---------------------------------------------------------------------------

static void print_usage(const char* prog) {
    std::cerr << "Usage: " << prog << " <input_image> <output_image> [num_workers] [filter]\n"
              << "  num_workers: optional, default 2, range 1-8\n"
              << "  filter: optional, grayscale (default) or invert\n"
              << "\nExamples:\n"
              << "  " << prog << " in.png out.png\n"
              << "  " << prog << " in.png out.png 4\n"
              << "  " << prog << " in.png out.png invert\n"
              << "  " << prog << " in.png out.png 4 invert\n";
}

int main(int argc, char* argv[]) {
    if (argc < 3 || argc > 5) {
        print_usage(argv[0]);
        return 1;
    }

    const char* input_path = argv[1];
    const char* output_path = argv[2];
    int num_workers = 2;
    FilterType filter = FILTER_GRAYSCALE;

    if (argc >= 4) {
        if (is_positive_int_string(argv[3])) {
            num_workers = std::atoi(argv[3]);
            if (argc == 5) {
                if (!parse_filter_name(argv[4], &filter)) {
                    std::cerr << "Error: unknown filter '" << argv[4]
                              << "'. Use grayscale or invert.\n";
                    return 1;
                }
            }
        } else {
            if (!parse_filter_name(argv[3], &filter)) {
                std::cerr << "Error: expected num_workers or filter name, got '"
                          << argv[3] << "'\n";
                print_usage(argv[0]);
                return 1;
            }
        }
    }

    if (num_workers < 1 || num_workers > MAX_WORKERS) {
        std::cerr << "Error: num_workers must be between 1 and " << MAX_WORKERS << "\n";
        return 1;
    }

    std::cout << "Concurrent Image Processing Pipeline\n";
    std::cout << "Input : " << input_path << "\n";
    std::cout << "Output: " << output_path << "\n";
    std::cout << "Workers: " << num_workers << "\n";
    std::cout << "Filter: " << filter_to_string(filter) << "\n\n";

    return run_supervisor(input_path, output_path, num_workers, filter);
}

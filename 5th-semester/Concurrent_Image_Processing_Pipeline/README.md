# Concurrent Image Processing Pipeline

**Course:** Operating Systems  
**Language:** C++17  
**Platform:** Ubuntu Linux  

## Project Objective

Build a **multi-process image processing pipeline** that reads a color image, splits it into row chunks, processes chunks in parallel using several worker processes, and writes a grayscale output image.

The goal is to demonstrate real **operating system concepts**: process creation, inter-process communication (IPC), shared memory, semaphores, and producer–consumer synchronization.

## OS Concepts Used

| Concept | API / Mechanism |
|--------|------------------|
| Process creation | `fork()` |
| Process waiting | `waitpid()` |
| Shared memory | `shm_open()`, `ftruncate()`, `mmap()`, `munmap()`, `shm_unlink()` |
| Semaphores | `sem_open()`, `sem_wait()`, `sem_post()`, `sem_close()`, `sem_unlink()` |
| IPC pattern | Producer–consumer with bounded buffer (8 slots) |
| Parallelism | Multiple worker child processes |

## Process Roles

```
                    +------------------+
                    |    Supervisor    |
                    |  (parent/main)   |
                    +--------+---------+
                             |
         +-------------------+-------------------+
         |                   |                   |
   +-----v-----+      +------v------+     +------v------+
   | Producer  |      |  Worker 0   |     |  Collector  |
   | (1 child) |      |  Worker 1   |     |  (1 child)  |
   |           |      |  ...        |     |             |
   +-----------+      +-------------+     +-------------+
```

1. **Supervisor (parent)** – Creates shared memory and semaphores, forks all children, waits with `waitpid()`, prints summary, cleans up IPC.
2. **Producer** – Loads the input image with OpenCV, splits rows into chunks, fills free slots in shared memory, signals workers.
3. **Workers (N children)** – Each worker handles chunks where `chunk_id % num_workers == worker_id`, applies the selected filter (`grayscale` or `invert`), marks slots done.
4. **Collector** – Reassembles processed chunks into one output image and saves it.

## Shared Memory Layout

One POSIX shared memory object holds:

### `SharedHeader`

- Image metadata: `width`, `height`, `channels`
- Pipeline config: `chunk_rows` (16), `total_chunks`, `num_slots` (8), `num_workers`
- Status: `producer_finished`, `chunks_done`, `worker_stats[8]`

### Chunk slots (8 fixed slots)

Each slot has:

- `state`: `FREE`, `READY`, or `DONE`
- `chunk_id`, `start_row`, `row_count`
- `data[]`: up to `chunk_rows × width × 3` bytes (BGR)

Slots form a **bounded buffer** between producer, workers, and collector.

## Semaphore Explanation

Three **named POSIX semaphores** coordinate the pipeline:

| Semaphore | Initial value | Meaning |
|-----------|---------------|---------|
| `sem_empty` | 8 (`num_slots`) | Number of free buffer slots |
| `sem_work` | 0 | Chunks ready for workers |
| `sem_done` | 0 | Chunks finished and ready for collector |

**Typical flow:**

1. Producer: `sem_wait(sem_empty)` → fill slot → `sem_post(sem_work)`
2. Worker: `sem_wait(sem_work)` → process → `sem_post(sem_done)`
3. Collector: `sem_wait(sem_done)` → copy to output → `sem_post(sem_empty)`

This avoids deadlock by always acquiring resources in a consistent order.

## Image Filters

Workers read `filter_type` from shared memory and apply one filter in-place on each chunk.

### Grayscale (default)

```
gray = (B + G + R) / 3
B = G = R = gray
```

### Invert

```
B = 255 - B
G = 255 - G
R = 255 - R
```

## Project Structure

```text
OS_Project_Simple/
├── CMakeLists.txt
├── README.md
├── main.cpp
└── assets/
    ├── input/      ← place test images here
    └── output/     ← processed images written here
```

## Dependencies (Ubuntu)

```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config libopencv-dev
```

## Build Instructions

```bash
cd OS_Project_Simple
cmake -S . -B build
cmake --build build
```

Executable: `build/image_pipeline`

## Run Instructions

```bash
./build/image_pipeline <input_image> <output_image> [num_workers] [filter]
```

- `num_workers` is optional (default: **2**, range **1–8**)
- `filter` is optional: **grayscale** (default) or **invert**

### Example Commands

```bash
# Copy a test image into assets/input first
cp ~/Pictures/photo.png assets/input/photo.png

./build/image_pipeline assets/input/photo.png assets/output/output.png
./build/image_pipeline assets/input/photo.png assets/output/output.png 4
./build/image_pipeline assets/input/photo.png assets/output/output.png invert
./build/image_pipeline assets/input/photo.png assets/output/output.png 4 invert
```

## Expected Output

Example console output:

```text
Concurrent Image Processing Pipeline
Input : assets/input/photo.png
Output: assets/output/output.png
Workers: 4
Filter: grayscale

[Producer] Finished sending 48 chunks.
[Worker 0] Processed 12 chunks.
[Worker 1] Processed 12 chunks.
[Worker 2] Processed 12 chunks.
[Worker 3] Processed 12 chunks.
[Collector] Saved image to assets/output/output.png

========== Pipeline Summary ==========
Image size      : 640 x 480 (BGR)
Chunk rows      : 16
Total chunks    : 30
Buffer slots    : 8
Filter          : grayscale
Workers         : 4
  Worker 0 chunks : 8
  Worker 1 chunks : 8
  Worker 2 chunks : 7
  Worker 3 chunks : 7
Chunks collected: 30
Elapsed time    : 0.0523 s
Output saved to : assets/output/output.png
======================================
```

The output image in `assets/output/` should be a **grayscale** version of the input.

## Viva Questions and Answers

**Q1: Why use `fork()` instead of threads?**  
**A:** To demonstrate **process-based** parallelism and separate address spaces. IPC via shared memory is required because `fork()` children do not share heap data automatically (except mapped shared regions).

**Q2: What is the role of `shm_open()` and `mmap()`?**  
**A:** `shm_open()` creates/opens a shared memory object. `mmap()` maps it into the virtual address space of each process so producer, workers, and collector can read/write the same header and chunk slots.

**Q3: Why do we need semaphores if we already have shared memory?**  
**A:** Shared memory does not provide **synchronization**. Semaphores prevent race conditions (e.g., worker reading a slot before producer finishes writing).

**Q4: Explain producer–consumer here.**  
**A:** The producer fills slots (buffer); workers consume READY slots; the collector consumes DONE slots and frees buffers. `sem_empty`, `sem_work`, and `sem_done` coordinate these stages.

**Q5: What does `sem_empty` with initial value 8 mean?**  
**A:** There are 8 slot buffers. Each `sem_wait` reserves one slot; each `sem_post` from the collector returns one slot. The producer blocks when all 8 slots are full.

**Q6: How are chunks assigned to workers?**  
**A:** Worker `w` processes chunks where `chunk_id % num_workers == w`. This gives a simple static partition without a central task queue.

**Q7: Why might a worker call `sem_post(sem_work)` without processing?**  
**A:** If it wakes up but the READY chunk belongs to another worker, it **returns the token** so the correct worker can be signaled.

**Q8: Who calls `shm_unlink()` and `sem_unlink()`?**  
**A:** The **supervisor (parent)** after all children exit, to remove IPC objects from the system.

**Q9: What happens if the program crashes?**  
**A:** Named IPC objects may remain. The supervisor unlinks old objects before creating new ones to reduce leftover `/dev/shm` entries.

**Q10: Why `waitpid()` in the parent?**  
**A:** To **reap zombie child processes** and ensure the pipeline finished before cleanup and summary printing.

## How to Demonstrate in Viva

1. Draw the four process types and arrows between them.
2. Show `/dev/shm` or explain named shared memory (`/img_pipeline_shm`).
3. Run the program live with 2 and 4 workers; compare `worker_stats` in the summary.
4. Open input vs output image to prove the grayscale filter.
5. Point to `fork`, `sem_wait`, and `shm_open` in `main.cpp` and explain one full chunk lifecycle: FREE → READY → DONE → FREE.

## License

Educational use for Operating Systems coursework.

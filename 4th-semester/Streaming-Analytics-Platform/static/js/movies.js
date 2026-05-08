let moviesByYearChart, moviesRatingChart;

let moviesPage = 1;
let moviesPageSize = 10;
let moviesTotal = 0;

if (typeof fetchJSON === 'undefined') {
  console.warn('movies.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initMovies;
  document.head.appendChild(script);
} else {
  initMovies();
}

function initMovies() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMovies);
  } else {
    initializeMovies();
  }
}

function createChart(ref, ctx, type, labels, data, label) {
  if (ref) {
    ref.data.labels = labels;
    ref.data.datasets[0].data = data;
    ref.update();
    return ref;
  }
  return new Chart(ctx, {
    type,
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(37, 99, 235, 1)",
          borderWidth: 1.5
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true, labels: { color: "#111827" } }
      },
      scales: {
        x: { ticks: { color: "#111827" } },
        y: { beginAtZero: true, ticks: { color: "#111827" } }
      }
    }
  });
}

function updateMoviesMeta(total, avg, maxDur) {
  const totalMeta = document.getElementById("moviesTotalMeta");
  const avgMeta = document.getElementById("moviesAvgMeta");
  const maxMeta = document.getElementById("moviesMaxMeta");

  if (totalMeta) totalMeta.textContent = `${total} titles in catalog`;
  if (avgMeta) avgMeta.textContent = "Average across all movies with ratings";
  if (maxMeta) maxMeta.textContent = "Longest movie duration in minutes";
}

async function loadMovieStats() {
  try {
    const data = await fetchJSON("/api/movies/stats");
    const totalElement = document.getElementById("moviesTotal");
    const avgElement = document.getElementById("moviesAvgRating");
    const maxElement = document.getElementById("moviesMaxDuration");

    if (totalElement) totalElement.textContent = data.total || 0;
    if (avgElement) avgElement.textContent = (data.avgRating || 0).toFixed(2);
    if (maxElement) maxElement.textContent = data.maxDuration || 0;

    updateMoviesMeta(data.total || 0, data.avgRating || 0, data.maxDuration || 0);
  } catch (error) {
    console.error("Error loading movie stats:", error);
    const totalElement = document.getElementById("moviesTotal");
    const avgElement = document.getElementById("moviesAvgRating");
    const maxElement = document.getElementById("moviesMaxDuration");

    if (totalElement) totalElement.textContent = "Error";
    if (avgElement) avgElement.textContent = "Error";
    if (maxElement) maxElement.textContent = "Error";
  }
}

async function loadMoviesByYear() {
  try {
    const data = await fetchJSON("/api/movies/by-year");
    const labels = data.map(d => d._id || "Unknown");
    const values = data.map(d => d.count || 0);
    const ctx = document.getElementById("moviesByYearChart");
    if (!ctx) return;
    moviesByYearChart = createChart(
      moviesByYearChart,
      ctx,
      "bar",
      labels,
      values,
      "Movies"
    );
  } catch (error) {
    console.error("Error loading movies by year:", error);
  }
}

async function loadRatingDistribution() {
  try {
    const data = await fetchJSON("/api/movies/rating-distribution");
    const labels = data.map(d => `${d._id}★`);
    const values = data.map(d => d.count || 0);
    const ctx = document.getElementById("moviesRatingChart");
    if (!ctx) return;
    moviesRatingChart = createChart(
      moviesRatingChart,
      ctx,
      "bar",
      labels,
      values,
      "Movies"
    );
  } catch (error) {
    console.error("Error loading rating distribution:", error);
  }
}

function updateMoviesPaginationUI() {
  const info = document.getElementById("moviesPageInfo");
  const prev = document.getElementById("moviesPrev");
  const next = document.getElementById("moviesNext");
  if (!info || !prev || !next) return;

  if (!moviesTotal) {
    info.textContent = "No movies";
    prev.disabled = true;
    next.disabled = true;
    return;
  }

  const start = (moviesPage - 1) * moviesPageSize + 1;
  const end = Math.min(moviesPage * moviesPageSize, moviesTotal);
  info.textContent = `Showing ${start}–${end} of ${moviesTotal}`;

  prev.disabled = moviesPage <= 1;
  next.disabled = end >= moviesTotal;
}

async function loadSampleMovies() {
  try {
    const url = `/api/movies/sample-paged?page=${encodeURIComponent(moviesPage)}` +
                `&page_size=${encodeURIComponent(moviesPageSize)}`;
    const data = await fetchJSON(url);

    moviesPage = data.page || moviesPage;
    moviesPageSize = data.page_size || moviesPageSize;
    moviesTotal = data.total || 0;

    const tbody = document.querySelector("#moviesSampleTable tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!data.docs || data.docs.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-muted py-3">
            No movies found
          </td>
        </tr>
      `;
      updateMoviesPaginationUI();
      return;
    }

    data.docs.forEach(m => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${m.title ?? ""}</td>
        <td>${m.release_year ?? ""}</td>
        <td>${m.duration_min ?? ""}</td>
        <td>${m.rating_avg ? m.rating_avg.toFixed(2) : ""}</td>
      `;
      tbody.appendChild(tr);
    });

    updateMoviesPaginationUI();
  } catch (error) {
    console.error("Error loading sample movies:", error);
    const tbody = document.querySelector("#moviesSampleTable tbody");
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-danger py-3">
            Error loading movies
          </td>
        </tr>
      `;
    }
    updateMoviesPaginationUI();
  }
}

function initializeMovies() {
  if (!document.getElementById("moviesTotal")) return;

  loadMovieStats();
  loadMoviesByYear();
  loadRatingDistribution();
  loadSampleMovies();

  const prevBtn = document.getElementById("moviesPrev");
  const nextBtn = document.getElementById("moviesNext");

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      if (moviesPage > 1) {
        moviesPage -= 1;
        loadSampleMovies();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const maxPage = Math.ceil(moviesTotal / moviesPageSize);
      if (moviesPage < maxPage) {
        moviesPage += 1;
        loadSampleMovies();
      }
    });
  }
}
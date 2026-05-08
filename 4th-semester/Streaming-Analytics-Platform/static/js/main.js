let topMoviesChart, topGenresChart, activeUsersChart, reviewsChart, plansPieChart;

if (typeof fetchJSON === 'undefined') {
  console.warn('main.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initDashboard;
  document.head.appendChild(script);
} else {
  initDashboard();
}

function initDashboard() {

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCharts);
  } else {
    initializeCharts();
  }
}

function createOrUpdateChart(chartRef, ctx, type, labels, data, label, extraOptions = {}) {
  const baseDataset = {
    label,
    data
  };

  if (type === "pie" || type === "doughnut") {
    const palette = [
      "#f97316", "#22c55e", "#3b82f6", "#a855f7",
      "#ef4444", "#14b8a6", "#eab308", "#fb7185",
      "#6366f1", "#facc15"
    ];
    baseDataset.backgroundColor = labels.map((_, i) => palette[i % palette.length]);
  } else {
    baseDataset.backgroundColor = "rgba(59, 130, 246, 0.6)";
    baseDataset.borderColor = "rgba(37, 99, 235, 1)";
    baseDataset.borderWidth = 1.5;
  }

  if (chartRef) {
    chartRef.data.labels = labels;
    chartRef.data.datasets[0].data = data;
    chartRef.update();
    return chartRef;
  }

  return new Chart(ctx, {
    type,
    data: {
      labels,
      datasets: [baseDataset]
    },
    options: Object.assign(
      {
        responsive: true,
        plugins: {
          legend: { display: true, labels: { color: "#111827" } }
        },
        scales:
          type === "pie" || type === "doughnut"
            ? {}
            : {
                x: { ticks: { color: "#111827" } },
                y: { beginAtZero: true, ticks: { color: "#111827" } }
              }
      },
      extraOptions
    )
  });
}

async function loadSummaryStats() {
  try {
    const data = await fetchJSON("/api/summary-stats");
    document.getElementById("statUsers").textContent = data.users || 0;
    document.getElementById("statMovies").textContent = data.movies || 0;
    document.getElementById("statActors").textContent = data.actors || 0;
    document.getElementById("statDirectors").textContent = data.directors || 0;
    document.getElementById("statSubs").textContent = data.active_subscriptions || 0;
    document.getElementById("statRevenue").textContent = (data.total_payments || 0).toFixed(2);
  } catch (e) {
    console.error("Failed to load summary stats:", e);

    ["statUsers", "statMovies", "statActors", "statDirectors", "statSubs", "statRevenue"]
      .forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = "0";
      });
  }
}

async function loadTopMovies() {
  try {
    const data = await fetchJSON("/api/top-movies");
    const labels = data.map(d => d.title);
    const values = data.map(d => d.avgRating);
    const ctx = document.getElementById("topMoviesChart");
    if (!ctx) return;
    topMoviesChart = createOrUpdateChart(
      topMoviesChart,
      ctx,
      "bar",
      labels,
      values,
      "Average Rating"
    );
  } catch (e) {
    console.error("Failed to load top movies:", e);
  }
}

async function loadTopGenres() {
  try {
    const data = await fetchJSON("/api/top-genres");
    const labels = data.map(d => d._id || "Unknown");
    const values = data.map(d => d.count || 0);
    const ctx = document.getElementById("topGenresChart");
    if (!ctx) return;
    topGenresChart = createOrUpdateChart(
      topGenresChart,
      ctx,
      "bar",
      labels,
      values,
      "Movie Count"
    );
  } catch (e) {
    console.error("Failed to load top genres:", e);
  }
}

async function loadActiveUsers() {
  try {
    const data = await fetchJSON("/api/active-users?limit=10");
    const labels = data.map(d => d.user);
    const values = data.map(d => d.watches);
    const ctx = document.getElementById("activeUsersChart");
    if (!ctx) return;
    activeUsersChart = createOrUpdateChart(
      activeUsersChart,
      ctx,
      "bar",
      labels,
      values,
      "Watch Count"
    );
  } catch (e) {
    console.error("Failed to load active users:", e);
  }
}

async function loadReviewsPerMonth() {
  try {
    const year = document.getElementById("reviewsYear")?.value || "2025";
    const data = await fetchJSON(`/api/reviews-per-month?year=${encodeURIComponent(year)}`);
    const labels = data.map(d => d._id || "Unknown");
    const values = data.map(d => d.reviews || 0);
    const ctx = document.getElementById("reviewsChart");
    if (!ctx) return;
    reviewsChart = createOrUpdateChart(
      reviewsChart,
      ctx,
      "line",
      labels,
      values,
      "Reviews"
    );
  } catch (e) {
    console.error("Failed to load reviews per month:", e);
  }
}

async function loadPlansPie() {
  try {
    const data = await fetchJSON("/api/subscription-plans");
    const labels = data.map(d => d._id || "Unknown");
    const values = data.map(d => d.count || 0);
    const ctx = document.getElementById("plansPieChart");
    if (!ctx) return;
    plansPieChart = createOrUpdateChart(
      plansPieChart,
      ctx,
      "pie",
      labels,
      values,
      "Subscriptions by Plan"
    );
  } catch (e) {
    console.error("Failed to load subscription plans:", e);
  }
}

async function loadMoviesTable() {
  const minYear = document.getElementById("minYear")?.value || 0;
  const minRating = document.getElementById("minRating")?.value || 0;
  const limit = document.getElementById("limit")?.value || 0;
  const sortBy = document.getElementById("sortBy")?.value || "rating";
  const sortDir = document.getElementById("sortDir")?.value || "desc";

  const url = `/api/movies?min_year=${encodeURIComponent(minYear)}` +
    `&min_rating=${encodeURIComponent(minRating)}` +
    `&limit=${encodeURIComponent(limit)}` +
    `&sort_by=${encodeURIComponent(sortBy)}` +
    `&sort_dir=${encodeURIComponent(sortDir)}`;

  try {
    const data = await fetchJSON(url);
    const tbody = document.querySelector("#moviesTable tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!data || !Array.isArray(data)) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-muted">No movies found</td></tr>';
      return;
    }

    data.forEach(m => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${m.title ?? ""}</td>
        <td>${m.release_year ?? ""}</td>
        <td>${m.duration_min ?? ""}</td>
        <td>${m.rating_avg ? m.rating_avg.toFixed(2) : ""}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Failed to load movies table:", e);
    const tbody = document.querySelector("#moviesTable tbody");
    if (tbody) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-danger">Error loading movies</td></tr>';
    }
  }
}

function initializeCharts() {
  if (!document.getElementById("statUsers")) return;

  loadSummaryStats();
  loadTopMovies();
  loadTopGenres();
  loadActiveUsers();
  loadReviewsPerMonth();
  loadPlansPie();
  loadMoviesTable();

  const btnLoadMovies = document.getElementById("btnLoadMovies");
  if (btnLoadMovies) {
    btnLoadMovies.addEventListener("click", loadMoviesTable);
  }

  const reviewsYearInput = document.getElementById("reviewsYear");
  if (reviewsYearInput) {
    reviewsYearInput.addEventListener("change", loadReviewsPerMonth);
  }
}
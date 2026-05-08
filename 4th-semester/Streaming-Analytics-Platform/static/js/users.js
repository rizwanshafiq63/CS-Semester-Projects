let usersCountryChart;

let usersPage = 1;
let usersPageSize = 10;
let usersTotal = 0;

if (typeof fetchJSON === 'undefined') {
  console.warn('users.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initUsers;
  document.head.appendChild(script);
} else {
  initUsers();
}

function initUsers() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUsers);
  } else {
    initializeUsers();
  }
}

function createBarChart(ref, ctx, labels, data, label) {
  if (ref) {
    ref.data.labels = labels;
    ref.data.datasets[0].data = data;
    ref.update();
    return ref;
  }
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          backgroundColor: "rgba(34, 197, 94, 0.6)",
          borderColor: "rgba(22, 163, 74, 1)",
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

async function loadUsersCountry() {
  try {
    const data = await fetchJSON("/api/users/country-counts");
    const total = data.reduce((sum, d) => sum + d.count, 0);
    const totalElement = document.getElementById("usersTotal");
    if (totalElement) totalElement.textContent = total;

    const countryCount = data.length;
    const avgPerCountry = countryCount ? Math.round(total / countryCount) : 0;
    const meta = document.getElementById("usersMeta");
    if (meta) {
      meta.textContent = `${countryCount} countries · ~${avgPerCountry} users/country`;
    }

    const top = data.slice(0, 8);
    const labels = top.map(d => d._id || "Unknown");
    const values = top.map(d => d.count);
    const ctx = document.getElementById("usersCountryChart");
    if (!ctx) return;
    usersCountryChart = createBarChart(
      usersCountryChart,
      ctx,
      labels,
      values,
      "Users"
    );
  } catch (error) {
    console.error("Error loading users country data:", error);
    const totalElement = document.getElementById("usersTotal");
    if (totalElement) totalElement.textContent = "Error";
  }
}

function updateUsersPaginationUI() {
  const info = document.getElementById("usersPageInfo");
  const prev = document.getElementById("usersPrev");
  const next = document.getElementById("usersNext");
  if (!info || !prev || !next) return;

  if (!usersTotal) {
    info.textContent = "No users";
    prev.disabled = true;
    next.disabled = true;
    return;
  }

  const start = (usersPage - 1) * usersPageSize + 1;
  const end = Math.min(usersPage * usersPageSize, usersTotal);
  info.textContent = `Showing ${start}–${end} of ${usersTotal}`;
  prev.disabled = usersPage <= 1;
  next.disabled = end >= usersTotal;
}

async function loadUsersTable() {
  try {
    const url = `/api/users/sample-paged?page=${encodeURIComponent(usersPage)}` +
                `&page_size=${encodeURIComponent(usersPageSize)}`;
    const data = await fetchJSON(url);

    usersPage = data.page || usersPage;
    usersPageSize = data.page_size || usersPageSize;
    usersTotal = data.total || 0;

    const tbody = document.querySelector("#usersTable tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!data.docs || data.docs.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-muted py-3">
            No users found
          </td>
        </tr>
      `;
      updateUsersPaginationUI();
      return;
    }

    data.docs.forEach(u => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${u.name ?? ""}</td>
        <td>${u.email ?? ""}</td>
        <td>${u.country ?? ""}</td>
        <td>${u.join_date ? u.join_date.slice(0, 10) : ""}</td>
      `;
      tbody.appendChild(tr);
    });

    updateUsersPaginationUI();
  } catch (error) {
    console.error("Error loading users table:", error);
    const tbody = document.querySelector("#usersTable tbody");
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="4" class="text-center text-danger py-3">
            Error loading users
          </td>
        </tr>
      `;
    }
    updateUsersPaginationUI();
  }
}

function initializeUsers() {
  if (!document.getElementById("usersTotal")) return;

  loadUsersCountry();
  loadUsersTable();

  const prevBtn = document.getElementById("usersPrev");
  const nextBtn = document.getElementById("usersNext");

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      if (usersPage > 1) {
        usersPage -= 1;
        loadUsersTable();
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const maxPage = Math.ceil(usersTotal / usersPageSize);
      if (usersPage < maxPage) {
        usersPage += 1;
        loadUsersTable();
      }
    });
  }
}
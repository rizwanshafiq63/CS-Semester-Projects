let subsPlanPie;

let paymentsPage = 1;
let paymentsPageSize = 10;
let paymentsTotal = 0;

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

function createPieChart(ref, ctx, labels, data, label) {
  const palette = [
    "#f97316", "#22c55e", "#3b82f6", "#a855f7",
    "#ef4444", "#14b8a6", "#eab308", "#fb7185"
  ];
  if (ref) {
    ref.data.labels = labels;
    ref.data.datasets[0].data = data;
    ref.update();
    return ref;
  }
  return new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          backgroundColor: labels.map((_, i) => palette[i % palette.length])
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true, labels: { color: "#111827" } }
      }
    }
  });
}

async function loadSubsStats() {
  const stats = await fetchJSON("/api/subscriptions/stats");
  document.getElementById("subsTotal").textContent = stats.total;
  document.getElementById("subsActive").textContent = stats.active;

  const plans = await fetchJSON("/api/subscription-plans");
  const labels = plans.map(p => p._id || "Unknown");
  const values = plans.map(p => p.count);
  const ctx = document.getElementById("subsPlanPie");
  if (ctx) {
    subsPlanPie = createPieChart(subsPlanPie, ctx, labels, values, "Subscriptions");
  }

  const planCount = plans.length;
  const totalMeta = document.getElementById("subsTotalMeta");
  const activeMeta = document.getElementById("subsActiveMeta");
  if (totalMeta) {
    totalMeta.textContent = `${planCount} plans configured`;
  }
  if (activeMeta) {
    const rate = stats.total ? Math.round((stats.active / stats.total) * 100) : 0;
    activeMeta.textContent = `Active rate: ${rate}%`;
  }
}

function updatePaymentsPaginationUI() {
  const info = document.getElementById("paymentsPageInfo");
  const prev = document.getElementById("paymentsPrev");
  const next = document.getElementById("paymentsNext");
  if (!info || !prev || !next) return;

  if (!paymentsTotal) {
    info.textContent = "No payments";
    prev.disabled = true;
    next.disabled = true;
    return;
  }

  const start = (paymentsPage - 1) * paymentsPageSize + 1;
  const end = Math.min(paymentsPage * paymentsPageSize, paymentsTotal);
  info.textContent = `Showing ${start}–${end} of ${paymentsTotal}`;
  prev.disabled = paymentsPage <= 1;
  next.disabled = end >= paymentsTotal;
}

async function loadPaymentsTable() {
  const url =
    `/api/payments/sample-paged?page=${encodeURIComponent(paymentsPage)}` +
    `&page_size=${encodeURIComponent(paymentsPageSize)}`;
  const data = await fetchJSON(url);

  paymentsPage = data.page || paymentsPage;
  paymentsPageSize = data.page_size || paymentsPageSize;
  paymentsTotal = data.total || 0;

  const tbody = document.querySelector("#paymentsTable tbody");
  if (!tbody) return;
  tbody.innerHTML = "";
  (data.docs || []).forEach(p => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${p.user_id ?? ""}</td>
      <td>${p.amount_usd ?? ""}</td>
      <td>${p.method ?? ""}</td>
      <td>${p.paid_at ?? ""}</td>
    `;
    tbody.appendChild(tr);
  });

  updatePaymentsPaginationUI();
}

document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("subsTotal")) return;

  loadSubsStats();
  loadPaymentsTable();

  document.getElementById("paymentsPrev").addEventListener("click", () => {
    if (paymentsPage > 1) {
      paymentsPage -= 1;
      loadPaymentsTable();
    }
  });

  document.getElementById("paymentsNext").addEventListener("click", () => {
    const maxPage = Math.ceil(paymentsTotal / paymentsPageSize);
    if (paymentsPage < maxPage) {
      paymentsPage += 1;
      loadPaymentsTable();
    }
  });
});
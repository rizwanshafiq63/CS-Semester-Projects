if (typeof fetchJSON === 'undefined') {
  console.warn('advanced.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initAdvanced;
  document.head.appendChild(script);
} else {
  initAdvanced();
}

function initAdvanced() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAdvanced);
  } else {
    initializeAdvanced();
  }
}

function renderEngagementTable(data) {
  const tbody = document.getElementById("engagementBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (!data || !data.length) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-muted">No data</td></tr>`;
    return;
  }

  data.forEach(row => {
    const engagement = row.engagement || 0;
    let level = "Beginner";
    let levelClass = "bg-secondary";

    if (engagement > 50) {
      level = "Advanced";
      levelClass = "bg-success";
    } else if (engagement > 20) {
      level = "Intermediate";
      levelClass = "bg-primary";
    }

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.user || ""}</td>
      <td>${row.watches || 0}</td>
      <td>${(row.avg_rating || 0).toFixed ? (row.avg_rating || 0).toFixed(2) : row.avg_rating}</td>
      <td>${(row.engagement || 0).toFixed ? (row.engagement || 0).toFixed(2) : row.engagement}</td>
      <td><span class="badge ${levelClass}">${level}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

async function runUserEngagement() {
  try {
    const btn = document.getElementById("btnUserEngagement");
    if (btn) btn.disabled = true;

    const data = await fetchJSON("/api/analytics/user-engagement");
    renderEngagementTable(data);

    if (btn) btn.disabled = false;
  } catch (e) {
    console.error("Engagement failed:", e);
    const tbody = document.getElementById("engagementBody");
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-danger">Error: ${e.message}</td></tr>`;
    }
    const btn = document.getElementById("btnUserEngagement");
    if (btn) btn.disabled = false;
  }
}

function exportToCSV() {
  const rows = Array.from(document.querySelectorAll("#engagementBody tr"));
  if (!rows.length) {
    alert("No data to export. Run the aggregation first.");
    return;
  }

  let csv = "User,Watches,Avg Rating,Engagement Score,Level\n";

  rows.forEach(row => {
    const cells = row.querySelectorAll("td");
    if (cells.length === 5) {
      const user = cells[0].textContent.trim();
      const watches = cells[1].textContent.trim();
      const avgRating = cells[2].textContent.trim();
      const engagement = cells[3].textContent.trim();
      const level = cells[4].querySelector(".badge")?.textContent.trim() || "";

      csv += `"${user}",${watches},${avgRating},${engagement},"${level}"\n`;
    }
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "user_engagement.csv";
  a.click();
  window.URL.revokeObjectURL(url);
}

function initializeAdvanced() {
  const btnEng = document.getElementById("btnUserEngagement");
  if (btnEng) btnEng.addEventListener("click", runUserEngagement);

  const btnExport = document.getElementById("btnExportCsv");
  if (btnExport) btnExport.addEventListener("click", exportToCSV);

  runUserEngagement();
}
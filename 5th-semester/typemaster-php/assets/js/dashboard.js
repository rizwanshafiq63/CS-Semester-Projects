// Dashboard logic (API-backed)

document.addEventListener("DOMContentLoaded", async () => {
  loadComponent("navbar-container", "components/navbar.html");
  loadComponent("footer-container", "components/footer.html");

  if (!auth.requireAuth()) return;

  try {
    const statsRes = await window.api.getMyStats();

    const user = auth.getCurrentUser();
    if (user && document.getElementById("user-name")) {
      document.getElementById("user-name").textContent = user.name || "User";
    }

    // Stats cards
    document.getElementById("tests-taken").textContent = statsRes.totalTests;
    document.getElementById("avg-wpm").textContent = Math.round(statsRes.averageWpm);
    document.getElementById("avg-accuracy").textContent =
      Math.round(statsRes.averageAccuracy) + "%";
    document.getElementById("best-wpm").textContent = statsRes.bestWpm;

    const totalSeconds = Number(statsRes.totalTime || 0);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    document.getElementById("total-time").textContent =
      hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;

    const improvement = Number(statsRes.improvementPercentage || 0);
    const improvementRounded = Math.round(improvement);
    document.getElementById("improvement").textContent =
      (improvement > 0 ? "+" : "") + improvementRounded + "%";

    // Recent tests (table)
    renderRecentTests(statsRes.recentTests || []);
    // Progress chart
    drawProgressChart(statsRes.recentTests || []);

    window.addEventListener("resize", () => {
      drawProgressChart(statsRes.recentTests || []);
    });
  } catch (e) {
    console.error("Dashboard load failed:", e);
    showToast(e.message || "Failed to load dashboard data", "error");
  }
});

function renderRecentTests(tests) {
  const tbody = document.getElementById("tests-table-body");
  const noTestsMsg = document.getElementById("no-tests-message");
  const table = document.querySelector(".tests-table");

  if (!tbody || !noTestsMsg || !table) return;

  const recent = (tests || []).slice(0, 5); // already latest-first

  if (recent.length > 0) {
    tbody.innerHTML = recent
      .map((test) => {
        const dateStr = formatDate(test.createdAt || test.date);
        const accuracy = typeof test.accuracy === "number" ? test.accuracy.toFixed(1) : test.accuracy;
        return `
          <tr>
            <td>${dateStr}</td>
            <td class="stat-highlight">${test.wpm}</td>
            <td>${accuracy}%</td>
            <td>${formatTime(Math.floor(test.timeTaken || 0))}</td>
            <td>${test.mistakes || 0}</td>
          </tr>
        `;
      })
      .join("");

    table.style.display = "table";
    noTestsMsg.style.display = "none";
  } else {
    table.style.display = "none";
    noTestsMsg.style.display = "block";
  }
}

function formatDate(dateString) {
  if (!dateString) return "-";
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return `${diffDays} days ago`;
  return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function drawProgressChart(tests) {
  const canvas = document.getElementById("progress-chart");
  const noDataMsg = document.getElementById("no-chart-data");
  if (!canvas || !noDataMsg) return;
  const container = canvas.parentElement;
  if (!container) return;

  const history = [...(tests || [])].reverse(); // chronological

  if (history.length < 2) {
    canvas.style.display = "none";
    noDataMsg.style.display = "block";
    return;
  }

  canvas.style.display = "block";
  noDataMsg.style.display = "none";

  const ctx = canvas.getContext("2d");
  const rootStyles = getComputedStyle(document.documentElement);
  const borderColor = rootStyles.getPropertyValue("--border").trim() || "#6272a4";
  const mutedTextColor = rootStyles.getPropertyValue("--text-secondary").trim() || "#bfbfbf";
  const accentColor = rootStyles.getPropertyValue("--accent").trim() || "#bd93f9";
  const infoColor = rootStyles.getPropertyValue("--info").trim() || "#8be9fd";
  const backgroundColor = rootStyles.getPropertyValue("--bg-primary").trim() || "#282a36";

  canvas.width = container.clientWidth;
  canvas.height = 300;

  const padding = 50;
  const chartWidth = canvas.width - padding * 2;
  const chartHeight = canvas.height - padding * 2;

  const maxWPM = Math.max(...history.map((t) => t.wpm), 50);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Grid lines
  ctx.strokeStyle = borderColor;
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= 5; i++) {
    const y = padding + (chartHeight / 5) * i;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(canvas.width - padding, y);
    ctx.stroke();

    ctx.fillStyle = mutedTextColor;
    ctx.font = "12px Inter, sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(Math.round(maxWPM - (maxWPM / 5) * i), padding - 10, y + 4);
  }

  // Line
  ctx.beginPath();
  ctx.strokeStyle = accentColor;
  ctx.lineWidth = 3;

  history.forEach((test, index) => {
    const x = padding + (chartWidth / (history.length - 1)) * index;
    const y = padding + chartHeight - (test.wpm / maxWPM) * chartHeight;
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Points
  history.forEach((test, index) => {
    const x = padding + (chartWidth / (history.length - 1)) * index;
    const y = padding + chartHeight - (test.wpm / maxWPM) * chartHeight;

    ctx.beginPath();
    ctx.fillStyle = infoColor;
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = backgroundColor;
    ctx.lineWidth = 2;
    ctx.stroke();
  });

  setupChartTooltip(canvas, container, history, maxWPM, padding, chartWidth, chartHeight);
}

function setupChartTooltip(canvas, container, history, maxWPM, padding, chartWidth, chartHeight) {
  if (!history.length) return;

  let tooltip = container.querySelector(".chart-tooltip");
  if (!tooltip) {
    tooltip = document.createElement("div");
    tooltip.className = "chart-tooltip";
    tooltip.style.display = "none";
    container.appendChild(tooltip);
  }

  const points = history.map((test, index) => ({
    test,
    x: padding + (chartWidth / (history.length - 1)) * index,
    y: padding + chartHeight - (test.wpm / maxWPM) * chartHeight,
  }));

  const renderTooltip = (point, pointerX, pointerY) => {
    const date = new Date(point.test.createdAt || point.test.date || Date.now());
    const dateText = date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
    const accuracyText =
      typeof point.test.accuracy === "number"
        ? `${point.test.accuracy.toFixed(1)}%`
        : "N/A";
    const mistakesText =
      point.test.mistakes !== undefined && point.test.mistakes !== null
        ? point.test.mistakes
        : "N/A";

    tooltip.innerHTML = `
      <div><strong>${dateText}</strong></div>
      <div>WPM: ${point.test.wpm}</div>
      <div>Accuracy: ${accuracyText}</div>
      <div>Mistakes: ${mistakesText}</div>
    `;

    tooltip.style.display = "block";
    tooltip.style.left = `${pointerX}px`;
    tooltip.style.top = `${pointerY}px`;
  };

  canvas.onmousemove = (event) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    let closest = null;
    let minDistance = Infinity;

    points.forEach((point) => {
      const distance = Math.hypot(mouseX - point.x, mouseY - point.y);
      if (distance < minDistance) {
        minDistance = distance;
        closest = point;
      }
    });

    if (!closest || minDistance > 18) {
      tooltip.style.display = "none";
      return;
    }

    renderTooltip(closest, closest.x, closest.y);
  };

  canvas.onmouseleave = () => {
    tooltip.style.display = "none";
  };
}


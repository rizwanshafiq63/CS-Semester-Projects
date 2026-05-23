// Profile logic (API-backed)

let userProfileState = {
  user: null,
  history: [],
  stats: {},
};
const HISTORY_PAGE_SIZE = 10;
let historyCurrentPage = 1;

document.addEventListener("DOMContentLoaded", async () => {
  loadComponent("navbar-container", "components/navbar.html");
  loadComponent("footer-container", "components/footer.html");

  if (!auth.requireAuth()) return;

  try {
    await loadProfileData();
  } catch (e) {
    console.error("Profile load failed:", e);
    showToast(e.message || "Failed to load profile", "error");
  }

  // Settings + avatar UI doesn't depend on server data
  loadUserSettings();
  attachProfileForms();

  // Render UI once state is ready
  renderAll();

  const params = new URLSearchParams(window.location.search);
  const section = params.get("section");
  if (section && ["overview", "edit", "history", "settings"].includes(section)) {
    switchSection(section);
  }
});

async function loadProfileData() {
  const [profileRes, statsRes] = await Promise.all([
    window.api.getProfile(),
    window.api.getMyStats(),
  ]);

  const user = profileRes.user;
  const totalStats = {
    totalTests: statsRes.totalTests,
    averageWpm: statsRes.averageWpm,
    bestWpm: statsRes.bestWpm,
    averageAccuracy: statsRes.averageAccuracy,
    totalTime: statsRes.totalTime,
    improvementPercentage: statsRes.improvementPercentage,
    recentTests: statsRes.recentTests || [],
  };

  userProfileState.user = user;
  userProfileState.stats = totalStats;
  userProfileState.history = totalStats.recentTests;
}

function renderAll() {
  if (!userProfileState.user) return;

  // Sidebar
  document.getElementById("profile-name").textContent = userProfileState.user.name || "User";
  document.getElementById("profile-email").textContent = userProfileState.user.email || "";
  document.getElementById("avatar-initial").textContent = (userProfileState.user.name || "U").charAt(0).toUpperCase();

  const createdAt = userProfileState.user.createdAt || userProfileState.user.createdAt;
  if (createdAt) {
    const joinedDate = new Date(createdAt);
    const options = { year: "numeric", month: "long" };
    document.getElementById("profile-joined").textContent =
      `Member since ${joinedDate.toLocaleDateString("en-US", options)}`;
  }

  renderBadges();
  renderOverview();
  drawPerformanceChart();
  renderActivityList();
  renderTestHistory();
}

function renderOverview() {
  const s = userProfileState.stats || {};
  document.getElementById("overview-tests").textContent = s.totalTests || 0;
  document.getElementById("overview-avg-wpm").textContent = Math.round(s.averageWpm || 0);
  document.getElementById("overview-best-wpm").textContent = s.bestWpm || 0;
  document.getElementById("overview-avg-accuracy").textContent =
    Math.round(s.averageAccuracy || 0) + "%";

  const totalSeconds = Number(s.totalTime || 0);
  const totalMinutes = Math.floor(totalSeconds / 60);
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  document.getElementById("overview-total-time").textContent =
    hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;

  const improvement = Number(s.improvementPercentage || 0);
  document.getElementById("overview-improvement").textContent =
    (improvement > 0 ? "+" : "") + Math.round(improvement) + "%";
}

function renderBadges() {
  const stats = userProfileState.stats || {};
  const badgesContainer = document.getElementById("profile-badges");
  if (!badgesContainer) return;

  const badges = [];
  const testsTaken = stats.totalTests || 0;
  const averageAccuracy = stats.averageAccuracy || 0;
  const bestWpm = stats.bestWpm || 0;

  if (testsTaken >= 1) badges.push({ icon: "🎯", name: "Beginner" });
  if (testsTaken >= 10) badges.push({ icon: "📚", name: "Dedicated" });
  if (testsTaken >= 50) badges.push({ icon: "🏅", name: "Expert" });
  if (bestWpm >= 50) badges.push({ icon: "⚡", name: "Speedster" });
  if (bestWpm >= 100) badges.push({ icon: "🚀", name: "Lightning" });
  if (averageAccuracy >= 95) badges.push({ icon: "🎯", name: "Precision" });

  if (badges.length === 0) badges.push({ icon: "🌟", name: "Newcomer" });

  badgesContainer.innerHTML = badges
    .map(
      (badge) => `
      <div class="badge">
        <span class="badge-icon">${badge.icon}</span>
        <span class="badge-name">${badge.name}</span>
      </div>
    `
    )
    .join("");

  // Prefill edit form
  const nameInput = document.getElementById("edit-name");
  const emailInput = document.getElementById("edit-email");
  if (nameInput) nameInput.value = userProfileState.user.name || "";
  if (emailInput) emailInput.value = userProfileState.user.email || "";
}

function drawPerformanceChart() {
  const canvas = document.getElementById("performance-chart");
  if (!canvas) return;

  const historyLatestFirst = userProfileState.history || [];
  const history = [...historyLatestFirst].reverse(); // chronological

  const ctx = canvas.getContext("2d");
  const rootStyles = getComputedStyle(document.documentElement);
  const borderColor = rootStyles.getPropertyValue("--border").trim() || "#6272a4";
  const mutedTextColor = rootStyles.getPropertyValue("--text-secondary").trim() || "#bfbfbf";
  const accentColor = rootStyles.getPropertyValue("--accent").trim() || "#bd93f9";
  const infoColor = rootStyles.getPropertyValue("--info").trim() || "#8be9fd";
  const backgroundColor = rootStyles.getPropertyValue("--bg-primary").trim() || "#282a36";

  if (history.length < 2) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "14px Inter, sans-serif";
    ctx.fillStyle = "var(--text-muted)";
    ctx.textAlign = "center";
    ctx.fillText(
      "Complete at least 2 tests to see your progress chart",
      canvas.width / 2,
      canvas.height / 2
    );
    return;
  }

  const container = canvas.parentElement;
  canvas.width = container.clientWidth;
  canvas.height = 250;

  const padding = 40;
  const chartWidth = canvas.width - padding * 2;
  const chartHeight = canvas.height - padding * 2;

  const maxWPM = Math.max(...history.map((t) => t.wpm), 50);

  // Grid
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
}

function renderActivityList() {
  const activityList = document.getElementById("activity-list");
  if (!activityList) return;

  const history = userProfileState.history || [];
  if (history.length === 0) {
    activityList.innerHTML =
      '<p class="no-activity">No recent activity. Take a typing test to get started!</p>';
    return;
  }

  activityList.innerHTML = history
    .map((test) => {
      const date = new Date(test.createdAt || Date.now());
      const timeAgo = getTimeAgo(date);
      return `
        <div class="activity-item">
          <div class="activity-icon">${test.wpm >= 50 ? "🚀" : "⌨️"}</div>
          <div class="activity-content">
            <div class="activity-title">Typing Test - ${test.wpm} WPM</div>
            <div class="activity-meta">${test.accuracy}% accuracy • ${timeAgo}</div>
          </div>
          <div class="activity-stat">${test.wpm} WPM</div>
        </div>
      `;
    })
    .join("");
}

function renderTestHistory() {
  const tbody = document.getElementById("history-table-body");
  const noHistory = document.getElementById("no-history");
  const pagination = document.getElementById("history-pagination");
  const pageInfo = document.getElementById("history-page-info");
  const prevBtn = document.getElementById("history-prev-btn");
  const nextBtn = document.getElementById("history-next-btn");
  if (!tbody || !noHistory) return;

  const history = userProfileState.history || [];
  if (history.length === 0) {
    tbody.innerHTML = "";
    noHistory.style.display = "block";
    if (pagination) pagination.style.display = "none";
    return;
  }
  noHistory.style.display = "none";

  const totalPages = Math.max(1, Math.ceil(history.length / HISTORY_PAGE_SIZE));
  historyCurrentPage = Math.min(historyCurrentPage, totalPages);
  const start = (historyCurrentPage - 1) * HISTORY_PAGE_SIZE;
  const end = start + HISTORY_PAGE_SIZE;
  const pageRows = history.slice(start, end);

  tbody.innerHTML = pageRows
    .map((test) => {
      const date = new Date(test.createdAt || Date.now());
      const formattedDate = date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
      return `
        <tr>
          <td>${formattedDate}</td>
          <td class="stat-highlight">${test.wpm}</td>
          <td>${Math.round(test.accuracy)}%</td>
          <td>${formatTime(Math.floor(test.timeTaken || 0))}</td>
          <td>${test.mistakes || 0}</td>
        </tr>
      `;
    })
    .join("");

  if (pagination && pageInfo && prevBtn && nextBtn) {
    pagination.style.display = history.length > HISTORY_PAGE_SIZE ? "flex" : "none";
    pageInfo.textContent = `Page ${historyCurrentPage} of ${totalPages}`;
    prevBtn.disabled = historyCurrentPage <= 1;
    nextBtn.disabled = historyCurrentPage >= totalPages;
  }
}

function getTimeAgo(date) {
  const now = new Date();
  const diff = Math.floor((now - date) / 1000);
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} hours ago`;
  if (diff < 604800) return `${Math.floor(diff / 86400)} days ago`;
  return date.toLocaleDateString();
}

function switchSection(section) {
  document.querySelectorAll(".profile-nav-btn").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.section === section);
  });

  document.querySelectorAll(".profile-section").forEach((sectionEl) => {
    sectionEl.classList.remove("active");
  });

  document.getElementById(`${section}-section`).classList.add("active");

  if (section === "overview") {
    setTimeout(drawPerformanceChart, 100);
  }
}

// Expose to inline HTML handlers
window.switchSection = switchSection;

function attachProfileForms() {
  const historyPrevBtn = document.getElementById("history-prev-btn");
  const historyNextBtn = document.getElementById("history-next-btn");
  if (historyPrevBtn) {
    historyPrevBtn.addEventListener("click", () => {
      if (historyCurrentPage <= 1) return;
      historyCurrentPage -= 1;
      renderTestHistory();
    });
  }
  if (historyNextBtn) {
    historyNextBtn.addEventListener("click", () => {
      const history = userProfileState.history || [];
      const totalPages = Math.max(1, Math.ceil(history.length / HISTORY_PAGE_SIZE));
      if (historyCurrentPage >= totalPages) return;
      historyCurrentPage += 1;
      renderTestHistory();
    });
  }

  // Edit profile (name only)
  const profileForm = document.getElementById("profile-form");
  if (profileForm) {
    profileForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      try {
        const name = document.getElementById("edit-name").value;
        const email = document.getElementById("edit-email").value; // not editable by backend
        const res = await window.api.updateProfile({ name, email });

        showToast(res.message || "Profile updated", "success");
        setTimeout(() => location.reload(), 800);
      } catch (err) {
        showToast(err.message || "Profile update failed", "error");
      }
    });
  }

  // Password update UI: disabled (backend not provided in this phase)
  const passwordForm = document.getElementById("password-form");
  if (passwordForm) {
    passwordForm.addEventListener("submit", (e) => {
      e.preventDefault();
      showToast("Password change is not supported yet.", "info");
    });
  }
}

function loadUserSettings() {
  const settings = Storage.get("userSettings", {});
  if (settings.defaultDuration)
    document.getElementById("default-duration").value = settings.defaultDuration;
  if (settings.defaultDifficulty)
    document.getElementById("default-difficulty").value = settings.defaultDifficulty;
  if (settings.soundEffects !== undefined) document.getElementById("sound-effects").checked = settings.soundEffects;
  if (settings.showWPM !== undefined) document.getElementById("show-wpm").checked = settings.showWPM;
}

window.saveSettings = function saveSettings() {
  const settings = {
    defaultDuration: document.getElementById("default-duration").value,
    defaultDifficulty: document.getElementById("default-difficulty").value,
    soundEffects: document.getElementById("sound-effects").checked,
    showWPM: document.getElementById("show-wpm").checked,
  };
  Storage.set("userSettings", settings);
  showToast("Settings saved!", "success");
};

window.filterHistory = function filterHistory() {
  const filter = document.getElementById("history-filter")?.value || "all";
  const allHistory = userProfileState.stats.recentTests || [];
  const now = new Date();
  const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

  if (filter === "week") {
    userProfileState.history = allHistory.filter((test) => new Date(test.createdAt) >= weekAgo);
  } else if (filter === "month") {
    userProfileState.history = allHistory.filter((test) => new Date(test.createdAt) >= monthAgo);
  } else if (filter === "best") {
    userProfileState.history = [...allHistory].sort((a, b) => b.wpm - a.wpm).slice(0, 20);
  } else {
    userProfileState.history = [...allHistory];
  }

  historyCurrentPage = 1;
  renderTestHistory();
};

window.exportHistory = function exportHistory() {
  const history = userProfileState.history || [];
  let csv = "Date,WPM,Accuracy,Time,Mistakes\n";
  history.forEach((test) => {
    const createdAt = test.createdAt ? new Date(test.createdAt).toISOString() : "";
    csv += `${createdAt},${test.wpm},${Math.round(test.accuracy)}%,${test.timeTaken || 0},${test.mistakes || 0}\n`;
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "my-typing-history.csv";
  a.click();
  window.URL.revokeObjectURL(url);

  showToast("History exported!", "success");
};

window.clearHistory = function clearHistory() {
  showToast("Clearing history is not supported yet.", "info");
};

window.deleteAccount = function deleteAccount() {
  showToast("Account deletion is not supported yet.", "info");
};


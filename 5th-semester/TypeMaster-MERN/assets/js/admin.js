// Admin panel logic (API-backed)

let adminParagraphs = [];
let selectedParagraphId = null;
let adminFilteredParagraphs = [];
let adminSearchQuery = "";
let adminDifficultyFilter = "all";
let adminStatusFilter = "all";
let adminCurrentPage = 1;
const ADMIN_PAGE_SIZE = 10;

document.addEventListener("DOMContentLoaded", async () => {
  loadComponent("navbar-container", "components/navbar.html");
  loadComponent("footer-container", "components/footer.html");

  if (!auth.requireAuth()) return;

  const user = auth.getCurrentUser();
  if (!user || user.role !== "admin") {
    showToast("Admin access required", "error");
    window.location.href = "dashboard.html";
    return;
  }

  attachAdminFormHandlers();
  await loadParagraphs();
});

async function loadParagraphs() {
  const res = await window.api.adminGetParagraphs();
  // Backend returns: { paragraphs: [...] }
  adminParagraphs = res.paragraphs || [];
  applyAdminFilters();
}

function renderParagraphs() {
  const tbody = document.getElementById("admin-paragraphs-body");
  const empty = document.getElementById("admin-empty");
  const pagination = document.getElementById("admin-pagination");
  const pageInfo = document.getElementById("admin-page-info");
  const prevBtn = document.getElementById("admin-prev-btn");
  const nextBtn = document.getElementById("admin-next-btn");
  if (!tbody || !empty) return;

  if (adminFilteredParagraphs.length === 0) {
    empty.style.display = "block";
    tbody.innerHTML = "";
    if (pagination) pagination.style.display = "none";
    return;
  }

  empty.style.display = "none";
  const totalPages = Math.max(1, Math.ceil(adminFilteredParagraphs.length / ADMIN_PAGE_SIZE));
  adminCurrentPage = Math.min(adminCurrentPage, totalPages);
  const start = (adminCurrentPage - 1) * ADMIN_PAGE_SIZE;
  const end = start + ADMIN_PAGE_SIZE;
  const pageRows = adminFilteredParagraphs.slice(start, end);

  tbody.innerHTML = pageRows
    .map((p) => {
      const status = p.isActive ? "Active" : "Inactive";
      const statusClass = p.isActive ? "text-success" : "text-error";
      const text = p.text ? p.text.replace(/\s+/g, " ").trim() : "";
      const preview = text.length > 80 ? text.slice(0, 80) + "..." : text;

      return `
        <tr>
          <td title="${escapeHtml(text)}">${escapeHtml(preview)}</td>
          <td>${p.difficulty}</td>
          <td class="${statusClass}">${status}</td>
          <td>
            <div class="d-flex gap-1">
              <button type="button" class="btn btn-secondary btn-sm" onclick="selectParagraph('${p._id}')">Edit</button>
              <button type="button" class="btn btn-danger btn-sm" onclick="disableParagraph('${p._id}')">Disable</button>
            </div>
          </td>
        </tr>
      `;
    })
    .join("");

  if (pagination && pageInfo && prevBtn && nextBtn) {
    pagination.style.display = adminFilteredParagraphs.length > ADMIN_PAGE_SIZE ? "flex" : "none";
    pageInfo.textContent = `Page ${adminCurrentPage} of ${totalPages}`;
    prevBtn.disabled = adminCurrentPage <= 1;
    nextBtn.disabled = adminCurrentPage >= totalPages;
  }
}

function attachAdminFormHandlers() {
  const searchInput = document.getElementById("admin-search-input");
  const difficultyFilter = document.getElementById("admin-difficulty-filter");
  const statusFilter = document.getElementById("admin-status-filter");
  const prevBtn = document.getElementById("admin-prev-btn");
  const nextBtn = document.getElementById("admin-next-btn");

  if (searchInput) {
    searchInput.addEventListener("input", debounce((e) => {
      adminSearchQuery = e.target.value.toLowerCase().trim();
      adminCurrentPage = 1;
      applyAdminFilters();
    }, 250));
  }

  if (difficultyFilter) {
    difficultyFilter.addEventListener("change", (e) => {
      adminDifficultyFilter = e.target.value;
      adminCurrentPage = 1;
      applyAdminFilters();
    });
  }

  if (statusFilter) {
    statusFilter.addEventListener("change", (e) => {
      adminStatusFilter = e.target.value;
      adminCurrentPage = 1;
      applyAdminFilters();
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      if (adminCurrentPage <= 1) return;
      adminCurrentPage -= 1;
      renderParagraphs();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const totalPages = Math.max(1, Math.ceil(adminFilteredParagraphs.length / ADMIN_PAGE_SIZE));
      if (adminCurrentPage >= totalPages) return;
      adminCurrentPage += 1;
      renderParagraphs();
    });
  }

  const addForm = document.getElementById("add-paragraph-form");
  if (addForm) {
    addForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = document.getElementById("add-text").value;
      const difficulty = document.getElementById("add-difficulty").value;
      try {
        await window.api.adminAddParagraph({ text, difficulty });
        showToast("Paragraph added", "success");
        addForm.reset();
        await loadParagraphs();
      } catch (err) {
        showToast(err.message || "Failed to add paragraph", "error");
      }
    });
  }

  const editForm = document.getElementById("edit-paragraph-form");
  if (editForm) {
    editForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!selectedParagraphId) {
        showToast("Select a paragraph to edit", "info");
        return;
      }

      const text = document.getElementById("edit-text").value;
      const difficulty = document.getElementById("edit-difficulty").value;
      const isActive = document.getElementById("edit-isActive").checked;

      try {
        await window.api.adminUpdateParagraph(selectedParagraphId, {
          text,
          difficulty,
          isActive,
        });
        showToast("Paragraph updated", "success");
        await loadParagraphs();
      } catch (err) {
        showToast(err.message || "Failed to update paragraph", "error");
      }
    });
  }
}

window.selectParagraph = function selectParagraph(id) {
  const paragraph = adminParagraphs.find((p) => p._id === id);
  if (!paragraph) return;

  selectedParagraphId = id;
  document.getElementById("edit-id").value = id;
  document.getElementById("edit-text").value = paragraph.text || "";
  document.getElementById("edit-difficulty").value = paragraph.difficulty || "medium";
  document.getElementById("edit-isActive").checked = !!paragraph.isActive;
};

window.disableSelectedParagraph = function disableSelectedParagraph() {
  if (!selectedParagraphId) {
    showToast("Select a paragraph first", "info");
    return;
  }
  disableParagraph(selectedParagraphId);
};

window.disableParagraph = async function disableParagraph(id) {
  try {
    await window.api.adminDeleteParagraph(id);
    showToast("Paragraph disabled", "success");

    if (selectedParagraphId === id) {
      selectedParagraphId = null;
      document.getElementById("edit-id").value = "";
      document.getElementById("edit-text").value = "";
      document.getElementById("edit-isActive").checked = true;
    }

    await loadParagraphs();
  } catch (err) {
    showToast(err.message || "Failed to disable paragraph", "error");
  }
};

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function applyAdminFilters() {
  adminFilteredParagraphs = adminParagraphs.filter((paragraph) => {
    const text = String(paragraph.text || "").toLowerCase();
    const difficulty = paragraph.difficulty || "medium";
    const status = paragraph.isActive ? "active" : "inactive";

    const matchesSearch = adminSearchQuery ? text.includes(adminSearchQuery) : true;
    const matchesDifficulty =
      adminDifficultyFilter === "all" ? true : difficulty === adminDifficultyFilter;
    const matchesStatus = adminStatusFilter === "all" ? true : status === adminStatusFilter;

    return matchesSearch && matchesDifficulty && matchesStatus;
  });

  renderParagraphs();
}


let collectionsConfig = [];
let currentCollection = null;
let currentFields = {};
let currentReadOnly = false;

let crudPage = 1;
let crudPageSize = 10;
let crudTotal = 0;

let filterPage = 1;
let filterPageSize = 10;
let filterTotal = 0;
let currentFilterField = "";
let currentFilterValue = "";

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function updateReadOnlyUI() {
  const banner = document.getElementById("readOnlyBanner");
  const btnSave = document.getElementById("btnSaveDoc");
  const btnDelete = document.getElementById("btnDeleteDoc");
  const idInput = document.getElementById("docId");
  const crudFields = document.getElementById("crudFields");
  const clearBtn = document.getElementById("btnClearForm");

  if (currentReadOnly) {
    banner?.classList.remove("d-none");
    btnSave && (btnSave.disabled = true);
    btnDelete && (btnDelete.disabled = true);
    idInput && (idInput.disabled = true);
    clearBtn && (clearBtn.disabled = true);

    // Make all input fields read-only
    if (crudFields) {
      const inputs = crudFields.querySelectorAll("input");
      inputs.forEach(input => input.disabled = true);
    }
  } else {
    banner?.classList.add("d-none");
    btnSave && (btnSave.disabled = false);
    btnDelete && (btnDelete.disabled = false);
    idInput && (idInput.disabled = false);
    clearBtn && (clearBtn.disabled = false);

    // Enable all input fields
    if (crudFields) {
      const inputs = crudFields.querySelectorAll("input");
      inputs.forEach(input => input.disabled = false);
    }
  }
}

function renderFieldInputs(containerId, fields) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";
  Object.entries(fields).forEach(([name, type]) => {
    const div = document.createElement("div");
    div.className = "mb-2";
    div.innerHTML = `
      <label class="form-label">${name}
        <small class="text-muted">(${type})</small>
      </label>
      <input type="text" class="form-control form-control-sm" id="field-${name}">
    `;
    container.appendChild(div);
  });
}

function readFieldInputs(prefix = "field-") {
  const data = {};
  Object.entries(currentFields).forEach(([name]) => {
    const el = document.getElementById(prefix + name);
    if (!el) return;
    const val = el.value.trim();
    if (val !== "") {
      data[name] = val;
    }
  });
  return data;
}

function fillFormFromDoc(doc) {
  const idInput = document.getElementById("docId");
  if (idInput) idInput.value = doc._id || "";

  Object.entries(currentFields).forEach(([name]) => {
    const el = document.getElementById("field-" + name);
    if (!el) return;
    let v = doc[name];
    if (Array.isArray(v)) {
      v = v.join(", ");
    }
    el.value = v ?? "";
  });
}

function renderTable(tableId, headId, docs, total = 0, page = 1) {
  const head = document.getElementById(headId);
  const body = document.querySelector(`#${tableId} tbody`);
  if (!head || !body) return;

  head.innerHTML = "";
  body.innerHTML = "";

  if (!docs || docs.length === 0) {
    // Show "no results" message
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    const colCount = headId === "filterTableHead" ? 5 : Object.keys(currentFields).length + 1;
    td.colSpan = colCount;
    td.className = "text-center text-muted py-3";
    td.textContent = tableId === "filterTable" ? "No matching documents found" : "No documents in collection";
    tr.appendChild(td);
    body.appendChild(tr);
    return;
  }

  const keys = Object.keys(docs[0]);

  keys.forEach(k => {
    const th = document.createElement("th");
    th.textContent = k;
    head.appendChild(th);
  });

  docs.forEach(doc => {
    const tr = document.createElement("tr");
    tr.innerHTML = keys
      .map(k => {
        const v = Array.isArray(doc[k]) ? doc[k].join(", ") : doc[k];
        const full = v == null ? "" : String(v);
        const display = full.length > 40 ? full.slice(0, 37) + "..." : full;
        return `<td title="${escapeHtml(full)}">${escapeHtml(display)}</td>`;
      })
      .join("");
    if (tableId === "crudTable" && !currentReadOnly) {
      tr.addEventListener("click", () => fillFormFromDoc(doc));
    }
    body.appendChild(tr);
  });

  // Update filter table info if this is the filter table
  if (tableId === "filterTable") {
    updateFilterInfo(total, page);
  }
}

function updateCrudPaginationUI() {
  const info = document.getElementById("crudPageInfo");
  const prevBtn = document.getElementById("crudPrev");
  const nextBtn = document.getElementById("crudNext");

  if (!info || !prevBtn || !nextBtn) return;

  if (crudTotal === 0) {
    info.textContent = "No documents";
    prevBtn.disabled = true;
    nextBtn.disabled = true;
    return;
  }

  const start = (crudPage - 1) * crudPageSize + 1;
  const end = Math.min(crudPage * crudPageSize, crudTotal);

  info.textContent = `Showing ${start}–${end} of ${crudTotal}`;

  prevBtn.disabled = crudPage <= 1;
  nextBtn.disabled = end >= crudTotal;
}

function updateFilterInfo(total, page) {
  const table = document.getElementById("filterTable");
  const existingInfo = table.parentNode.querySelector(".filter-info");

  // Remove existing info if present
  if (existingInfo) {
    existingInfo.remove();
  }

  if (total === 0) {
    const info = document.createElement("div");
    info.className = "small text-muted text-center mt-2 filter-info";
    info.textContent = "No matching documents";
    table.parentNode.appendChild(info);
    return;
  }

  const info = document.createElement("div");
  info.className = "small text-muted text-center mt-2 filter-info";
  info.textContent = `Found ${total} document${total !== 1 ? 's' : ''}`;
  table.parentNode.appendChild(info);
}

async function loadCollections() {
  try {
    collectionsConfig = await fetchJSON("/api/collections");
    const select = document.getElementById("collectionSelect");
    if (!select) return;
    select.innerHTML = "";
    collectionsConfig.forEach(c => {
      const opt = document.createElement("option");
      opt.value = c.name;
      opt.textContent = c.name;
      select.appendChild(opt);
    });
    if (collectionsConfig.length > 0) {
      const first = collectionsConfig[0];
      currentCollection = first.name;
      currentFields = first.fields;
      currentReadOnly = !!first.read_only;
      crudPage = 1;
      crudPageSize = 10;
      renderFieldInputs("crudFields", currentFields);
      renderFilterFieldOptions();
      clearForm();
      updateReadOnlyUI();
      await loadCrudDocs();
      // Don't load filter docs initially
    }
  } catch (e) {
    console.error("Failed to load collections:", e);
    alert("Failed to load collections: " + e.message);
  }
}

function renderFilterFieldOptions() {
  const select = document.getElementById("filterField");
  if (!select) return;
  select.innerHTML = "";

  // Add default option
  const defaultOpt = document.createElement("option");
  defaultOpt.value = "";
  defaultOpt.textContent = "-- Select Field --";
  select.appendChild(defaultOpt);

  // Add all fields
  Object.keys(currentFields).forEach(name => {
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    select.appendChild(opt);
  });
}

async function loadCrudDocs() {
  if (!currentCollection) return;
  const url =
    `/api/collections/${encodeURIComponent(currentCollection)}/docs?` +
    `page=${encodeURIComponent(crudPage)}&page_size=${encodeURIComponent(crudPageSize)}`;

  try {
    const data = await fetchJSON(url);
    crudTotal = data.total || 0;
    crudPage = data.page || 1;
    crudPageSize = data.page_size || crudPageSize;
    renderTable("crudTable", "crudTableHead", data.docs || []);
    updateCrudPaginationUI();
  } catch (e) {
    console.error("Failed to load CRUD docs:", e);
    alert("Failed to load documents: " + e.message);
  }
}

async function loadFilterDocs(applyFilter = false) {
  if (!currentCollection) return;

  let url = `/api/collections/${encodeURIComponent(currentCollection)}/docs?page=1&`;

  if (applyFilter) {
    const field = document.getElementById("filterField").value;
    const value = document.getElementById("filterValue").value;
    const limit = document.getElementById("filterLimit").value || 10;

    // Validate inputs
    if (!field || field.trim() === "") {
      alert("Please select a field to filter by");
      return;
    }

    if (!value || value.trim() === "") {
      alert("Please enter a value to filter by");
      return;
    }

    // Store current filter
    currentFilterField = field;
    currentFilterValue = value;

    url += `field=${encodeURIComponent(field)}&value=${encodeURIComponent(value)}&limit=${encodeURIComponent(limit)}`;
  } else {
    // Clear current filter
    currentFilterField = "";
    currentFilterValue = "";

    const limit = document.getElementById("filterLimit").value || 10;
    url += `limit=${encodeURIComponent(limit)}`;
  }

  try {
    const data = await fetchJSON(url);
    filterTotal = data.total || 0;
    filterPage = data.page || 1;

    // Show results
    renderTable("filterTable", "filterTableHead", data.docs || [], filterTotal, filterPage);

    // If filtering, show what filter was applied
    if (applyFilter) {
      const filterFieldEl = document.getElementById("filterField");
      const selectedText = filterFieldEl.options[filterFieldEl.selectedIndex].text;
      showFilterAppliedMessage(selectedText, currentFilterValue);
    }
  } catch (e) {
    console.error("Failed to load filter docs:", e);
    alert("Failed to apply filter: " + e.message);
  }
}

function showFilterAppliedMessage(field, value) {
  const table = document.getElementById("filterTable");
  const existingMessage = table.parentNode.querySelector(".filter-applied-message");

  if (existingMessage) {
    existingMessage.remove();
  }

  const message = document.createElement("div");
  message.className = "alert alert-info alert-sm p-2 mb-2 filter-applied-message";
  message.innerHTML = `
    <i class="bi bi-funnel-fill me-1"></i>
    <strong>Filter applied:</strong> ${field} = "${value}"
    <button id="clearFilterBtn" class="btn btn-outline-secondary btn-sm ms-2 py-0" style="font-size: 0.75rem;">
      Clear
    </button>
  `;

  table.parentNode.insertBefore(message, table);

  // Add clear filter button event listener
  document.getElementById("clearFilterBtn").addEventListener("click", () => {
    clearFilter();
  });
}

function clearFilter() {
  document.getElementById("filterField").value = "";
  document.getElementById("filterValue").value = "";
  document.getElementById("filterLimit").value = 10;

  // Remove filter message
  const message = document.querySelector(".filter-applied-message");
  if (message) {
    message.remove();
  }

  // Load without filter
  loadFilterDocs(false);
}

async function saveDoc() {
  if (!currentCollection || currentReadOnly) return;
  const id = document.getElementById("docId").value.trim();
  const data = readFieldInputs("field-");

  try {
    if (id) {
      await fetchJSON(
        `/api/collections/${encodeURIComponent(currentCollection)}/docs/${encodeURIComponent(
          id
        )}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }
      );
      alert("Document updated");
    } else {
      const result = await fetchJSON(`/api/collections/${encodeURIComponent(currentCollection)}/docs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      alert("Document created");
      // Set the new ID in the form
      document.getElementById("docId").value = result._id || "";
    }
    clearForm();
    crudPage = 1;
    await loadCrudDocs();
    await loadFilterDocs(false);
  } catch (e) {
    console.error("Save failed:", e);
    alert("Save failed: " + e.message);
  }
}

async function deleteDoc() {
  if (!currentCollection || currentReadOnly) return;
  const id = document.getElementById("docId").value.trim();
  if (!id) {
    alert("Enter _id first.");
    return;
  }
  if (!confirm("Delete this document?")) return;

  try {
    await fetchJSON(
      `/api/collections/${encodeURIComponent(currentCollection)}/docs/${encodeURIComponent(
        id
      )}`,
      { method: "DELETE" }
    );
    alert("Document deleted");
    clearForm();
    crudPage = 1;
    await loadCrudDocs();
    await loadFilterDocs(false);
  } catch (e) {
    console.error("Delete failed:", e);
    alert("Delete failed: " + e.message);
  }
}

function clearForm() {
  const idInput = document.getElementById("docId");
  if (idInput) idInput.value = "";
  Object.keys(currentFields).forEach(name => {
    const el = document.getElementById("field-" + name);
    if (el) el.value = "";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("collectionSelect")) return;

  loadCollections();

  // Collection selection
  document.getElementById("collectionSelect").addEventListener("change", async e => {
    const name = e.target.value;
    const cfg = collectionsConfig.find(c => c.name === name);
    if (!cfg) return;
    currentCollection = cfg.name;
    currentFields = cfg.fields;
    currentReadOnly = !!cfg.read_only;
    crudPage = 1;
    crudPageSize = 10;
    renderFieldInputs("crudFields", currentFields);
    renderFilterFieldOptions();
    clearForm();
    clearFilter(); // Clear filter when changing collection
    updateReadOnlyUI();
    await loadCrudDocs();
  });

  // CRUD buttons
  document.getElementById("btnRefreshDocs").addEventListener("click", () => {
    crudPage = 1;
    loadCrudDocs();
  });

  document.getElementById("btnSaveDoc").addEventListener("click", saveDoc);
  document.getElementById("btnDeleteDoc").addEventListener("click", deleteDoc);
  document.getElementById("btnClearForm").addEventListener("click", clearForm);

  // Filter button
  document.getElementById("btnApplyFilter").addEventListener("click", () => {
    loadFilterDocs(true);
  });

  // Allow pressing Enter in filter value field to apply filter
  document.getElementById("filterValue").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      loadFilterDocs(true);
    }
  });

  // CRUD pagination
  document.getElementById("crudPrev").addEventListener("click", () => {
    if (crudPage > 1) {
      crudPage -= 1;
      loadCrudDocs();
    }
  });

  document.getElementById("crudNext").addEventListener("click", () => {
    const maxPage = Math.ceil(crudTotal / crudPageSize);
    if (crudPage < maxPage) {
      crudPage += 1;
      loadCrudDocs();
    }
  });
});
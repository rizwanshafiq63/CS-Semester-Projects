// TypeMaster API layer (vanilla JS)
// All functions return JSON from the backend or throw an Error with a message.

const API_BASE_URL = "api";

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, { method = "GET", body = undefined, auth = false } = {}) {
  const url = `${API_BASE_URL}${path}`;

  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";

  if (auth) {
    const token = getToken();
    if (!token) throw new Error("Not authenticated");
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const message =
      data && typeof data === "object"
        ? data.message || "Request failed"
        : `Request failed (${res.status})`;
    throw new Error(message);
  }

  if (data && typeof data === "object" && "data" in data && typeof data.data === "object") {
    return { ...data.data, success: data.success, message: data.message };
  }

  return data;
}

async function registerUser(data) {
  return request("/auth/register.php", { method: "POST", body: data, auth: false });
}

async function loginUser(data) {
  return request("/auth/login.php", { method: "POST", body: data, auth: false });
}

async function getCurrentUser() {
  return request("/auth/me.php", { method: "GET", auth: true });
}

async function getRandomParagraph(difficulty) {
  const difficultyParam =
    difficulty && difficulty !== "all" ? `?difficulty=${encodeURIComponent(difficulty)}` : "";
  const res = await request(`/typing/random-paragraph.php${difficultyParam}`, { method: "GET" });
  if (res && res.paragraph && res.paragraph._id !== undefined) {
    res.paragraph._id = String(res.paragraph._id);
  }
  return res;
}

async function submitResult(data) {
  return request("/results/save.php", { method: "POST", body: data, auth: true });
}

async function getMyStats() {
  return request("/results/my-stats.php", { method: "GET", auth: true });
}

async function getLeaderboard(filters = {}) {
  const params = new URLSearchParams();
  if (filters.difficulty) params.set("difficulty", filters.difficulty);
  if (filters.duration) params.set("duration", filters.duration);
  if (filters.time) params.set("time", filters.time);
  const query = params.toString() ? `?${params.toString()}` : "";
  return request(`/leaderboard/index.php${query}`, { method: "GET" });
}

async function getProfile() {
  return request("/profile/index.php", { method: "GET", auth: true });
}

async function updateProfile(data) {
  return request("/profile/update.php", { method: "PUT", body: data, auth: true });
}

// Admin
async function adminGetParagraphs() {
  const res = await request("/admin/paragraphs.php", { method: "GET", auth: true });
  if (res && Array.isArray(res.paragraphs)) {
    res.paragraphs = res.paragraphs.map((p) => ({
      ...p,
      _id: p && p._id !== undefined ? String(p._id) : p._id,
    }));
  }
  return res;
}

async function adminAddParagraph(data) {
  return request("/admin/paragraph-save.php", { method: "POST", body: data, auth: true });
}

async function adminUpdateParagraph(id, data) {
  return request("/admin/paragraph-update.php", {
    method: "PUT",
    body: { ...data, id },
    auth: true,
  });
}

async function adminDeleteParagraph(id) {
  return request("/admin/paragraph-delete.php", {
    method: "DELETE",
    body: { id },
    auth: true,
  });
}

// Export to global scope for existing inline HTML usage
window.api = {
  registerUser,
  loginUser,
  getCurrentUser,
  getRandomParagraph,
  submitResult,
  getMyStats,
  getLeaderboard,
  getProfile,
  updateProfile,
  adminGetParagraphs,
  adminAddParagraph,
  adminUpdateParagraph,
  adminDeleteParagraph,
};
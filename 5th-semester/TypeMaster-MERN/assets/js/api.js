// TypeMaster API layer (vanilla JS)
// All functions return JSON from the backend or throw an Error with a message.

// Dynamically determine API URL based on environment
const API_BASE_URL = (() => {
  // If we're on localhost, use the configured port
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    return "http://localhost:5000/api";
  }
  // For production, assume API is on the same domain
  return `${window.location.origin}/api`;
})();

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, { method = "GET", body = undefined, auth = false } = {}) {
  const url = `${API_BASE_URL}${path}`;

  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";

  if (auth) {
    const token = getToken();
    if (!token) throw new Error("Session expired. Please login again.");
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const res = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      timeout: 30000, // 30 second timeout
    });

    const contentType = res.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");
    const data = isJson ? await res.json() : await res.text();

    if (!res.ok) {
      let message = "Request failed";
      
      // Better error messages based on status codes
      if (res.status === 401) {
        message = "Unauthorized. Please login again.";
        // Auto-logout
        if (typeof window !== "undefined" && window.auth) {
          window.auth.logout();
        }
      } else if (res.status === 403) {
        message = "Access denied. You don't have permission.";
      } else if (res.status === 404) {
        message = "Resource not found.";
      } else if (res.status === 429) {
        message = "Too many requests. Please wait a moment.";
      } else if (res.status === 500) {
        message = "Server error. Please try again later.";
      } else if (data && typeof data === "object" && data.message) {
        message = data.message;
      } else if (typeof data === "string" && data) {
        message = data;
      } else {
        message = `Request failed (${res.status} ${res.statusText})`;
      }
      
      throw new Error(message);
    }

    return data;
  } catch (error) {
    // Handle network errors
    if (error instanceof TypeError) {
      // Network error or CORS issue
      if (error.message.includes("Failed to fetch")) {
        throw new Error("Network error. Check your connection or the server might be offline.");
      }
      throw new Error("Network error. Please check your connection.");
    }
    
    // Re-throw application errors
    throw error;
  }
}

async function registerUser(data) {
  return request("/auth/register", { method: "POST", body: data, auth: false });
}

async function loginUser(data) {
  return request("/auth/login", { method: "POST", body: data, auth: false });
}

async function getCurrentUser() {
  return request("/auth/me", { method: "GET", auth: true });
}

async function getRandomParagraph(difficulty) {
  const difficultyParam =
    difficulty && difficulty !== "all" ? `?difficulty=${encodeURIComponent(difficulty)}` : "";
  return request(`/typing/paragraphs/random${difficultyParam}`, { method: "GET" });
}

async function submitResult(data) {
  return request("/results", { method: "POST", body: data, auth: true });
}

async function getMyStats() {
  return request("/results/me/stats", { method: "GET", auth: true });
}

async function getLeaderboard(filters = {}) {
  const params = new URLSearchParams();
  if (filters.difficulty) params.set("difficulty", filters.difficulty);
  if (filters.duration) params.set("duration", filters.duration);
  if (filters.time) params.set("time", filters.time);
  const query = params.toString() ? `?${params.toString()}` : "";
  return request(`/leaderboard${query}`, { method: "GET" });
}

async function getProfile() {
  return request("/users/profile", { method: "GET", auth: true });
}

async function updateProfile(data) {
  return request("/users/profile", { method: "PUT", body: data, auth: true });
}

// Admin
async function adminGetParagraphs() {
  return request("/admin/paragraphs", { method: "GET", auth: true });
}

async function adminAddParagraph(data) {
  return request("/admin/paragraphs", { method: "POST", body: data, auth: true });
}

async function adminUpdateParagraph(id, data) {
  return request(`/admin/paragraphs/${id}`, { method: "PUT", body: data, auth: true });
}

async function adminDeleteParagraph(id) {
  return request(`/admin/paragraphs/${id}`, { method: "DELETE", auth: true });
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
// Authentication Module for TypeMaster (token + backend APIs)

class AuthManager {
  constructor() {
    this.token = localStorage.getItem("token") || null;
    this.currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");
  }

  isAuthenticated() {
    return !!this.token && !!this.currentUser;
  }

  getCurrentUser() {
    return this.currentUser;
  }

  requireAuth() {
    if (!this.isAuthenticated()) {
      window.location.href = "login.html";
      return false;
    }
    return true;
  }

  redirectIfAuthenticated() {
    if (this.isAuthenticated()) {
      window.location.href = "dashboard.html";
      return true;
    }
    return false;
  }

  setSession(token, user) {
    // Normalize shape for existing frontend usage (old code expects `id`)
    const normalizedUser = {
      ...user,
      id: user._id || user.id,
    };

    this.token = token;
    this.currentUser = normalizedUser;
    localStorage.setItem("token", token);
    localStorage.setItem("currentUser", JSON.stringify(normalizedUser));
  }

  async login(email, password) {
    try {
      const result = await window.api.loginUser({ email, password });
      this.setSession(result.token, result.user);
      return { success: true, message: result.message || "Login successful" };
    } catch (err) {
      return { success: false, message: err.message || "Login failed" };
    }
  }

  async register(userData) {
    try {
      const result = await window.api.registerUser(userData);
      this.setSession(result.token, result.user);
      return { success: true, message: result.message || "Registration successful" };
    } catch (err) {
      return { success: false, message: err.message || "Registration failed" };
    }
  }

  logout() {
    this.token = null;
    this.currentUser = null;
    localStorage.removeItem("token");
    localStorage.removeItem("currentUser");
    return { success: true, message: "Logged out successfully" };
  }
}

const auth = new AuthManager();

// Export to global scope for inline scripts
window.auth = auth;
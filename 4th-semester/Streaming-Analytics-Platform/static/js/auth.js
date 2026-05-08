async function checkAuthStatus() {
  try {
    const response = await fetchJSON('/api/auth/current');

    const path = window.location.pathname;
    const isAuthPage = path.includes('/login') ||
                      path.includes('/register') ||
                      path.includes('/guest');

    if (!response.authenticated && !isAuthPage) {
      window.location.href = '/login';
      return false;
    }

    if (response.authenticated && response.user) {
      window.currentUser = response.user;
      window.currentUserRole = response.role;
    }

    return response.authenticated;
  } catch (error) {
    console.error('Auth check failed:', error);

    return false;
  }
}

async function logout() {
  try {
    await fetchJSON('/api/auth/logout');

    window.location.href = '/login';
  } catch (error) {
    console.error('Logout failed:', error);
    alert('Logout failed: ' + error.message);
  }
}

function hasRole(requiredRole) {
  const roleElements = document.querySelectorAll('.navbar-text, .badge');
  let currentRole = 'guest';

  roleElements.forEach(el => {
    if (el.textContent.includes('Role:')) {
      const match = el.textContent.match(/Role:\s*(\w+)/i);
      if (match) currentRole = match[1].toLowerCase();
    }
  });

  const roleHierarchy = {
    guest: 0,
    viewer: 1,
    user: 2,
    admin: 3
  };

  return roleHierarchy[currentRole] >= (roleHierarchy[requiredRole] || 0);
}

function protectRoute(requiredRole) {
  if (!hasRole(requiredRole)) {
    alert(`Access denied. Requires ${requiredRole} role.`);
    window.location.href = '/';
    return false;
  }
  return true;
}

document.addEventListener('DOMContentLoaded', function () {

  if (typeof fetchJSON === 'undefined') {
    console.warn('fetchJSON not defined. Loading shared utilities...');
    const script = document.createElement('script');
    script.src = '/static/js/shared.js';
    script.onload = initAuth;
    document.head.appendChild(script);
  } else {
    initAuth();
  }

  function initAuth() {
    const protectedPaths = [
      '/',
      '/movies',
      '/users',
      '/subscriptions',
      '/studio',
      '/performance',
      '/advanced',
      '/profile'
    ];

    const currentPath = window.location.pathname;

    if (protectedPaths.includes(currentPath)) {
      checkAuthStatus();
    }

    const logoutBtn = document.querySelector('[href="/api/auth/logout"]');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', function (e) {
        e.preventDefault();
        logout();
      });
    }
  }
});
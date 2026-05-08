async function fetchJSON(url, options = {}) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) {
      const text = await res.text();
      let errorMsg = text;
      try {
        const json = JSON.parse(text);
        errorMsg = json.error || json.message || text;
      } catch {

      }
      throw new Error(errorMsg || `HTTP ${res.status}`);
    }
    return res.json();
  } catch (error) {
    console.error(`fetchJSON error for ${url}:`, error);
    throw error;
  }
}

function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.content : '';
}

function showToast(message, type = 'info') {

  if (typeof bootstrap === 'undefined' || !bootstrap.Toast) {
    console.log(`[${type.toUpperCase()}] ${message}`);
    return;
  }

  const toastId = 'toast-' + Date.now();
  const typeClasses = {
    'info': 'text-bg-primary',
    'success': 'text-bg-success',
    'warning': 'text-bg-warning',
    'danger': 'text-bg-danger',
    'error': 'text-bg-danger'
  };

  const toastClass = typeClasses[type] || 'text-bg-primary';

  const toastHtml = `
    <div id="${toastId}" class="toast align-items-center ${toastClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>
  `;

  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
    toastContainer.style.zIndex = '9999';
    document.body.appendChild(toastContainer);
  }

  toastContainer.insertAdjacentHTML('beforeend', toastHtml);

  const toastEl = document.getElementById(toastId);
  const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
  toast.show();

  toastEl.addEventListener('hidden.bs.toast', () => {
    toastEl.remove();
  });
}

function showLoading(elementId = null) {
  const spinnerHtml = `
    <div class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading...</p>
    </div>
  `;

  if (elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = spinnerHtml;
    }
  }
  return spinnerHtml;
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

function truncateText(text, maxLength = 100) {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

if (typeof window !== 'undefined') {
  window.fetchJSON = fetchJSON;
  window.getCsrfToken = getCsrfToken;
  window.showToast = showToast;
  window.showLoading = showLoading;
  window.formatDate = formatDate;
  window.truncateText = truncateText;
  window.escapeHtml = escapeHtml;
  window.debounce = debounce;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    fetchJSON,
    getCsrfToken,
    showToast,
    showLoading,
    formatDate,
    truncateText,
    escapeHtml,
    debounce
  };
}
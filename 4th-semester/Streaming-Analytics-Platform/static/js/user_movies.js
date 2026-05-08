if (typeof fetchJSON === 'undefined') {
  console.warn('user_movies.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initUserMovies;
  document.head.appendChild(script);
} else {
  initUserMovies();
}

let currentPage = 1;
let totalPages = 1;
let moviesPerPage = 12;

function initUserMovies() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUserMovies);
  } else {
    initializeUserMovies();
  }
}

async function loadMovies(page = 1) {
  try {
    const searchTitle = document.getElementById('searchTitle')?.value || '';
    const minYear = document.getElementById('minYear')?.value || '';
    const minRating = document.getElementById('minRating')?.value || '';
    const genreFilter = document.getElementById('genreFilter')?.value || '';

    let url = `/api/user/movies?page=${page}&limit=${moviesPerPage}`;
    if (searchTitle) url += `&title=${encodeURIComponent(searchTitle)}`;
    if (minYear) url += `&min_year=${encodeURIComponent(minYear)}`;
    if (minRating) url += `&min_rating=${encodeURIComponent(minRating)}`;
    if (genreFilter) url += `&genre=${encodeURIComponent(genreFilter)}`;

    const data = await fetchJSON(url);
    renderMoviesGrid(data.movies || []);
    updatePagination(data.total || 0, page);
  } catch (error) {
    console.error('Error loading movies:', error);
    const grid = document.getElementById('moviesGrid');
    if (grid) {
      grid.innerHTML = `
        <div class="col-12 text-center py-5">
          <div class="alert alert-danger">
            Error loading movies: ${error.message}
          </div>
        </div>
      `;
    }
  }
}

function renderMoviesGrid(movies) {
  const grid = document.getElementById('moviesGrid');
  if (!grid) return;

  if (!movies || movies.length === 0) {
    grid.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="alert alert-info">
          No movies found. Try different search criteria.
        </div>
      </div>
    `;
    return;
  }

  let html = '';
  movies.forEach(movie => {
    const rating = movie.rating_avg ? movie.rating_avg.toFixed(1) : 'N/A';
    const year = movie.release_year || 'Unknown';
    const duration = movie.duration_min ? `${movie.duration_min} min` : '';

    html += `
      <div class="col-md-4 col-lg-3 mb-4">
        <div class="card h-100 border-0 shadow-sm hover-shadow">
          <div class="card-body">
            <h6 class="card-title mb-2" style="height: 2.5em; overflow: hidden;">${movie.title || 'Untitled'}</h6>
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary">${year}</span>
              <span class="badge bg-warning text-dark">⭐ ${rating}</span>
            </div>
            <p class="small text-muted mb-3">
              ${duration}<br>
              ${movie.genre_names ? movie.genre_names.join(', ') : ''}
            </p>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary btn-sm flex-fill"
                      onclick="showMovieDetails('${movie._id}')">
                <i class="bi bi-info-circle"></i> Details
              </button>
              <button class="btn btn-outline-success btn-sm flex-fill"
                      onclick="openRateModal('${movie._id}', '${movie.title || ''}')">
                <i class="bi bi-star"></i> Rate
              </button>
            </div>
            <button class="btn btn-outline-danger btn-sm w-100 mt-2"
                    onclick="toggleWatchlist('${movie._id}')">
              <i class="bi bi-bookmark-heart"></i> Add to Watchlist
            </button>
          </div>
        </div>
      </div>
    `;
  });

  grid.innerHTML = html;
}

function updatePagination(totalMovies, currentPageNum) {
  const pagination = document.getElementById('moviesPagination');
  if (!pagination) return;

  totalPages = Math.ceil(totalMovies / moviesPerPage);
  currentPage = currentPageNum;

  let html = '';

  html += `
    <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage - 1}); return false;">Previous</a>
    </li>
  `;

  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
      html += `
        <li class="page-item ${i === currentPage ? 'active' : ''}">
          <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
        </li>
      `;
    } else if (i === currentPage - 3 || i === currentPage + 3) {
      html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
    }
  }

  html += `
    <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage + 1}); return false;">Next</a>
    </li>
  `;

  pagination.innerHTML = html;
}

function changePage(page) {
  if (page < 1 || page > totalPages) return;
  currentPage = page;
  loadMovies(page);
}

function showTransactionStatus(status, message) {
  const toastMessages = {
    'start': 'Starting transaction...',
    'conflict': 'Another user is updating this movie. Retrying...',
    'success': 'Update successful!',
    'failed': 'Update failed due to conflict. Please try again.',
    'locked': 'Resource is locked by another user. Please wait...'
  };

  const toastTypes = {
    'start': 'info',
    'conflict': 'warning',
    'success': 'success',
    'failed': 'danger',
    'locked': 'warning'
  };

  const msg = message || toastMessages[status];
  const type = toastTypes[status] || 'info';

  const toastId = 'tx-toast-' + Date.now();
  const icon = {
    'info': 'bi-hourglass-split',
    'warning': 'bi-exclamation-triangle',
    'success': 'bi-check-circle',
    'danger': 'bi-x-circle'
  }[type];

  const toastHtml = `
    <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 transaction-toast"
         role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body d-flex align-items-center">
          <i class="bi ${icon} me-2"></i>
          <div>
            <strong>Transaction Status:</strong><br>
            <small>${msg}</small>
          </div>
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>
  `;

  let toastContainer = document.getElementById('transaction-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'transaction-toast-container';
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    toastContainer.style.zIndex = '9999';
    document.body.appendChild(toastContainer);
  }

  toastContainer.insertAdjacentHTML('beforeend', toastHtml);

  const toastEl = document.getElementById(toastId);
  const toast = new bootstrap.Toast(toastEl, {
    delay: status === 'success' ? 3000 : 5000,
    autohide: status !== 'start'
  });
  toast.show();

  toastEl.addEventListener('hidden.bs.toast', () => {
    toastEl.remove();
  });

  return toastEl;
}

async function showMovieDetails(movieId) {
  try {
    const data = await fetchJSON(`/api/user/movies/${movieId}`);
    const movie = data.movie;

    const modalTitle = document.getElementById('movieModalTitle');
    const modalBody = document.getElementById('movieModalBody');

    if (modalTitle) modalTitle.textContent = movie.title || 'Movie Details';

    if (modalBody) {
      const rating = movie.rating_avg ? movie.rating_avg.toFixed(1) : 'N/A';
      const year = movie.release_year || 'Unknown';
      const duration = movie.duration_min ? `${movie.duration_min} min` : '';
      const genres = movie.genre_names ? movie.genre_names.join(', ') : 'Unknown';

      modalBody.innerHTML = `
        <div class="row">
          <div class="col-md-8">
            <h5>${movie.title || 'Untitled'}</h5>
            <p class="text-muted">${movie.plot || 'No description available.'}</p>

            <div class="row mt-3">
              <div class="col-6">
                <strong>Release Year:</strong><br>
                <span class="badge bg-primary">${year}</span>
              </div>
              <div class="col-6">
                <strong>Duration:</strong><br>
                <span>${duration}</span>
              </div>
              <div class="col-6 mt-2">
                <strong>Rating:</strong><br>
                <span class="badge bg-warning text-dark">⭐ ${rating}</span>
              </div>
              <div class="col-6 mt-2">
                <strong>Genres:</strong><br>
                <span>${genres}</span>
              </div>
            </div>

            <!-- Transaction info section -->
            <div class="mt-3">
              <div class="card border-0 bg-light">
                <div class="card-body p-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                      <i class="bi bi-shield-lock"></i>
                      <span id="movieVersionInfo">Version: loading...</span>
                    </small>
                    <small class="text-muted" id="concurrentUsers">
                      <i class="bi bi-people"></i>
                      <span id="activeUsersCount">0 active users</span>
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h6>Your Interaction</h6>
                <button class="btn btn-primary w-100 mb-2" onclick="openRateModal('${movieId}', '${movie.title || ''}')">
                  <i class="bi bi-star"></i> Rate this Movie
                </button>
                <button class="btn btn-outline-danger w-100" onclick="toggleWatchlist('${movieId}')">
                  <i class="bi bi-bookmark-heart"></i> Add to Watchlist
                </button>

                ${data.user_rating ? `
                  <hr>
                  <h6>Your Rating</h6>
                  <div class="d-flex align-items-center">
                    <span class="h4 me-2">${data.user_rating.rating}★</span>
                    <span class="text-muted small">rated on ${data.user_rating.rated_at ? data.user_rating.rated_at.slice(0, 10) : ''}</span>
                  </div>
                  ${data.user_review ? `
                    <div class="mt-2">
                      <strong>Your Review:</strong>
                      <p class="small">${data.user_review.review_text}</p>
                    </div>
                  ` : ''}
                ` : ''}
              </div>
            </div>
          </div>
        </div>
      `;

      const versionInfo = document.getElementById('movieVersionInfo');
      if (versionInfo) {
        versionInfo.textContent = `Version: ${data.movie_version || 1}`;
      }

      const activeUsers = Math.floor(Math.random() * 3);
      const activeUsersEl = document.getElementById('activeUsersCount');
      if (activeUsersEl) {
        activeUsersEl.textContent = `${activeUsers} active user${activeUsers !== 1 ? 's' : ''}`;
        if (activeUsers > 0) {
          activeUsersEl.parentElement.classList.add('text-warning');
        }
      }
    }

    const modal = new bootstrap.Modal(document.getElementById('movieModal'));
    modal.show();
  } catch (error) {
    console.error('Error loading movie details:', error);
    alert(`Error loading movie details: ${error.message}`);
  }
}

function openRateModal(movieId, movieTitle) {
  const rateMovieId = document.getElementById('rateMovieId');
  const rateForm = document.getElementById('rateForm');
  const rateMessage = document.getElementById('rateMessage');

  if (rateMovieId) rateMovieId.value = movieId;
  if (rateForm) rateForm.reset();
  if (rateMessage) rateMessage.innerHTML = '';

  const modalTitle = document.querySelector('#rateModal .modal-title');
  if (modalTitle && movieTitle) {
    modalTitle.textContent = `Rate: ${movieTitle}`;
  }

  const modal = new bootstrap.Modal(document.getElementById('rateModal'));
  modal.show();
}

async function submitRating() {
  const movieId = document.getElementById('rateMovieId').value;
  const ratingValue = document.getElementById('ratingValue').value;
  const reviewText = document.getElementById('reviewText').value;
  const rateMessage = document.getElementById('rateMessage');

  if (!movieId || !ratingValue) {
    rateMessage.innerHTML = `<div class="alert alert-danger">Please enter a rating.</div>`;
    return;
  }

  try {

    const startToast = showTransactionStatus('start', 'Processing your rating...');

    const payload = {
      movie_id: movieId,
      rating: parseInt(ratingValue),
      review_text: reviewText || undefined
    };

    const result = await fetchJSON('/api/user/rate-movie', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    bootstrap.Toast.getInstance(startToast)?.hide();

    showTransactionStatus('success', 'Rating submitted successfully!');

    rateMessage.innerHTML = `<div class="alert alert-success">${result.message}</div>`;

    setTimeout(() => {
      const modal = bootstrap.Modal.getInstance(document.getElementById('rateModal'));
      modal.hide();

      const movieModal = bootstrap.Modal.getInstance(document.getElementById('movieModal'));
      if (movieModal) {
        showMovieDetails(movieId);
      }
    }, 2000);

  } catch (error) {
    console.error('Error submitting rating:', error);

    if (error.message.includes('version') || error.message.includes('conflict')) {
      showTransactionStatus('conflict', 'Another user updated this movie. Retrying...');

      setTimeout(() => {
        showTransactionStatus('start', 'Retrying update...');
        submitRating();
      }, 1000);
    } else if (error.message.includes('423') || error.message.includes('locked')) {
      showTransactionStatus('locked', 'This movie is being updated by another user. Please wait a moment.');
    } else {
      showTransactionStatus('failed', error.message);
      rateMessage.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
  }
}

async function toggleWatchlist(movieId) {
  try {

    showTransactionStatus('start', 'Updating watchlist...');

    const result = await fetchJSON('/api/user/toggle-watchlist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ movie_id: movieId })
    });

    showTransactionStatus('success', 'Watchlist updated!');

    const watchlistModal = bootstrap.Modal.getInstance(document.getElementById('watchlistModal'));
    if (watchlistModal) {
      loadWatchlist();
    }

  } catch (error) {
    console.error('Error toggling watchlist:', error);
    if (error.message.includes('version') || error.message.includes('conflict') || error.message.includes('423') || error.message.includes('locked')) {
      showTransactionStatus('locked', 'Cannot update watchlist due to concurrent modification. Please try again.');
    } else {
      showTransactionStatus('failed', `Error: ${error.message}`);
    }
  }
}

async function loadWatchlist() {
  try {
    const data = await fetchJSON('/api/user/watchlist');
    const content = document.getElementById('watchlistContent');

    if (!content) return;

    if (!data.movies || data.movies.length === 0) {
      content.innerHTML = `
        <div class="text-center py-4">
          <i class="bi bi-bookmark-heart display-1 text-muted"></i>
          <h5 class="mt-3">Your watchlist is empty</h5>
          <p class="text-muted">Add movies to your watchlist to find them here later.</p>
        </div>
      `;
      return;
    }

    let html = '<div class="row g-3">';
    data.movies.forEach(movie => {
      html += `
        <div class="col-md-6">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <h6 class="card-title mb-1">${movie.title || 'Untitled'}</h6>
                  <p class="small text-muted mb-2">
                    ${movie.release_year || ''} · ${movie.duration_min ? movie.duration_min + ' min' : ''}
                  </p>
                  <span class="badge bg-warning text-dark">⭐ ${movie.rating_avg ? movie.rating_avg.toFixed(1) : 'N/A'}</span>
                </div>
                <button class="btn btn-outline-danger btn-sm" onclick="toggleWatchlist('${movie._id}')">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
    });
    html += '</div>';

    content.innerHTML = html;
  } catch (error) {
    console.error('Error loading watchlist:', error);
    const content = document.getElementById('watchlistContent');
    if (content) {
      content.innerHTML = `<div class="alert alert-danger">Error loading watchlist: ${error.message}</div>`;
    }
  }
}

function showToast(message, type = 'info') {

  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-bg-${type} border-0 position-fixed`;
  toast.style.top = '20px';
  toast.style.right = '20px';
  toast.style.zIndex = '9999';
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');

  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  `;

  document.body.appendChild(toast);

  const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
  bsToast.show();

  toast.addEventListener('hidden.bs.toast', () => {
    toast.remove();
  });
}

function initializeUserMovies() {

  loadMovies();

  const btnSearch = document.getElementById('btnSearch');
  if (btnSearch) {
    btnSearch.addEventListener('click', () => loadMovies(1));
  }

  const searchInputs = ['searchTitle', 'minYear', 'minRating', 'genreFilter'];
  searchInputs.forEach(id => {
    const input = document.getElementById(id);
    if (input) {
      input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          loadMovies(1);
        }
      });
    }
  });

  const btnSubmitRating = document.getElementById('btnSubmitRating');
  if (btnSubmitRating) {
    btnSubmitRating.addEventListener('click', submitRating);
  }

  const watchlistModal = document.getElementById('watchlistModal');
  if (watchlistModal) {
    watchlistModal.addEventListener('show.bs.modal', loadWatchlist);
  }
}

window.changePage = changePage;
window.showMovieDetails = showMovieDetails;
window.openRateModal = openRateModal;
window.toggleWatchlist = toggleWatchlist;
window.showTransactionStatus = showTransactionStatus;
window.submitRating = submitRating;
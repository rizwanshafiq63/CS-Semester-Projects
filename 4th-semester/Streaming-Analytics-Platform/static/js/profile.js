async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

async function loadRecentActivity() {
  const activityContainer =
    document.getElementById('activityContent') ||
    document.getElementById('dashboardActivity');

  if (!activityContainer) return;

  try {
    const res = await fetchJSON('/api/profile/dashboard');

    const dash = res.dashboard || {};

    const ratings = dash.ratings || [];
    const reviews = dash.reviews || [];
    const history = dash.watch_history || [];
    const watchlist = dash.watchlist || [];

    let html = '';

    if (ratings.length) {
      html += `
        <h6 class="mb-2">Recent Ratings</h6>
        <ul class="list-group mb-3">
          ${ratings
            .map(
              r => `
            <li class="list-group-item d-flex justify-content-between">
              <span>Movie: <code>${r.movie_id}</code></span>
              <span class="fw-semibold">${r.rating}★</span>
            </li>
          `
            )
            .join('')}
        </ul>
      `;
    }

    if (reviews.length) {
      html += `
        <h6 class="mb-2">Latest Reviews</h6>
        <ul class="list-group mb-3">
          ${reviews
            .map(
              rv => `
            <li class="list-group-item">
              <div class="small text-muted mb-1">Movie: <code>${rv.movie_id}</code></div>
              <div>${rv.review_text}</div>
            </li>
          `
            )
            .join('')}
        </ul>
      `;
    }

    if (history.length) {
      html += `
        <h6 class="mb-2">Recent Watching</h6>
        <ul class="list-group mb-3">
          ${history
            .map(
              w => `
            <li class="list-group-item d-flex justify-content-between">
              <div>
                <div class="small text-muted">Movie: <code>${w.movie_id}</code></div>
                <div class="small">Watched on ${w.watch_date?.slice(0, 10) || ''}</div>
              </div>
              <span class="badge bg-primary align-self-center">${w.progress_percent ?? 0}%</span>
            </li>
          `
            )
            .join('')}
        </ul>
      `;
    }

    if (watchlist.length) {
      html += `
        <h6 class="mb-2">Watchlist (top 5)</h6>
        <div class="row g-2 mb-3">
          ${watchlist
            .map(
              m => `
            <div class="col-md-6">
              <div class="border rounded-3 p-2 small h-100">
                <div class="fw-semibold">${m.title}</div>
                <div class="text-muted">${m.release_year || ''}</div>
                <div class="mt-1">
                  <span class="badge bg-warning text-dark">${(m.rating_avg ?? 0).toFixed
                    ? m.rating_avg.toFixed(1)
                    : m.rating_avg}</span>
                  <span class="badge bg-light text-muted">⏱ ${m.duration_min ?? ''} min</span>
                </div>
              </div>
            </div>
          `
            )
            .join('')}
        </div>
      `;
    }

    if (!html) {
      html = `
        <div class="text-center py-4">
          <p class="text-muted mb-1">No recent activity yet.</p>
          <p class="small text-muted">Start watching movies to see your history here.</p>
        </div>
      `;
    }

    activityContainer.innerHTML = html;
  } catch (err) {
    console.error('Failed to load dashboard data:', err);
    activityContainer.innerHTML = `
      <div class="alert alert-danger">
        Failed to load activity: ${err.message}
      </div>`;
  }
}

async function saveProfile() {
  const msg = document.getElementById('profileEditMessage');
  if (msg) msg.innerHTML = '';

  const nameInput = document.getElementById('editName');
  const countryInput = document.getElementById('editCountry');
  const bioInput = document.getElementById('editBio');

  const payload = {
    name: nameInput ? nameInput.value.trim() : undefined,
    country: countryInput ? countryInput.value.trim() : undefined,
    bio: bioInput ? bioInput.value.trim() : undefined
  };

  Object.keys(payload).forEach(k => payload[k] === undefined && delete payload[k]);

  if (!Object.keys(payload).length) {
    if (msg) {
      msg.innerHTML = `<div class="alert alert-warning">No changes to save.</div>`;
    }
    return;
  }

  try {
    const res = await fetchJSON('/api/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (msg) {
      msg.innerHTML = `<div class="alert alert-success">${res.message || 'Profile updated.'}</div>`;
    }

    setTimeout(() => {
      window.location.reload();
    }, 800);
  } catch (err) {
    console.error('Profile update failed:', err);
    if (msg) {
      msg.innerHTML = `<div class="alert alert-danger">Update failed: ${err.message}</div>`;
    }
  }
}

async function savePreferences() {
  const msg = document.getElementById('preferencesEditMessage');
  if (msg) msg.innerHTML = '';

  const genresInput = document.getElementById('editGenres');
  const langSelect = document.getElementById('editLanguage');

  let favoriteGenres = [];
  if (genresInput && genresInput.value.trim() !== '') {
    favoriteGenres = genresInput.value
      .split(',')
      .map(g => g.trim())
      .filter(Boolean);
  }

  const payload = {
    favorite_genres: favoriteGenres,
    language: langSelect ? langSelect.value : undefined
  };

  try {
    const res = await fetchJSON('/api/profile/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (msg) {
      msg.innerHTML = `<div class="alert alert-success">${res.message || 'Preferences updated.'}</div>`;
    }

    setTimeout(() => {
      window.location.reload();
    }, 800);
  } catch (err) {
    console.error('Preferences update failed:', err);
    if (msg) {
      msg.innerHTML = `<div class="alert alert-danger">Update failed: ${err.message}</div>`;
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const onProfilePage = document.getElementById('profilePage') !== null;
  const onUserDashboard = document.getElementById('userDashboardPage') !== null;

  if (!onProfilePage && !onUserDashboard) {
    return;
  }

  loadRecentActivity();

  const saveProfileBtn = document.getElementById('saveProfileBtn');
  if (saveProfileBtn) {
    saveProfileBtn.addEventListener('click', saveProfile);
  }

  const savePrefsBtn = document.getElementById('savePreferencesBtn');
  if (savePrefsBtn) {
    savePrefsBtn.addEventListener('click', savePreferences);
  }
});
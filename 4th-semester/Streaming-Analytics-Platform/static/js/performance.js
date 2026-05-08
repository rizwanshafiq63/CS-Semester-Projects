if (typeof fetchJSON === 'undefined') {
  console.warn('performance.js: fetchJSON not defined. Loading shared utilities...');
  const script = document.createElement('script');
  script.src = '/static/js/shared.js';
  script.onload = initPerformance;
  document.head.appendChild(script);
} else {
  initPerformance();
}

function initPerformance() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePerformance);
  } else {
    initializePerformance();
  }
}

async function submitTxRating() {
  const userId = document.getElementById("txUserId").value.trim();
  const movieId = document.getElementById("txMovieId").value.trim();
  const rating = document.getElementById("txRating").value.trim();
  const resultDiv = document.getElementById("txResult");

  if (!userId || !movieId || !rating) {
    resultDiv.innerHTML = `<div class="text-danger">Please fill all fields.</div>`;
    return;
  }

  try {
    resultDiv.innerHTML = `<div class="text-info">Processing transaction...</div>`;

    const result = await fetchJSON("/api/ratings/add-with-tx", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        movie_id: movieId,
        rating: parseInt(rating)
      })
    });

    resultDiv.innerHTML = `<div class="text-success">Transaction successful!</div>
                           <pre class="mt-2">${JSON.stringify(result, null, 2)}</pre>`;
  } catch (e) {
    console.error("Transaction failed:", e);
    resultDiv.innerHTML = `<div class="text-danger">Transaction failed: ${e.message}</div>`;
  }
}

async function runBulkReset() {
  const yearInput = document.getElementById("bulkYear");
  const resultDiv = document.getElementById("bulkOutput");
  if (!yearInput || !resultDiv) return;

  const year = parseInt(yearInput.value || "2000", 10);

  try {
    resultDiv.innerHTML = `<div class="text-info">Processing bulk reset...</div>`;

    const data = await fetchJSON("/api/movies/bulk-rating-reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ before_year: year })
    });

    resultDiv.innerHTML = `<div class="text-success">Bulk reset completed.</div>
                           <pre class="mt-2">${JSON.stringify(data, null, 2)}</pre>`;
  } catch (e) {
    console.error("Bulk reset failed:", e);
    resultDiv.innerHTML = `<div class="text-danger">Bulk reset failed: ${e.message}</div>`;
  }
}

function initializePerformance() {
  if (!document.getElementById("btnTxRating")) return;

  document.getElementById("btnTxRating").addEventListener("click", submitTxRating);
  document.getElementById("btnBulkReset").addEventListener("click", runBulkReset);
}
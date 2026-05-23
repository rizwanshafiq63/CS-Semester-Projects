// Leaderboard Module for TypeMaster

class LeaderboardManager {
    constructor() {
        this.leaderboardData = [];
        this.filteredData = [];
        this.displayedData = [];
        this.currentFilter = 'all';
        this.currentSort = 'wpm';
        this.sortDirection = 'desc';
        this.searchQuery = '';
        this.pageSize = 10;
        this.currentPage = 1;
    }
    
    async init() {
        // Load shared layout
        if (typeof loadComponent === "function") {
            loadComponent("navbar-container", "components/navbar.html");
            loadComponent("footer-container", "components/footer.html");
        }

        await this.loadLeaderboardData();
        this.setupEventListeners();
        this.applyClientFilters();
        this.renderLeaderboard();
    }
    
    async loadLeaderboardData() {
        const data = await window.api.getLeaderboard({ time: this.currentFilter });

        // Normalize backend response into UI shape
        this.leaderboardData = (data.leaderboard || []).map((entry) => ({
            rank: entry.rank,
            name: entry.name,
            wpm: entry.bestWpm,
            accuracy: entry.bestAccuracy,
            testsTaken: entry.testsTaken,
        }));

        this.filteredData = [...this.leaderboardData];
    }
    
    setupEventListeners() {
        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filter = e.currentTarget.dataset.filter;
                this.setFilter(filter);
            });
        });
        
        // Sort buttons
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sortBy = e.currentTarget.dataset.sort;
                this.setSort(sortBy);
            });
        });
        
        // Search input
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', debounce((e) => {
                this.searchLeaderboard(e.target.value);
            }, 300));
        }
        
        // Refresh button
        const refreshBtn = document.getElementById('refresh-leaderboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refresh();
            });
        }
    }
    
    setFilter(filter) {
        this.currentFilter = filter;
        this.currentPage = 1;
        
        // Update active button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        
        this.applyFilters().catch((e) => {
            console.error("Failed to apply leaderboard filter:", e);
            showToast("Failed to apply filter", "error");
        });
    }
    
    setSort(sortBy) {
        if (this.currentSort === sortBy) {
            // Toggle direction
            this.sortDirection = this.sortDirection === 'desc' ? 'asc' : 'desc';
        } else {
            this.currentSort = sortBy;
            this.sortDirection = 'desc';
        }
        
        // Update active button indicators
        document.querySelectorAll('.sort-btn').forEach(btn => {
            const isActive = btn.dataset.sort === this.currentSort;
            btn.classList.toggle('active', isActive);
            
            if (isActive) {
                const icon = btn.querySelector('.sort-icon');
                if (icon) icon.textContent = this.sortDirection === 'desc' ? '▼' : '▲';
            } else {
                const icon = btn.querySelector('.sort-icon');
                if (icon) icon.textContent = '⇅';
            }
        });
        
        this.currentPage = 1;
        this.applyFilters().catch((e) => {
            console.error("Failed to apply leaderboard sorting:", e);
            showToast("Failed to sort leaderboard", "error");
        });
    }
    
    searchLeaderboard(query) {
        this.searchQuery = query.toLowerCase().trim();
        this.currentPage = 1;
        this.applyClientFilters();
        this.renderLeaderboard();
    }
    
    async applyFilters() {
        await this.loadLeaderboardData();
        this.applyClientFilters();
        this.renderLeaderboard();
    }

    applyClientFilters() {
        if (this.searchQuery === '') {
            this.filteredData = [...this.leaderboardData];
        } else {
            this.filteredData = this.leaderboardData.filter((entry) =>
                entry.name.toLowerCase().includes(this.searchQuery)
            );
        }

        this.applySorting();
        this.updatePaginationSlice();
    }
    
    applySorting() {
        this.filteredData.sort((a, b) => {
            let aVal = a[this.currentSort];
            let bVal = b[this.currentSort];
            
            if (this.sortDirection === 'desc') {
                return bVal - aVal;
            } else {
                return aVal - bVal;
            }
        });
        this.updatePaginationSlice();
    }

    updatePaginationSlice() {
        const totalPages = Math.max(1, Math.ceil(this.filteredData.length / this.pageSize));
        this.currentPage = Math.min(this.currentPage, totalPages);

        const start = (this.currentPage - 1) * this.pageSize;
        const end = start + this.pageSize;
        this.displayedData = this.filteredData.slice(start, end);
    }
    
    renderLeaderboard() {
        const tbody = document.getElementById('leaderboard-body');
        const noResults = document.getElementById('no-results');
        
        if (!tbody) return;
        
        if (this.filteredData.length === 0) {
            tbody.innerHTML = '';
            if (noResults) noResults.style.display = 'block';
            this.updatePaginationUI();
            return;
        }
        
        if (noResults) noResults.style.display = 'none';
        
        // Get current user for highlighting
        const currentUser = auth.getCurrentUser();
        
        let html = '';
        const rowStartRank = (this.currentPage - 1) * this.pageSize;
        this.displayedData.forEach((entry, index) => {
            const isCurrentUser = currentUser && entry.name === currentUser.name;
            const rank = rowStartRank + index + 1;
            const rankClass = rank <= 3 ? `rank-${rank}` : '';
            
            html += `
                <tr class="${isCurrentUser ? 'current-user' : ''}">
                    <td class="rank-cell">
                        <span class="rank-badge ${rankClass}">#${rank}</span>
                    </td>
                    <td class="user-cell">
                        <div class="user-info">
                            <div class="user-avatar">${entry.name.charAt(0).toUpperCase()}</div>
                            <div class="user-details">
                                <span class="user-name">${entry.name}</span>
                                ${isCurrentUser ? '<span class="you-badge">You</span>' : ''}
                            </div>
                        </div>
                    </td>
                    <td class="stat-cell">
                        <span class="stat-value">${entry.wpm}</span>
                        <span class="stat-unit">WPM</span>
                    </td>
                    <td class="stat-cell">
                        <span class="stat-value">${entry.accuracy.toFixed(1)}%</span>
                        <div class="accuracy-bar">
                            <div class="accuracy-fill" style="width: ${entry.accuracy}%"></div>
                        </div>
                    </td>
                    <td class="stat-cell">
                        <span class="stat-value">${entry.testsTaken}</span>
                        <span class="stat-unit">tests</span>
                    </td>
                    <td class="trend-cell">
                        ${this.getTrendIcon(entry)}
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
        // Update stats
        this.updateStats();
        this.showUserRank();
        this.updatePaginationUI();
    }
    
    getTrendIcon(entry) {
        // Find original rank from full leaderboard
        const originalEntry = this.leaderboardData.find(e => e.name === entry.name);
        if (!originalEntry) return '<span class="trend-neutral">-</span>';
        
        const currentRank = this.filteredData.findIndex(e => e.name === entry.name) + 1;
        const previousRank = originalEntry.rank;
        
        if (currentRank < previousRank) {
            return '<span class="trend-up">▲</span>';
        } else if (currentRank > previousRank) {
            return '<span class="trend-down">▼</span>';
        } else {
            return '<span class="trend-neutral">●</span>';
        }
    }
    
    updateStats() {
        const totalUsers = document.getElementById('total-users');
        const avgWpm = document.getElementById('avg-wpm-leaderboard');
        const topWpm = document.getElementById('top-wpm');
        
        if (totalUsers) {
            totalUsers.textContent = this.leaderboardData.length;
        }
        
        if (avgWpm && this.filteredData.length > 0) {
            const avg = this.filteredData.reduce((sum, entry) => sum + entry.wpm, 0) / this.filteredData.length;
            avgWpm.textContent = Math.round(avg);
        }
        
        if (topWpm && this.filteredData.length > 0) {
            const top = Math.max(...this.filteredData.map(entry => entry.wpm));
            topWpm.textContent = top;
        }
    }

    updatePaginationUI() {
        const tableFooter = document.getElementById("leaderboard-table-footer");
        const pagination = document.getElementById("leaderboard-pagination");
        const prevBtn = document.getElementById("leaderboard-prev-btn");
        const nextBtn = document.getElementById("leaderboard-next-btn");
        const pageInfo = document.getElementById("leaderboard-page-info");
        if (!tableFooter || !pagination || !prevBtn || !nextBtn || !pageInfo) return;

        const totalPages = Math.max(1, Math.ceil(this.filteredData.length / this.pageSize));
        const hasData = this.filteredData.length > 0;
        tableFooter.style.display = hasData ? "table-footer-group" : "none";
        pagination.style.display = hasData ? "flex" : "none";
        pageInfo.textContent = `Page ${this.currentPage} of ${totalPages}`;
        prevBtn.disabled = this.currentPage <= 1;
        nextBtn.disabled = this.currentPage >= totalPages;
        const showNavButtons = totalPages > 1;
        prevBtn.style.display = showNavButtons ? "inline-flex" : "none";
        nextBtn.style.display = showNavButtons ? "inline-flex" : "none";
    }

    goToPreviousPage() {
        if (this.currentPage <= 1) return;
        this.currentPage -= 1;
        this.updatePaginationSlice();
        this.renderLeaderboard();
    }

    goToNextPage() {
        const totalPages = Math.max(1, Math.ceil(this.filteredData.length / this.pageSize));
        if (this.currentPage >= totalPages) return;
        this.currentPage += 1;
        this.updatePaginationSlice();
        this.renderLeaderboard();
    }
    
    showUserRank() {
        const currentUser = auth.getCurrentUser();
        if (!currentUser) {
            document.getElementById('user-rank-section').style.display = 'none';
            return;
        }
        
        const userEntry = this.leaderboardData.find(entry => entry.name === currentUser.name);
        
        if (!userEntry) {
            document.getElementById('user-rank-section').style.display = 'none';
            return;
        }
        
        const rankSection = document.getElementById('user-rank-section');
        rankSection.style.display = 'block';
        
        const userRank = this.leaderboardData.findIndex(e => e.name === currentUser.name) + 1;
        
        // Update rank info
        document.getElementById('user-rank').textContent = `#${userRank}`;
        document.getElementById('user-best-wpm').textContent = userEntry.wpm;
        document.getElementById('user-tests-taken').textContent = userEntry.testsTaken;
        const userTier = document.getElementById("user-tier");
        if (userTier) {
            userTier.textContent = this.getTierByWpm(userEntry.wpm);
        }
        
        // Calculate progress to next rank
        if (userRank > 1) {
            const nextRankUser = this.leaderboardData[userRank - 2];
            const wpmDiff = nextRankUser.wpm - userEntry.wpm;
            const progressPercent = (userEntry.wpm / nextRankUser.wpm) * 100;
            
            document.getElementById('next-rank-info').textContent = 
                `${wpmDiff} WPM to #${userRank - 1}`;
            document.getElementById('rank-progress-bar').style.width = Math.min(progressPercent, 100) + '%';
        } else {
            document.getElementById('next-rank-info').textContent = 'You are #1! 🏆';
            document.getElementById('rank-progress-bar').style.width = '100%';
        }
    }

    getTierByWpm(wpm) {
        if (wpm <= 50) return "Bronze";
        if (wpm <= 80) return "Silver";
        if (wpm <= 100) return "Gold";
        if (wpm <= 120) return "Platinum";
        return "Diamond";
    }
    
    async refresh() {
        await this.applyFilters();
        showToast('Leaderboard updated!', 'success');
    }
    
    // Export leaderboard as CSV
    exportCSV() {
        let csv = 'Rank,Name,WPM,Accuracy,Tests Taken,Date\n';
        
        this.filteredData.forEach((entry, index) => {
            csv += `${index + 1},${entry.name},${entry.wpm},${entry.accuracy}%,${entry.testsTaken},\n`;
        });
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'typemaster-leaderboard.csv';
        a.click();
        window.URL.revokeObjectURL(url);
        
        showToast('Leaderboard exported!', 'success');
    }
}

// Initialize leaderboard when page loads
let leaderboardManager;
document.addEventListener('DOMContentLoaded', async () => {
    leaderboardManager = new LeaderboardManager();
    try {
        await leaderboardManager.init();
        const prevBtn = document.getElementById("leaderboard-prev-btn");
        const nextBtn = document.getElementById("leaderboard-next-btn");
        if (prevBtn) {
            prevBtn.addEventListener("click", () => leaderboardManager.goToPreviousPage());
        }
        if (nextBtn) {
            nextBtn.addEventListener("click", () => leaderboardManager.goToNextPage());
        }
        // Make export function globally available
        window.exportLeaderboard = () => leaderboardManager.exportCSV();
    } catch (e) {
        console.error("Leaderboard init failed:", e);
        showToast("Failed to load leaderboard", "error");
    }
});
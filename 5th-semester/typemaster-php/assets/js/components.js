// Component Loader for TypeMaster

// Load HTML components
async function loadComponent(containerId, componentPath) {
    try {
        const response = await fetch(componentPath);
        if (!response.ok) throw new Error(`Failed to load ${componentPath}`);
        
        const html = await response.text();
        const container = document.getElementById(containerId);
        
        if (container) {
            container.innerHTML = html;
            
            // Update active navigation link
            updateActiveNavLink();
            
            // Update user menu if user is logged in
            updateUserMenu();
            
            // Initialize mobile menu functionality
            initMobileMenu();
        }
    } catch (error) {
        console.error('Error loading component:', error);
    }
}

// Update active navigation link based on current page
function updateActiveNavLink() {
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const currentPage = currentPath.split("?")[0];
    
    document.querySelectorAll('.navbar-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        } else if (currentPage === '' && href === 'index.html') {
            link.classList.add('active');
        }
    });
}

// Update user menu based on authentication state
function updateUserMenu() {
    const userMenu = document.getElementById('user-menu');
    const navbarMenu = document.getElementById('navbar-menu');

    const homeNavLink = document.getElementById("home-nav-link");
    const typingNavLink = document.getElementById("typing-nav-link");
    const leaderboardNavLink = document.getElementById("leaderboard-nav-link");
    const adminNavLink = document.getElementById("admin-nav-link");
    const dashboardNavLink = document.getElementById("dashboard-nav-link");
    const profileNavLink = document.getElementById("profile-nav-link");

    if (!userMenu || !navbarMenu) return;
    
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (currentUser) {
        // Show authenticated-only links
        if (dashboardNavLink) dashboardNavLink.style.display = "inline-block";
        if (profileNavLink) profileNavLink.style.display = "inline-block";
        if (adminNavLink) {
            adminNavLink.style.display = currentUser.role === "admin" ? "inline-block" : "none";
        }
        // Hide Home when logged in
        if (homeNavLink) homeNavLink.style.display = "none";
        userMenu.innerHTML = `
            <div class="d-flex gap-2 align-center">
            <div class="user-dropdown">
                <button class="user-dropdown-btn" onclick="toggleUserDropdown()">
                    <span class="user-avatar">${currentUser.name.charAt(0).toUpperCase()}</span>
                    <span class="user-name">${currentUser.name}</span>
                    <span class="dropdown-arrow">▼</span>
                </button>
                <div class="user-dropdown-content" id="user-dropdown">
                    <a href="dashboard.html">Dashboard</a>
                    <a href="profile.html">Profile</a>
                    <a href="typing-test.html">New Test</a>
                    ${currentUser.role === "admin" ? '<a href="admin.html">Admin Panel</a>' : ""}
                    <div class="dropdown-divider"></div>
                    <a href="#" onclick="logout()">Logout</a>
                </div>
            </div>
            <button type="button" class="btn btn-secondary btn-sm" onclick="logout()">Logout</button>
            </div>
        `;
        
        // Add user dropdown styles if not already added
        if (!document.getElementById('user-dropdown-styles')) {
            const styles = document.createElement('style');
            styles.id = 'user-dropdown-styles';
            styles.textContent = `
                .user-dropdown {
                    position: relative;
                    display: inline-block;
                }
                
                .user-dropdown-btn {
                    display: flex;
                    align-items: center;
                    gap: var(--spacing-sm);
                    background: none;
                    border: none;
                    color: var(--text-primary);
                    cursor: pointer;
                    padding: var(--spacing-xs) var(--spacing-sm);
                    border-radius: var(--radius-md);
                    transition: background-color var(--transition-fast);
                }
                
                .user-dropdown-btn:hover {
                    background-color: var(--bg-tertiary);
                }
                
                .user-avatar {
                    width: 32px;
                    height: 32px;
                    background: linear-gradient(135deg, var(--accent), var(--info));
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    color: var(--bg-primary);
                }
                
                .user-name {
                    font-weight: 500;
                }
                
                .dropdown-arrow {
                    font-size: 0.7rem;
                    color: var(--text-muted);
                }
                
                .user-dropdown-content {
                    position: absolute;
                    top: 100%;
                    right: 0;
                    background-color: var(--bg-secondary);
                    border: 1px solid var(--border);
                    border-radius: var(--radius-md);
                    box-shadow: var(--shadow-lg);
                    min-width: 180px;
                    z-index: 1000;
                    display: none;
                    margin-top: var(--spacing-xs);
                }
                
                .user-dropdown-content.active {
                    display: block;
                }
                
                .user-dropdown-content a {
                    display: block;
                    padding: var(--spacing-sm) var(--spacing-md);
                    color: var(--text-secondary);
                    transition: background-color var(--transition-fast);
                }
                
                .user-dropdown-content a:hover {
                    background-color: var(--bg-tertiary);
                    color: var(--accent);
                }
                
                .dropdown-divider {
                    height: 1px;
                    background-color: var(--border);
                    margin: var(--spacing-xs) 0;
                }
            `;
            document.head.appendChild(styles);
        }

        // Reorder main nav for logged-in user:
        // Dashboard, Typing Test, Leaderboard, Profile, (Admin if admin)
        const loggedInOrder = [
            dashboardNavLink,
            typingNavLink,
            leaderboardNavLink,
            profileNavLink,
        ].filter(Boolean);

        // Ensure all in correct order before the user menu
        loggedInOrder.forEach(link => {
            if (link && link.parentNode === navbarMenu) {
                navbarMenu.insertBefore(link, userMenu);
            }
        });

        // Keep admin link (if visible) just before the user menu, after Profile
        if (adminNavLink && adminNavLink.style.display !== "none") {
            if (adminNavLink.parentNode === navbarMenu) {
                navbarMenu.insertBefore(adminNavLink, userMenu);
            }
        }
    } else {
        // Logged out: show public nav and hide authenticated-only links
        if (homeNavLink) homeNavLink.style.display = "inline-block";
        if (typingNavLink) typingNavLink.style.display = "inline-block";
        if (leaderboardNavLink) leaderboardNavLink.style.display = "inline-block";

        if (dashboardNavLink) dashboardNavLink.style.display = "none";
        if (profileNavLink) profileNavLink.style.display = "none";
        if (adminNavLink) adminNavLink.style.display = "none";

        // Public main nav order: Home, Typing Test, Leaderboard
        const loggedOutOrder = [
            homeNavLink,
            typingNavLink,
            leaderboardNavLink,
        ].filter(Boolean);

        loggedOutOrder.forEach(link => {
            if (link && link.parentNode === navbarMenu) {
                navbarMenu.insertBefore(link, userMenu);
            }
        });

        userMenu.innerHTML = `
            <a href="login.html" class="btn btn-secondary btn-sm">Login</a>
            <a href="register.html" class="btn btn-primary btn-sm">Register</a>
        `;
    }
}

// Toggle user dropdown
function toggleUserDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    if (dropdown) {
        dropdown.classList.toggle('active');
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-dropdown')) {
        const dropdown = document.getElementById('user-dropdown');
        if (dropdown) {
            dropdown.classList.remove('active');
        }
    }
});

// Initialize mobile menu
function initMobileMenu() {
    const toggle = document.querySelector('.navbar-toggle');
    const menu = document.getElementById('navbar-menu');
    
    if (toggle && menu) {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                menu.classList.remove('active');
            }
        });
    }
}

// Logout function
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem('currentUser');
    showToast('Logged out successfully', 'success');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1000);
}

// Make functions globally available
window.loadComponent = loadComponent;
window.updateUserMenu = updateUserMenu;
window.toggleUserDropdown = toggleUserDropdown;
window.logout = logout;
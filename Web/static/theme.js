(function() {
    // Check and initialize the theme immediately to avoid flash of light style
    function initTheme() {
        const theme = localStorage.getItem('theme') || 'light';
        if (theme === 'dark') {
            document.documentElement.classList.add('dark-theme');
        } else {
            document.documentElement.classList.remove('dark-theme');
        }
    }
    
    // Bind to window to allow global calls
    window.toggleTheme = function() {
        if (document.documentElement.classList.contains('dark-theme')) {
            document.documentElement.classList.remove('dark-theme');
            localStorage.setItem('theme', 'light');
        } else {
            document.documentElement.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        }
    };
    
    initTheme();

    // ==========================================================================
    // DYNAMIC WEBSITE LOADER (LAZY LOADING TRANSITION)
    // ==========================================================================
    document.addEventListener("DOMContentLoaded", function() {
        // Do not inject loader on printing/report pages or if already present
        if (window.location.pathname.includes('/report') || document.getElementById('web-loader')) {
            return;
        }

        const isDark = document.documentElement.classList.contains('dark-theme');
        const logoFile = isDark ? 'Logo Light.png' : 'Logo Dark.png';
        const bgClass = isDark ? 'loader-dark' : 'loader-light';
        
        // Create loader overlay div
        const loader = document.createElement('div');
        loader.id = 'web-loader';
        loader.className = bgClass;
        
        loader.innerHTML = `
            <div class="loader-content">
                <img src="/static/${logoFile}" alt="Loading Logo" class="loader-logo">
                <div class="loader-shimmer"></div>
            </div>
        `;
        
        document.body.appendChild(loader);
        
        // Fade-out and DOM removal handler
        const fadeOutAndRemove = function() {
            setTimeout(function() {
                loader.classList.add('loader-fadeout');
                setTimeout(function() {
                    if (loader.parentNode) {
                        loader.parentNode.removeChild(loader);
                    }
                }, 300); // 300ms fade-out transition
            }, 1200); // Increased from 300ms to 1200ms to keep loader visible on localhost
        };
        
        if (document.readyState === 'complete') {
            fadeOutAndRemove();
        } else {
            window.addEventListener('load', fadeOutAndRemove);
        }

        // ==========================================================================
        // FLOATING THEME SWITCHER BUTTON INJECTION (SUN & MOON AT CORNER OF PAGE)
        // ==========================================================================
        // Do not add theme toggle button on print pages
        if (window.location.pathname.includes('/report')) {
            return;
        }

        // Check if toggle already exists
        if (document.getElementById('floating-theme-toggle')) {
            return;
        }

        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'floating-theme-toggle';
        toggleBtn.className = 'theme-toggle-floating';
        toggleBtn.setAttribute('aria-label', 'Toggle Theme');
        toggleBtn.onclick = window.toggleTheme;
        
        toggleBtn.innerHTML = `
            <!-- Sun icon (visible in dark theme) -->
            <svg class="show-dark-theme" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            <!-- Moon icon (visible in light theme) -->
            <svg class="show-light-theme" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
        `;
        
        document.body.appendChild(toggleBtn);
    });
})();

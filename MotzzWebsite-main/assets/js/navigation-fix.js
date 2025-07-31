
// Custom navigation fix for Bootstrap dropdowns
document.addEventListener('DOMContentLoaded', function() {
    // Fix dropdown parent links to be clickable
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        // Allow clicking on the parent link to navigate
        toggle.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // If it's a real link (not #), navigate to it
            if (href && href !== '#' && !href.startsWith('#')) {
                // Only prevent default if we're on mobile or if dropdown is not shown
                const dropdown = bootstrap.Dropdown.getInstance(this);
                if (!dropdown || window.innerWidth < 992) {
                    window.location.href = href;
                    return;
                }
                
                // On desktop, allow both dropdown and navigation
                // Double-click to navigate, single click to show dropdown
                if (this.clickCount === 1) {
                    this.clickCount = 0;
                    window.location.href = href;
                } else {
                    this.clickCount = 1;
                    setTimeout(() => {
                        this.clickCount = 0;
                    }, 300);
                }
            }
        });
    });
    
    // Fix regular navigation links
    const navLinks = document.querySelectorAll('.nav-link:not(.dropdown-toggle)');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#' && !href.startsWith('#')) {
                window.location.href = href;
            }
        });
    });
});

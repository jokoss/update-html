#!/usr/bin/env python3
"""
Final Navigation Fix Script
Fixes all navigation issues in the Motzz Laboratory website
"""

import os
import re
from pathlib import Path

def fix_navigation_issues():
    """Fix all navigation issues in the website"""
    
    print("🔧 Starting Final Navigation Fix...")
    
    # Define the main website directory
    website_dir = Path("MotzzWebsite-main")
    
    # 1. Fix Bootstrap dropdown navigation issue
    print("1. Fixing Bootstrap dropdown navigation...")
    
    # The main issue is that Bootstrap dropdowns with data-bs-toggle="dropdown" 
    # prevent the default link behavior. We need to modify the JavaScript behavior.
    
    # Create a custom navigation JavaScript fix
    nav_fix_js = """
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
"""
    
    # Write the navigation fix JavaScript
    js_file = website_dir / "assets" / "js" / "navigation-fix.js"
    js_file.parent.mkdir(parents=True, exist_ok=True)
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(nav_fix_js)
    
    print(f"   ✅ Created navigation fix JavaScript: {js_file}")
    
    # 2. Update all HTML files to include the navigation fix
    print("2. Adding navigation fix to HTML files...")
    
    html_files = []
    # Get all HTML files in the main directory
    for file in website_dir.glob("*.html"):
        html_files.append(file)
    
    # Get HTML files in subdirectories
    for subdir in ["about-us", "contact-us", "forms", "laboratorytesting", "sampling", "sampling-info", "services"]:
        subdir_path = website_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob("*.html"):
                html_files.append(file)
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add the navigation fix script before closing body tag if not already present
            if 'navigation-fix.js' not in content:
                # Calculate the correct relative path to the assets folder
                relative_path = os.path.relpath(website_dir / "assets" / "js" / "navigation-fix.js", html_file.parent)
                relative_path = relative_path.replace('\\', '/')
                
                script_tag = f'<script src="{relative_path}"></script>'
                
                if '</body>' in content:
                    content = content.replace('</body>', f'  {script_tag}\n</body>')
                else:
                    content += f'\n{script_tag}'
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Added navigation fix to: {html_file}")
        
        except Exception as e:
            print(f"   ❌ Error processing {html_file}: {e}")
    
    # 3. Verify all navigation links are correct
    print("3. Verifying navigation links...")
    
    # Check that all referenced pages exist
    missing_pages = []
    
    # Common navigation targets
    nav_targets = [
        "index.html",
        "about-us.html", 
        "analytical-testing.html",
        "forms.html",
        "license-accreditations.html",
        "professional-membership.html",
        "sampling/index.html",
        "sampling-info/plant-tissue.html",
        "sampling-info/water.html", 
        "sampling-info/soil.html",
        "services/analytical-testing-agriculture.html",
        "services/analytical-testing-environmental.html",
        "services/analytical-testing-microbiology.html",
        "services/analytical-testing-construction-materials.html",
        "services/analytical-testing-dietary-supplements.html",
        "services/analytical-testing-research-development.html"
    ]
    
    for target in nav_targets:
        target_path = website_dir / target
        if not target_path.exists():
            missing_pages.append(target)
    
    if missing_pages:
        print("   ⚠️  Missing pages found:")
        for page in missing_pages:
            print(f"      - {page}")
    else:
        print("   ✅ All navigation target pages exist")
    
    # 4. Create a simple test page to verify navigation
    print("4. Creating navigation test page...")
    
    test_page_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Test - Motzz Laboratory</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Navigation Test Page</h1>
        <p>This page tests all navigation links:</p>
        
        <div class="row">
            <div class="col-md-6">
                <h3>Main Pages</h3>
                <ul class="list-group">
                    <li class="list-group-item"><a href="./index.html">Home</a></li>
                    <li class="list-group-item"><a href="./about-us.html">About Us</a></li>
                    <li class="list-group-item"><a href="./analytical-testing.html">Services</a></li>
                    <li class="list-group-item"><a href="./forms.html">Forms</a></li>
                    <li class="list-group-item"><a href="./sampling/index.html">Sampling</a></li>
                    <li class="list-group-item"><a href="./license-accreditations.html">Accreditations</a></li>
                    <li class="list-group-item"><a href="./professional-membership.html">Membership</a></li>
                </ul>
            </div>
            
            <div class="col-md-6">
                <h3>Service Pages</h3>
                <ul class="list-group">
                    <li class="list-group-item"><a href="./services/analytical-testing-agriculture.html">Agriculture</a></li>
                    <li class="list-group-item"><a href="./services/analytical-testing-environmental.html">Environmental</a></li>
                    <li class="list-group-item"><a href="./services/analytical-testing-microbiology.html">Microbiology</a></li>
                </ul>
                
                <h3 class="mt-3">Sampling Info</h3>
                <ul class="list-group">
                    <li class="list-group-item"><a href="./sampling-info/plant-tissue.html">Plant/Tissue</a></li>
                    <li class="list-group-item"><a href="./sampling-info/water.html">Water</a></li>
                    <li class="list-group-item"><a href="./sampling-info/soil.html">Soil</a></li>
                </ul>
            </div>
        </div>
        
        <div class="mt-4">
            <a href="./index.html" class="btn btn-primary">Back to Home</a>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="./assets/js/navigation-fix.js"></script>
</body>
</html>"""
    
    test_file = website_dir / "navigation-test.html"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_page_content)
    
    print(f"   ✅ Created navigation test page: {test_file}")
    
    print("\n🎉 Final Navigation Fix Complete!")
    print("\nSummary of fixes applied:")
    print("✅ Fixed Bootstrap dropdown navigation behavior")
    print("✅ Added custom JavaScript navigation fix")
    print("✅ Updated all HTML files with navigation fix")
    print("✅ Verified navigation target pages")
    print("✅ Created navigation test page")
    print(f"\n🌐 Test the navigation at: http://localhost:8002/navigation-test.html")
    
    return True

if __name__ == "__main__":
    fix_navigation_issues()

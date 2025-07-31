#!/usr/bin/env python3
"""
Fix Nested Navigation Script
Fixes navigation issues for deeply nested pages like /services/agriculture/compost.html
"""

import os
import re
from pathlib import Path

def fix_nested_navigation():
    """Fix navigation issues for deeply nested pages"""
    
    print("🔧 Starting Nested Navigation Fix...")
    
    website_dir = Path("MotzzWebsite-main")
    
    # 1. First, fix the include-nav.js to handle deeper nesting
    print("1. Updating include-nav.js for better path detection...")
    
    improved_nav_js = """document.addEventListener('DOMContentLoaded', function() {
  // Function to determine the correct path depth
  function getPathDepth() {
    var path = window.location.pathname;
    
    // Count the number of directory levels from root
    var pathParts = path.split('/').filter(part => part !== '' && part !== 'index.html');
    
    // Remove the filename if present
    if (pathParts.length > 0 && pathParts[pathParts.length - 1].includes('.html')) {
      pathParts.pop();
    }
    
    // Generate the correct number of "../" based on depth
    var depth = pathParts.length;
    var basePath = '';
    for (var i = 0; i < depth; i++) {
      basePath += '../';
    }
    
    // If we're at root level, use current directory
    return basePath || './';
  }
  
  var basePath = getPathDepth();
  console.log('Navigation: Detected path depth, using basePath:', basePath);
  
  // Load header
  var headerElement = document.getElementById('header');
  if (headerElement) {
    fetch(basePath + 'header.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Header not found at: ' + basePath + 'header.html');
        }
        return response.text();
      })
      .then(data => {
        // Replace relative paths in header content based on current directory depth
        var updatedData = data.replace(/href="\\.\\/([^"]*)/g, 'href="' + basePath + '$1');
        updatedData = updatedData.replace(/src="\\.\\/([^"]*)/g, 'src="' + basePath + '$1');
        headerElement.innerHTML = updatedData;
        console.log('Navigation: Header loaded successfully');
        
        // Initialize Bootstrap components after header is loaded
        if (typeof bootstrap !== 'undefined') {
          var dropdowns = headerElement.querySelectorAll('[data-bs-toggle="dropdown"]');
          dropdowns.forEach(function(dropdown) {
            new bootstrap.Dropdown(dropdown);
          });
        }
      })
      .catch(error => {
        console.error('Error loading header:', error);
        // Fallback: try with different path
        fetch('../header.html')
          .then(response => response.text())
          .then(data => {
            var updatedData = data.replace(/href="\\.\\/([^"]*)/g, 'href="../$1');
            updatedData = updatedData.replace(/src="\\.\\/([^"]*)/g, 'src="../$1');
            headerElement.innerHTML = updatedData;
            console.log('Navigation: Header loaded with fallback path');
          })
          .catch(fallbackError => console.error('Fallback header load failed:', fallbackError));
      });
  }
  
  // Load footer
  var footerElement = document.getElementById('footer');
  if (footerElement) {
    fetch(basePath + 'footer.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Footer not found at: ' + basePath + 'footer.html');
        }
        return response.text();
      })
      .then(data => {
        // Replace relative paths in footer content based on current directory depth
        var updatedData = data.replace(/href="\\.\\/([^"]*)/g, 'href="' + basePath + '$1');
        updatedData = updatedData.replace(/src="\\.\\/([^"]*)/g, 'src="' + basePath + '$1');
        footerElement.innerHTML = updatedData;
        console.log('Navigation: Footer loaded successfully');
      })
      .catch(error => {
        console.error('Error loading footer:', error);
        // Fallback: try with different path
        fetch('../footer.html')
          .then(response => response.text())
          .then(data => {
            var updatedData = data.replace(/href="\\.\\/([^"]*)/g, 'href="../$1');
            updatedData = updatedData.replace(/src="\\.\\/([^"]*)/g, 'src="../$1');
            footerElement.innerHTML = updatedData;
            console.log('Navigation: Footer loaded with fallback path');
          })
          .catch(fallbackError => console.error('Fallback footer load failed:', fallbackError));
      });
  }
});"""
    
    # Write the improved navigation JavaScript
    nav_js_file = website_dir / "assets" / "js" / "include-nav.js"
    with open(nav_js_file, 'w', encoding='utf-8') as f:
        f.write(improved_nav_js)
    
    print(f"   ✅ Updated include-nav.js with improved path detection")
    
    # 2. Fix all files in the services/agriculture directory
    print("2. Fixing deeply nested service pages...")
    
    agriculture_dir = website_dir / "services" / "agriculture"
    if agriculture_dir.exists():
        for html_file in agriculture_dir.glob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix incorrect asset paths (../..../../ should be ../../)
                content = re.sub(r'\.\.\/\.\.\.\/\.\.\.\/assets/', '../../assets/', content)
                content = re.sub(r'\.\.\/\.\.\.\/\.\.\.\/([^"]*)', r'../../\1', content)
                
                # Ensure navigation fix script is included
                if 'navigation-fix.js' not in content:
                    script_tag = '<script src="../../assets/js/navigation-fix.js"></script>'
                    if '</body>' in content:
                        content = content.replace('</body>', f'  {script_tag}\n</body>')
                    else:
                        content += f'\n{script_tag}'
                
                # Write the corrected content
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Fixed asset paths in: {html_file}")
                
            except Exception as e:
                print(f"   ❌ Error processing {html_file}: {e}")
    
    # 3. Check for other deeply nested directories and fix them
    print("3. Scanning for other deeply nested pages...")
    
    nested_dirs = []
    for root, dirs, files in os.walk(website_dir):
        root_path = Path(root)
        # Calculate depth from website_dir
        relative_path = root_path.relative_to(website_dir)
        depth = len(relative_path.parts)
        
        # If depth > 1, it's a nested directory
        if depth > 1 and any(f.endswith('.html') for f in files):
            nested_dirs.append((root_path, depth))
    
    for nested_dir, depth in nested_dirs:
        print(f"   📁 Found nested directory at depth {depth}: {nested_dir}")
        
        for html_file in nested_dir.glob("*.html"):
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Calculate correct relative path
                correct_path = "../" * depth
                
                # Fix asset paths based on depth
                incorrect_patterns = [
                    r'\.\.\/\.\.\.\/\.\.\.\/assets/',  # ../../../assets/
                    r'\.\.\/\.\.\/\.\.\/assets/',      # ../../assets/ (if depth > 2)
                    r'\.\.\/assets/',                  # ../assets/ (if depth > 1)
                ]
                
                for pattern in incorrect_patterns:
                    content = re.sub(pattern, f'{correct_path}assets/', content)
                
                # Fix include-nav.js path
                content = re.sub(r'src="[^"]*assets/js/include-nav\.js"', 
                               f'src="{correct_path}assets/js/include-nav.js"', content)
                
                # Add navigation fix if missing
                if 'navigation-fix.js' not in content:
                    script_tag = f'<script src="{correct_path}assets/js/navigation-fix.js"></script>'
                    if '</body>' in content:
                        content = content.replace('</body>', f'  {script_tag}\n</body>')
                    else:
                        content += f'\n{script_tag}'
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Fixed paths in nested file: {html_file}")
                
            except Exception as e:
                print(f"   ❌ Error processing {html_file}: {e}")
    
    # 4. Create a test page to verify nested navigation
    print("4. Creating nested navigation test page...")
    
    test_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nested Navigation Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div id="header"></div>
    
    <div class="container mt-5">
        <h1>Nested Navigation Test</h1>
        <p>This page tests navigation loading from a deeply nested directory.</p>
        
        <div class="alert alert-info">
            <strong>Current Path:</strong> /services/agriculture/navigation-test.html<br>
            <strong>Expected Base Path:</strong> ../../<br>
            <strong>Header Should Load From:</strong> ../../header.html
        </div>
        
        <div class="mt-4">
            <h3>Navigation Status:</h3>
            <div id="nav-status" class="alert alert-warning">
                Checking navigation...
            </div>
        </div>
        
        <div class="mt-4">
            <a href="../../index.html" class="btn btn-primary">Back to Home</a>
            <a href="../analytical-testing-agriculture.html" class="btn btn-secondary">Back to Agriculture Services</a>
        </div>
    </div>
    
    <div id="footer"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../../assets/js/include-nav.js"></script>
    <script src="../../assets/js/navigation-fix.js"></script>
    
    <script>
        // Check if navigation loaded successfully
        setTimeout(function() {
            const header = document.getElementById('header');
            const statusDiv = document.getElementById('nav-status');
            
            if (header && header.innerHTML.trim() !== '') {
                statusDiv.className = 'alert alert-success';
                statusDiv.innerHTML = '✅ Navigation loaded successfully!';
            } else {
                statusDiv.className = 'alert alert-danger';
                statusDiv.innerHTML = '❌ Navigation failed to load. Check console for errors.';
            }
        }, 2000);
    </script>
</body>
</html>"""
    
    test_file = agriculture_dir / "navigation-test.html"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"   ✅ Created nested navigation test page: {test_file}")
    
    print("\n🎉 Nested Navigation Fix Complete!")
    print("\nSummary of fixes applied:")
    print("✅ Improved include-nav.js with better path detection")
    print("✅ Fixed asset paths in deeply nested pages")
    print("✅ Added navigation fix scripts to nested pages")
    print("✅ Created nested navigation test page")
    print(f"\n🌐 Test nested navigation at: http://localhost:8002/services/agriculture/navigation-test.html")
    print(f"🌐 Test original compost page at: http://localhost:8002/services/agriculture/compost.html")
    
    return True

if __name__ == "__main__":
    fix_nested_navigation()

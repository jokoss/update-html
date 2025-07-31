#!/usr/bin/env python3
"""
Comprehensive Navigation System Fix
This script systematically fixes all navigation issues across the entire website.
"""

import os
import re
from pathlib import Path

def find_all_html_files(directory):
    """Find all HTML files in the directory structure."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def calculate_relative_path(file_path, base_directory):
    """Calculate the relative path from a file to the base directory."""
    file_dir = os.path.dirname(file_path)
    rel_path = os.path.relpath(base_directory, file_dir)
    
    # Convert to forward slashes for web compatibility
    rel_path = rel_path.replace('\\', '/')
    
    # If we're in the same directory, use './'
    if rel_path == '.':
        return './'
    # If we need to go up directories, ensure it ends with '/'
    elif not rel_path.endswith('/'):
        return rel_path + '/'
    
    return rel_path

def clean_and_fix_html_file(file_path, base_directory):
    """Clean and fix a single HTML file."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Calculate the correct relative path for this file
        rel_path = calculate_relative_path(file_path, base_directory)
        
        # 1. Remove ALL jQuery navigation code
        jquery_patterns = [
            r'<script src="https://code\.jquery\.com/jquery-[^"]*"></script>',
            r'<script>\s*\$\(function\(\)\{\s*\$\("#header"\)\.load\("[^"]*"\);\s*\$\("#footer"\)\.load\("[^"]*"\);\s*\}\);\s*</script>',
            r'\$\(function\(\)\{\s*\$\("#header"\)\.load\("[^"]*"\);\s*\$\("#footer"\)\.load\("[^"]*"\);\s*\}\);',
            r'<script src="https://code\.jquery\.com/jquery-[^"]*"></script>\s*<script>\s*\$\(function\(\)\{[^}]*\}\);\s*</script>',
        ]
        
        for pattern in jquery_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                changes_made.append("Removed jQuery navigation code")
        
        # 2. Fix malformed header tags (escaped quotes)
        malformed_header = r'<header id=\\"header\\"></header>'
        if re.search(malformed_header, content):
            content = re.sub(malformed_header, '<div id="header"></div>', content)
            changes_made.append("Fixed malformed header tag")
        
        # 3. Ensure proper header and footer div structure
        # Check if header div exists
        if 'id="header"' not in content:
            # Find where to insert header div (usually after <body> or in <main>)
            if '<main class="page-wrapper">' in content:
                content = content.replace('<main class="page-wrapper">', '<main class="page-wrapper">\n      <div id="header"></div>')
                changes_made.append("Added missing header div")
            elif '<body>' in content:
                content = content.replace('<body>', '<body>\n    <div id="header"></div>')
                changes_made.append("Added missing header div")
        
        # Check if footer div exists
        if 'id="footer"' not in content:
            # Find where to insert footer div (usually before </main> or before </body>)
            if '</main>' in content:
                content = content.replace('</main>', '      <div id="footer"></div>\n    </main>')
                changes_made.append("Added missing footer div")
            elif '</body>' in content:
                content = content.replace('</body>', '    <div id="footer"></div>\n  </body>')
                changes_made.append("Added missing footer div")
        
        # 4. Ensure include-nav.js is loaded with correct path
        include_nav_pattern = r'<script src="[^"]*include-nav\.js"></script>'
        correct_include_nav = f'<script src="{rel_path}assets/js/include-nav.js"></script>'
        
        if re.search(include_nav_pattern, content):
            content = re.sub(include_nav_pattern, correct_include_nav, content)
            changes_made.append("Updated include-nav.js path")
        else:
            # Add include-nav.js before closing body tag
            if '</body>' in content:
                content = content.replace('</body>', f'      {correct_include_nav}\n</body>')
                changes_made.append("Added missing include-nav.js")
        
        # 5. Fix duplicate header elements
        # Remove any <header> tags that might conflict with our div structure
        header_tag_pattern = r'<header[^>]*>.*?</header>'
        if re.search(header_tag_pattern, content, re.DOTALL):
            # Only remove if it's not the main header structure we want
            if '<header id="header">' in content:
                content = re.sub(r'<header id="header"></header>', '', content)
                changes_made.append("Removed duplicate header tag")
        
        # 6. Fix asset paths to use relative paths
        asset_patterns = [
            (r'href="/assets/', f'href="{rel_path}assets/'),
            (r'src="/assets/', f'src="{rel_path}assets/'),
            (r'href="assets/', f'href="{rel_path}assets/'),
            (r'src="assets/', f'src="{rel_path}assets/'),
        ]
        
        for old_pattern, new_pattern in asset_patterns:
            if re.search(old_pattern, content):
                content = re.sub(old_pattern, new_pattern, content)
                changes_made.append(f"Fixed asset paths: {old_pattern}")
        
        # 7. Ensure proper HTML structure
        # Fix any remaining structural issues
        content = content.replace('<header id="header"></header>', '<div id="header"></div>')
        content = content.replace('<footer id="footer"></footer>', '<div id="footer"></div>')
        
        # 8. Clean up extra whitespace and formatting
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Remove excessive blank lines
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed: {', '.join(changes_made)}")
            return True
        else:
            print(f"  ✓ No changes needed")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False

def validate_navigation_structure(file_path):
    """Validate that a file has proper navigation structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for required elements
        if 'id="header"' not in content:
            issues.append("Missing header div")
        
        if 'id="footer"' not in content:
            issues.append("Missing footer div")
        
        if 'include-nav.js' not in content:
            issues.append("Missing include-nav.js script")
        
        # Check for problematic elements
        if 'jquery' in content.lower():
            issues.append("Still contains jQuery references")
        
        if '$("#header")' in content or '$("#footer")' in content:
            issues.append("Still contains jQuery navigation code")
        
        return issues
        
    except Exception as e:
        return [f"Error reading file: {e}"]

def main():
    base_directory = "MotzzWebsite-main"
    
    if not os.path.exists(base_directory):
        print(f"Error: Directory {base_directory} not found!")
        return
    
    print("=" * 60)
    print("COMPREHENSIVE NAVIGATION SYSTEM FIX")
    print("=" * 60)
    
    # Find all HTML files
    html_files = find_all_html_files(base_directory)
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    fixed_files = 0
    for html_file in html_files:
        if clean_and_fix_html_file(html_file, base_directory):
            fixed_files += 1
    
    print(f"\n📊 PROCESSING COMPLETE:")
    print(f"   Files processed: {len(html_files)}")
    print(f"   Files modified: {fixed_files}")
    
    # Validation phase
    print(f"\n🔍 VALIDATION PHASE:")
    problematic_files = []
    
    for html_file in html_files:
        issues = validate_navigation_structure(html_file)
        if issues:
            problematic_files.append((html_file, issues))
    
    if problematic_files:
        print(f"❌ Found {len(problematic_files)} files with remaining issues:")
        for file_path, issues in problematic_files:
            print(f"   {file_path}:")
            for issue in issues:
                print(f"     - {issue}")
    else:
        print(f"✅ All {len(html_files)} files have proper navigation structure!")
    
    print(f"\n✅ Comprehensive navigation fix complete!")

if __name__ == "__main__":
    main()

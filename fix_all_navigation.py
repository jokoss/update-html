#!/usr/bin/env python3
"""
Comprehensive script to fix all navigation issues in the Motzz Laboratory website.
This script will:
1. Fix asset paths in all HTML files
2. Update navigation includes
3. Ensure consistent relative paths
4. Fix broken links
"""

import os
import re
import glob
from pathlib import Path

def get_relative_path_to_root(file_path):
    """Calculate the relative path from a file to the root directory."""
    # Count directory levels
    path_parts = Path(file_path).parts
    # Remove the filename and count directories
    depth = len([part for part in path_parts[:-1] if part != 'MotzzWebsite-main'])
    
    if depth == 0:
        return "./"
    elif depth == 1:
        return "../"
    elif depth == 2:
        return "../../"
    else:
        return "../" * depth

def fix_html_file(file_path):
    """Fix navigation and asset paths in an HTML file."""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        relative_path = get_relative_path_to_root(file_path)
        
        # Fix asset paths
        content = re.sub(r'src="/assets/', f'src="{relative_path}assets/', content)
        content = re.sub(r'href="/assets/', f'href="{relative_path}assets/', content)
        content = re.sub(r'src="./assets/', f'src="{relative_path}assets/', content)
        content = re.sub(r'href="./assets/', f'href="{relative_path}assets/', content)
        
        # Fix navigation links
        content = re.sub(r'href="/index\.html"', f'href="{relative_path}index.html"', content)
        content = re.sub(r'href="/about-us\.html"', f'href="{relative_path}about-us.html"', content)
        content = re.sub(r'href="/analytical-testing\.html"', f'href="{relative_path}analytical-testing.html"', content)
        content = re.sub(r'href="/forms\.html"', f'href="{relative_path}forms.html"', content)
        content = re.sub(r'href="/license-accreditations\.html"', f'href="{relative_path}license-accreditations.html"', content)
        content = re.sub(r'href="/professional-membership\.html"', f'href="{relative_path}professional-membership.html"', content)
        content = re.sub(r'href="/privacy-policy\.html"', f'href="{relative_path}privacy-policy.html"', content)
        content = re.sub(r'href="/terms-conditions\.html"', f'href="{relative_path}terms-conditions.html"', content)
        
        # Fix service links
        content = re.sub(r'href="/services/', f'href="{relative_path}services/', content)
        content = re.sub(r'href="./services/', f'href="{relative_path}services/', content)
        
        # Fix sampling info links
        content = re.sub(r'href="/sampling-info/', f'href="{relative_path}sampling-info/', content)
        content = re.sub(r'href="./sampling-info/', f'href="{relative_path}sampling-info/', content)
        
        # Fix forms download links
        content = re.sub(r'href="/forms/download/', f'href="{relative_path}forms/download/', content)
        content = re.sub(r'href="./forms/download/', f'href="{relative_path}forms/download/', content)
        
        # Fix include script path
        content = re.sub(r'src="/assets/js/include-nav\.js"', f'src="{relative_path}assets/js/include-nav.js"', content)
        content = re.sub(r'src="./assets/js/include-nav\.js"', f'src="{relative_path}assets/js/include-nav.js"', content)
        
        # Ensure header and footer divs exist
        if '<div id="header">' not in content and '<header id="header">' not in content:
            # Add header div after body tag
            content = re.sub(r'(<body[^>]*>)', r'\1\n    <header id="header"></header>', content)
        
        if '<div id="footer">' not in content and '<footer id="footer"' not in content:
            # Add footer div before closing body tag
            content = re.sub(r'(</body>)', r'    <footer id="footer" class="footer bg-secondary pt-5 pb-4 pb-lg-5"></footer>\n\1', content)
        
        # Add include script if missing
        if 'include-nav.js' not in content:
            # Add before closing body tag
            script_tag = f'    <script src="{relative_path}assets/js/include-nav.js"></script>\n'
            content = re.sub(r'(</body>)', script_tag + r'\1', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Updated: {file_path}")
        else:
            print(f"  - No changes needed: {file_path}")
            
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")

def main():
    """Main function to process all HTML files."""
    print("Starting comprehensive navigation fix...")
    
    # Find all HTML files in the MotzzWebsite-main directory
    html_files = []
    
    # Get all HTML files recursively
    for root, dirs, files in os.walk('MotzzWebsite-main'):
        for file in files:
            if file.endswith('.html') and not file.startswith('404'):
                file_path = os.path.join(root, file)
                html_files.append(file_path)
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for file_path in sorted(html_files):
        fix_html_file(file_path)
    
    print("\nNavigation fix complete!")
    print("\nNext steps:")
    print("1. Test the website locally")
    print("2. Check all navigation links")
    print("3. Verify asset loading")

if __name__ == "__main__":
    main()

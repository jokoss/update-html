#!/usr/bin/env python3
"""
Comprehensive Page-by-Page Website Audit
This script will examine every HTML file individually and identify specific issues.
"""

import os
import re
from pathlib import Path
import json

def find_all_html_files(directory):
    """Find all HTML files in the website"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                html_files.append(rel_path)
    return sorted(html_files)

def analyze_page(file_path, base_dir):
    """Analyze a single HTML page for issues"""
    issues = []
    
    try:
        with open(os.path.join(base_dir, file_path), 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"ERROR: Cannot read file - {str(e)}"]
    
    # Check for asset paths
    css_links = re.findall(r'<link[^>]*href=["\']([^"\']*\.css)["\']', content)
    js_scripts = re.findall(r'<script[^>]*src=["\']([^"\']*\.js)["\']', content)
    img_sources = re.findall(r'<img[^>]*src=["\']([^"\']*)["\']', content)
    
    # Check if assets exist
    for css in css_links:
        if css.startswith('http'):
            continue
        css_path = resolve_path(css, file_path, base_dir)
        if not os.path.exists(css_path):
            issues.append(f"MISSING CSS: {css} -> {css_path}")
    
    for js in js_scripts:
        if js.startswith('http'):
            continue
        js_path = resolve_path(js, file_path, base_dir)
        if not os.path.exists(js_path):
            issues.append(f"MISSING JS: {js} -> {js_path}")
    
    # Check for navigation structure
    if '<div id="header"></div>' in content:
        issues.append("USES DYNAMIC HEADER: Requires include-nav.js")
    elif '<nav' not in content and 'header' not in content.lower():
        issues.append("NO NAVIGATION: Missing header/nav structure")
    
    if '<div id="footer"></div>' in content:
        issues.append("USES DYNAMIC FOOTER: Requires include-nav.js")
    elif '<footer' not in content and file_path != 'footer.html':
        issues.append("NO FOOTER: Missing footer structure")
    
    # Check for internal links
    internal_links = re.findall(r'href=["\']([^"\']*\.html)["\']', content)
    for link in internal_links:
        if link.startswith('http'):
            continue
        link_path = resolve_path(link, file_path, base_dir)
        if not os.path.exists(link_path):
            issues.append(f"BROKEN LINK: {link} -> {link_path}")
    
    # Check for specific issues
    if 'include-nav.js' in content:
        js_path = resolve_path('../assets/js/include-nav.js', file_path, base_dir)
        if not os.path.exists(js_path):
            issues.append("MISSING include-nav.js: Required for dynamic header/footer")
    
    return issues

def resolve_path(relative_path, current_file, base_dir):
    """Resolve relative path based on current file location"""
    current_dir = os.path.dirname(current_file)
    resolved = os.path.normpath(os.path.join(base_dir, current_dir, relative_path))
    return resolved

def main():
    base_dir = "MotzzWebsite-main"
    
    print("=== COMPREHENSIVE PAGE-BY-PAGE AUDIT ===\n")
    
    # Find all HTML files
    html_files = find_all_html_files(base_dir)
    
    print(f"Found {len(html_files)} HTML files to audit:\n")
    
    audit_results = {}
    total_issues = 0
    
    for file_path in html_files:
        print(f"AUDITING: {file_path}")
        issues = analyze_page(file_path, base_dir)
        
        if issues:
            audit_results[file_path] = issues
            total_issues += len(issues)
            print(f"  ❌ {len(issues)} issues found:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print(f"  ✅ No issues found")
        print()
    
    # Summary
    print("=== AUDIT SUMMARY ===")
    print(f"Total files audited: {len(html_files)}")
    print(f"Files with issues: {len(audit_results)}")
    print(f"Total issues found: {total_issues}")
    
    if audit_results:
        print("\n=== FILES REQUIRING FIXES ===")
        for file_path, issues in audit_results.items():
            print(f"\n{file_path}:")
            for issue in issues:
                print(f"  - {issue}")
    
    # Save results to JSON
    with open('page_audit_results.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    
    print(f"\nDetailed results saved to: page_audit_results.json")

if __name__ == "__main__":
    main()

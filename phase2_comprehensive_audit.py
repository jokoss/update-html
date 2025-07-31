#!/usr/bin/env python3
"""
Phase 2: Comprehensive Website Audit and Link Repair
This script performs a thorough audit of all HTML files and fixes any remaining broken links.
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

def find_all_html_files(directory):
    """Find all HTML files in the directory structure."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_links_from_html(file_path):
    """Extract all links (href and src) from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all href and src attributes
        href_pattern = r'href=["\']([^"\']*)["\']'
        src_pattern = r'src=["\']([^"\']*)["\']'
        
        hrefs = re.findall(href_pattern, content, re.IGNORECASE)
        srcs = re.findall(src_pattern, content, re.IGNORECASE)
        
        return hrefs, srcs, content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return [], [], ""

def is_external_link(url):
    """Check if a URL is external (starts with http/https)."""
    return url.startswith('http://') or url.startswith('https://')

def is_anchor_link(url):
    """Check if a URL is an anchor link (starts with #)."""
    return url.startswith('#')

def is_email_link(url):
    """Check if a URL is an email link (starts with mailto:)."""
    return url.startswith('mailto:')

def is_tel_link(url):
    """Check if a URL is a telephone link (starts with tel:)."""
    return url.startswith('tel:')

def resolve_relative_path(base_file, target_path):
    """Resolve a relative path from a base file to target."""
    base_dir = os.path.dirname(base_file)
    resolved = os.path.normpath(os.path.join(base_dir, target_path))
    return resolved

def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def audit_website_links(base_directory):
    """Perform comprehensive audit of all website links."""
    print("=== PHASE 2: COMPREHENSIVE WEBSITE AUDIT ===")
    print(f"Auditing directory: {base_directory}")
    
    html_files = find_all_html_files(base_directory)
    print(f"Found {len(html_files)} HTML files to audit")
    
    broken_links = []
    all_links = []
    
    for html_file in html_files:
        print(f"\nAuditing: {html_file}")
        hrefs, srcs, content = extract_links_from_html(html_file)
        
        # Check all href links
        for href in hrefs:
            if is_external_link(href) or is_anchor_link(href) or is_email_link(href) or is_tel_link(href):
                continue  # Skip external, anchor, email, and tel links
            
            # Resolve relative path
            resolved_path = resolve_relative_path(html_file, href)
            all_links.append((html_file, 'href', href, resolved_path))
            
            if not check_file_exists(resolved_path):
                broken_links.append({
                    'file': html_file,
                    'type': 'href',
                    'link': href,
                    'resolved': resolved_path,
                    'issue': 'File not found'
                })
        
        # Check all src links
        for src in srcs:
            if is_external_link(src):
                continue  # Skip external links
            
            # Resolve relative path
            resolved_path = resolve_relative_path(html_file, src)
            all_links.append((html_file, 'src', src, resolved_path))
            
            if not check_file_exists(resolved_path):
                broken_links.append({
                    'file': html_file,
                    'type': 'src',
                    'link': src,
                    'resolved': resolved_path,
                    'issue': 'File not found'
                })
    
    return broken_links, all_links

def suggest_fixes(broken_links, base_directory):
    """Suggest fixes for broken links."""
    print("\n=== BROKEN LINKS ANALYSIS ===")
    
    if not broken_links:
        print("✅ No broken links found!")
        return []
    
    fixes = []
    
    for broken in broken_links:
        print(f"\n❌ BROKEN: {broken['file']}")
        print(f"   Type: {broken['type']}")
        print(f"   Link: {broken['link']}")
        print(f"   Resolved to: {broken['resolved']}")
        
        # Try to find similar files
        filename = os.path.basename(broken['resolved'])
        potential_matches = []
        
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file == filename:
                    potential_matches.append(os.path.join(root, file))
        
        if potential_matches:
            print(f"   💡 Potential matches found:")
            for match in potential_matches:
                print(f"      - {match}")
                
                # Calculate relative path from broken file to potential match
                rel_path = os.path.relpath(match, os.path.dirname(broken['file']))
                fixes.append({
                    'file': broken['file'],
                    'type': broken['type'],
                    'old_link': broken['link'],
                    'new_link': rel_path.replace('\\', '/'),  # Use forward slashes for web
                    'confidence': 'high' if len(potential_matches) == 1 else 'medium'
                })
        else:
            print(f"   ❓ No potential matches found for {filename}")
    
    return fixes

def apply_fixes(fixes):
    """Apply the suggested fixes to HTML files."""
    print("\n=== APPLYING FIXES ===")
    
    files_modified = set()
    
    for fix in fixes:
        if fix['confidence'] == 'high':
            print(f"\n🔧 Fixing: {fix['file']}")
            print(f"   Replacing: {fix['old_link']} → {fix['new_link']}")
            
            try:
                with open(fix['file'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create the replacement pattern
                if fix['type'] == 'href':
                    old_pattern = f'href="{fix["old_link"]}"'
                    new_pattern = f'href="{fix["new_link"]}"'
                else:  # src
                    old_pattern = f'src="{fix["old_link"]}"'
                    new_pattern = f'src="{fix["new_link"]}"'
                
                # Also handle single quotes
                old_pattern_single = old_pattern.replace('"', "'")
                new_pattern_single = new_pattern.replace('"', "'")
                
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    files_modified.add(fix['file'])
                elif old_pattern_single in content:
                    content = content.replace(old_pattern_single, new_pattern_single)
                    files_modified.add(fix['file'])
                
                with open(fix['file'], 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Fixed successfully")
                
            except Exception as e:
                print(f"   ❌ Error applying fix: {e}")
    
    print(f"\n📊 SUMMARY: Modified {len(files_modified)} files")
    for file in sorted(files_modified):
        print(f"   - {file}")

def main():
    base_directory = "MotzzWebsite-main"
    
    if not os.path.exists(base_directory):
        print(f"Error: Directory {base_directory} not found!")
        return
    
    # Perform audit
    broken_links, all_links = audit_website_links(base_directory)
    
    print(f"\n📊 AUDIT SUMMARY:")
    print(f"   Total links checked: {len(all_links)}")
    print(f"   Broken links found: {len(broken_links)}")
    
    if broken_links:
        # Suggest fixes
        fixes = suggest_fixes(broken_links, base_directory)
        
        if fixes:
            print(f"\n🔧 FIXES AVAILABLE:")
            high_confidence = [f for f in fixes if f['confidence'] == 'high']
            medium_confidence = [f for f in fixes if f['confidence'] == 'medium']
            
            print(f"   High confidence fixes: {len(high_confidence)}")
            print(f"   Medium confidence fixes: {len(medium_confidence)}")
            
            # Apply high confidence fixes automatically
            if high_confidence:
                apply_fixes(high_confidence)
            
            # Show medium confidence fixes for manual review
            if medium_confidence:
                print(f"\n⚠️  MEDIUM CONFIDENCE FIXES (manual review recommended):")
                for fix in medium_confidence:
                    print(f"   File: {fix['file']}")
                    print(f"   Replace: {fix['old_link']} → {fix['new_link']}")
    
    print(f"\n✅ Phase 2 audit complete!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Systematic Page-by-Page Fix Script
This will fix all identified issues in every HTML file
"""

import os
import re
import json
from pathlib import Path

def fix_asset_paths_in_file(file_path, base_dir):
    """Fix asset paths in a specific file"""
    full_path = os.path.join(base_dir, file_path)
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return False
    
    original_content = content
    
    # Determine correct relative path based on file location
    path_parts = file_path.replace('\\', '/').split('/')
    depth = len(path_parts) - 1
    
    if depth == 0:
        # Root level files
        correct_prefix = "./"
    elif depth == 1:
        # One level deep (services/, about-us/, etc.)
        correct_prefix = "../"
    elif depth == 2:
        # Two levels deep (services/agriculture/, etc.)
        correct_prefix = "../../"
    else:
        # Deeper levels
        correct_prefix = "../" * depth
    
    # Fix common broken patterns
    broken_patterns = [
        (r'href="\.\.\.\./', f'href="{correct_prefix}'),
        (r'src="\.\.\.\./', f'src="{correct_prefix}'),
        (r'href="\.\.\.\.\.\./', f'href="{correct_prefix}'),
        (r'src="\.\.\.\.\.\./', f'src="{correct_prefix}'),
        (r'href="\.\.\.\.\.\.\.\./', f'href="{correct_prefix}'),
        (r'src="\.\.\.\.\.\.\.\./', f'src="{correct_prefix}'),
    ]
    
    for pattern, replacement in broken_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix specific asset paths that are commonly broken
    if depth > 0:
        # Fix CSS paths
        content = re.sub(r'href="assets/', f'href="{correct_prefix}assets/', content)
        content = re.sub(r'src="assets/', f'src="{correct_prefix}assets/', content)
        
        # Fix favicon paths
        content = re.sub(r'href="assets/favicon/', f'href="{correct_prefix}assets/favicon/', content)
        
        # Fix manifest paths
        content = re.sub(r'href="assets/favicon/site\.webmanifest"', f'href="{correct_prefix}assets/favicon/site.webmanifest"', content)
        content = re.sub(r'content="assets/favicon/', f'content="{correct_prefix}assets/favicon/', content)
    
    # Write back if changed
    if content != original_content:
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"FIXED: {file_path}")
            return True
        except Exception as e:
            print(f"ERROR writing {file_path}: {e}")
            return False
    
    return False

def copy_assets_to_subdirectories(base_dir):
    """Copy assets to subdirectories that need them"""
    source_assets = os.path.join(base_dir, "assets")
    
    if not os.path.exists(source_assets):
        print("ERROR: Source assets directory not found")
        return
    
    # Directories that need assets copied
    subdirs_needing_assets = [
        "about-us",
        "contact-us", 
        "forms",
        "laboratorytesting",
        "sampling",
        "sampling-info",
        "services"
    ]
    
    for subdir in subdirs_needing_assets:
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.exists(subdir_path):
            target_assets = os.path.join(subdir_path, "assets")
            
            # Create symlink or copy assets
            if not os.path.exists(target_assets):
                try:
                    # Try to create a symlink first (more efficient)
                    os.symlink(os.path.abspath(source_assets), target_assets)
                    print(f"SYMLINK: Created assets symlink in {subdir}")
                except OSError:
                    # If symlink fails, copy the directory
                    import shutil
                    shutil.copytree(source_assets, target_assets)
                    print(f"COPIED: Assets copied to {subdir}")

def fix_include_nav_paths(base_dir):
    """Ensure include-nav.js is accessible from all locations"""
    # Copy include-nav.js to assets/js if it doesn't exist there
    main_include_nav = os.path.join(base_dir, "assets", "js", "include-nav.js")
    root_include_nav = os.path.join("assets", "js", "include-nav.js")
    
    if os.path.exists(root_include_nav) and not os.path.exists(main_include_nav):
        os.makedirs(os.path.dirname(main_include_nav), exist_ok=True)
        import shutil
        shutil.copy2(root_include_nav, main_include_nav)
        print("COPIED: include-nav.js to main assets directory")

def main():
    base_dir = "MotzzWebsite-main"
    
    print("=== SYSTEMATIC PAGE-BY-PAGE FIXES ===\n")
    
    # Step 1: Copy assets to subdirectories
    print("Step 1: Setting up assets in subdirectories...")
    copy_assets_to_subdirectories(base_dir)
    
    # Step 2: Fix include-nav.js accessibility
    print("\nStep 2: Fixing include-nav.js accessibility...")
    fix_include_nav_paths(base_dir)
    
    # Step 3: Load audit results
    try:
        with open('page_audit_results.json', 'r') as f:
            audit_results = json.load(f)
    except FileNotFoundError:
        print("ERROR: page_audit_results.json not found. Run audit first.")
        return
    
    # Step 4: Fix each problematic file
    print(f"\nStep 3: Fixing {len(audit_results)} problematic files...")
    
    fixed_count = 0
    for file_path, issues in audit_results.items():
        # Skip vendor files and test files - these aren't part of the main website
        if any(skip in file_path for skip in ['vendor', 'test', 'demo', 'src/copy']):
            continue
            
        print(f"\nFixing: {file_path}")
        if fix_asset_paths_in_file(file_path, base_dir):
            fixed_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {len(audit_results)}")
    print(f"Files fixed: {fixed_count}")
    print("\nRun the audit again to verify fixes!")

if __name__ == "__main__":
    main()

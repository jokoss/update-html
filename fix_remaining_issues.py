#!/usr/bin/env python3
"""
Fix remaining issues identified in the audit
"""

import os
import re
import shutil
from pathlib import Path

def fix_broken_asset_patterns(base_dir):
    """Fix remaining broken asset patterns"""
    
    # Files that still have broken patterns
    problematic_files = [
        "about-us/analytical-testing.html",
        "contact-us/analytical-testing.html", 
        "forms/analytical-testing.html",
        "laboratorytesting/analytical-testing.html",
        "sampling/analytical-testing.html"
    ]
    
    for file_path in problematic_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            continue
        
        original_content = content
        
        # Fix the broken .... patterns
        content = re.sub(r'href="\.\.\.\./', 'href="../', content)
        content = re.sub(r'src="\.\.\.\./', 'src="../', content)
        
        if content != original_content:
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"FIXED broken patterns in: {file_path}")
            except Exception as e:
                print(f"ERROR writing {file_path}: {e}")

def fix_services_agriculture_paths(base_dir):
    """Fix the services/agriculture subdirectory paths"""
    
    agriculture_files = [
        "services/agriculture/compost.html",
        "services/agriculture/fertilizer.html", 
        "services/agriculture/plant-tissue-petiole.html",
        "services/agriculture/soil.html",
        "services/agriculture/water.html"
    ]
    
    for file_path in agriculture_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            continue
        
        original_content = content
        
        # Fix paths for 2-level deep files (services/agriculture/)
        # These need ../../ to get back to root
        
        # Fix CSS paths
        content = re.sub(r'href="\.\.\.\.\.\./', 'href="../../', content)
        content = re.sub(r'href="\.\.\.\./', 'href="../../', content)
        content = re.sub(r'href="\.\./\.\./\.\./', 'href="../../', content)
        
        # Fix JS paths  
        content = re.sub(r'src="\.\.\.\.\.\./', 'src="../../', content)
        content = re.sub(r'src="\.\.\.\./', 'src="../../', content)
        content = re.sub(r'src="\.\./\.\./\.\./', 'src="../../', content)
        
        if content != original_content:
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"FIXED agriculture paths in: {file_path}")
            except Exception as e:
                print(f"ERROR writing {file_path}: {e}")

def fix_sampling_info_links(base_dir):
    """Fix broken links in sampling-info pages"""
    
    sampling_files = [
        "sampling-info/plant-tissue.html",
        "sampling-info/soil.html",
        "sampling-info/water.html"
    ]
    
    for file_path in sampling_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            continue
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            continue
        
        original_content = content
        
        # Fix broken internal links
        content = re.sub(r'href="\.\./sampling-info/sampling-information-water\.html"', 'href="water.html"', content)
        content = re.sub(r'href="\.\./sampling-info/sampling-information-soil\.html"', 'href="soil.html"', content)
        
        if content != original_content:
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"FIXED sampling-info links in: {file_path}")
            except Exception as e:
                print(f"ERROR writing {file_path}: {e}")

def copy_missing_assets(base_dir):
    """Copy assets to directories that are missing them"""
    
    source_assets = os.path.join(base_dir, "assets")
    if not os.path.exists(source_assets):
        print("ERROR: Source assets directory not found")
        return
    
    # Directories that need assets
    target_dirs = [
        "about-us",
        "contact-us",
        "forms", 
        "laboratorytesting",
        "sampling",
        "sampling-info",
        "services"
    ]
    
    for target_dir in target_dirs:
        target_path = os.path.join(base_dir, target_dir)
        if not os.path.exists(target_path):
            continue
            
        target_assets = os.path.join(target_path, "assets")
        
        if not os.path.exists(target_assets):
            try:
                # Copy the entire assets directory
                shutil.copytree(source_assets, target_assets)
                print(f"COPIED assets to: {target_dir}")
            except Exception as e:
                print(f"ERROR copying assets to {target_dir}: {e}")

def main():
    base_dir = "MotzzWebsite-main"
    
    print("=== FIXING REMAINING ISSUES ===\n")
    
    print("Step 1: Copying missing assets...")
    copy_missing_assets(base_dir)
    
    print("\nStep 2: Fixing broken asset patterns...")
    fix_broken_asset_patterns(base_dir)
    
    print("\nStep 3: Fixing services/agriculture paths...")
    fix_services_agriculture_paths(base_dir)
    
    print("\nStep 4: Fixing sampling-info links...")
    fix_sampling_info_links(base_dir)
    
    print("\n=== FIXES COMPLETE ===")
    print("Run audit again to verify remaining issues!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Fix Services Asset Paths
Corrects the broken asset paths in all services pages
"""

import os
import re
import glob

def fix_services_asset_paths():
    """Fix asset paths in all services pages."""
    print("🔧 FIXING SERVICES ASSET PATHS")
    print("=" * 50)
    
    # Find all HTML files in services directory
    services_files = glob.glob("MotzzWebsite-main/services/*.html")
    
    print(f"📁 Found {len(services_files)} service pages to fix")
    
    fixed_count = 0
    
    for service_file in services_files:
        print(f"Processing: {service_file}")
        
        try:
            with open(service_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix the broken asset paths
            # Replace ..../assets/ with ../assets/
            content = content.replace('..../assets/', '../assets/')
            
            # Also fix any other variations
            content = content.replace('..../', '../')
            
            if content != original_content:
                with open(service_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Fixed asset paths")
                fixed_count += 1
            else:
                print(f"  ✓ No changes needed")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n📊 RESULTS:")
    print(f"   Files processed: {len(services_files)}")
    print(f"   Files fixed: {fixed_count}")
    
    if fixed_count > 0:
        print(f"\n🎉 Successfully fixed asset paths in {fixed_count} service pages!")
    else:
        print(f"\n✅ All service pages already have correct asset paths!")

if __name__ == "__main__":
    fix_services_asset_paths()

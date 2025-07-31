import os
import re

def main():
    # Fix asset paths in subpages
    fix_asset_paths()

def fix_asset_paths():
    # Update all subpages to use the correct asset paths
    subpage_dirs = [
        'MotzzWebsite-main/about-us',
        'MotzzWebsite-main/contact-us',
        'MotzzWebsite-main/laboratorytesting',
        'MotzzWebsite-main/sampling',
        'MotzzWebsite-main/forms'
    ]
    
    for subpage_dir in subpage_dirs:
        if os.path.exists(subpage_dir):
            for file in os.listdir(subpage_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(subpage_dir, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace asset paths with local paths
                    content = content.replace('src="../assets/img/logo.svg"', 'src="assets/img/logo.svg"')
                    content = content.replace('src="../assets/js/theme.min.js"', 'src="assets/js/theme.min.js"')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated asset paths in {file_path}")

if __name__ == "__main__":
    main()

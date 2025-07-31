import os
import re

def main():
    # Fix CSS paths in subpages
    fix_css_paths()

def fix_css_paths():
    # Update all subpages to use the correct CSS paths
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
                    
                    # Replace CSS paths with local paths
                    content = content.replace('href="../assets/css/site.css"', 'href="assets/css/site.css"')
                    content = content.replace('href="../assets/css/theme.min.css"', 'href="assets/css/theme.min.css"')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated CSS paths in {file_path}")

if __name__ == "__main__":
    main()

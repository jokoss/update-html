import os
import re

def main():
    # Fix the paths in subpages
    fix_subpage_paths()

def fix_subpage_paths():
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
                    
                    # Replace absolute paths with relative paths
                    content = content.replace('href="/assets/', 'href="../assets/')
                    content = content.replace('src="/assets/', 'src="../assets/')
                    
                    # Replace vendor paths
                    content = content.replace('href="/assets/vendor/', 'href="../assets/vendor/')
                    content = content.replace('src="/assets/vendor/', 'src="../assets/vendor/')
                    
                    # Replace favicon paths
                    content = content.replace('href="/assets/favicon/', 'href="../assets/favicon/')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated asset paths in {file_path}")

if __name__ == "__main__":
    main()

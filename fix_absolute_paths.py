import os
import re

def main():
    # Fix absolute paths in subpages
    fix_absolute_paths()

def fix_absolute_paths():
    # Update all subpages to use the correct paths
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
                    content = content.replace('href="/index.html"', 'href="../index.html"')
                    content = content.replace('href="/analytical-testing.html"', 'href="../analytical-testing.html"')
                    content = content.replace('href="/about-us.html"', 'href="../about-us.html"')
                    content = content.replace('href="/license-accreditations.html"', 'href="../license-accreditations.html"')
                    content = content.replace('href="/professional-membership.html"', 'href="../professional-membership.html"')
                    content = content.replace('href="/forms.html"', 'href="../forms.html"')
                    content = content.replace('href="/terms-conditions.html"', 'href="../terms-conditions.html"')
                    content = content.replace('href="/privacy-policy.html"', 'href="../privacy-policy.html"')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated absolute paths in {file_path}")

if __name__ == "__main__":
    main()

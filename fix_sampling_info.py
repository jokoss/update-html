import os
import re

def main():
    # Fix sampling-info paths in subpages
    fix_sampling_info_paths()

def fix_sampling_info_paths():
    # Update all subpages to use the correct sampling-info paths
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
                    
                    # Replace sampling-info paths with relative paths
                    content = content.replace('href="/sampling-info/plant-tissue.html"', 'href="../sampling-info/plant-tissue.html"')
                    content = content.replace('href="/sampling-info/sampling-information-water.html"', 'href="../sampling-info/water.html"')
                    content = content.replace('href="/sampling-info/sampling-information-soil.html"', 'href="../sampling-info/soil.html"')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated sampling-info paths in {file_path}")

if __name__ == "__main__":
    main()

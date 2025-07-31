import os
import re
import shutil

def main():
    # Create symlinks for common paths
    create_symlinks()
    
    # Fix the remaining broken links in subpage header and footer
    fix_subpage_header_footer()

def create_symlinks():
    # Create symlinks for common paths
    symlinks = [
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/MotzzWebsite-main/index.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/MotzzWebsite-main/analytical-testing.html'),
        ('MotzzWebsite-main/about-us.html', 'MotzzWebsite-main/MotzzWebsite-main/about-us.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/MotzzWebsite-main/license-accreditations.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/MotzzWebsite-main/professional-membership.html'),
        ('MotzzWebsite-main/forms.html', 'MotzzWebsite-main/MotzzWebsite-main/forms.html')
    ]
    
    for src, dst in symlinks:
        if os.path.exists(src) and not os.path.exists(dst):
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            # Copy the file
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

def fix_subpage_header_footer():
    # Fix the subpage header and footer
    subpage_files = [
        'MotzzWebsite-main/subpage-header.html',
        'MotzzWebsite-main/subpage-footer.html'
    ]
    
    for file_path in subpage_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace all ../path with ./path
            content = content.replace('href="../', 'href="./')
            content = content.replace('src="../', 'src="./')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Updated {file_path}")
    
    # Update all subpages to use the correct header and footer loading
    subpage_dirs = [
        'MotzzWebsite-main/services',
        'MotzzWebsite-main/services/agriculture',
        'MotzzWebsite-main/sampling-info',
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
                    
                    # Check if the file has jQuery and header/footer loading
                    if 'jquery' in content.lower() and '$("#header")' in content:
                        # Update the header/footer loading
                        content = content.replace('$("#header").load("../subpage-header.html")', '$("#header").load("../header.html")')
                        content = content.replace('$("#footer").load("../subpage-footer.html")', '$("#footer").load("../footer.html")')
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"Updated header/footer loading in {file_path}")

if __name__ == "__main__":
    main()

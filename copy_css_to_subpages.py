import os
import shutil

def main():
    # Copy CSS to subpages
    copy_css_to_subpages()

def copy_css_to_subpages():
    # Create the necessary directories in the subpages
    subpage_dirs = [
        'MotzzWebsite-main/about-us/assets/css',
        'MotzzWebsite-main/contact-us/assets/css',
        'MotzzWebsite-main/laboratorytesting/assets/css',
        'MotzzWebsite-main/sampling/assets/css',
        'MotzzWebsite-main/forms/assets/css'
    ]
    
    for asset_dir in subpage_dirs:
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
            print(f"Created directory: {asset_dir}")
    
    # Copy CSS to subpages
    css_files = [
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/about-us/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/contact-us/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/laboratorytesting/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/sampling/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/forms/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/about-us/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/contact-us/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/laboratorytesting/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/sampling/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/forms/assets/css/theme.min.css')
    ]
    
    for src, dst in css_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

if __name__ == "__main__":
    main()

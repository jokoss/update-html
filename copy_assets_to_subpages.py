import os
import shutil

def main():
    # Copy assets to subpages
    copy_assets_to_subpages()

def copy_assets_to_subpages():
    # Create the necessary directories in the subpages
    subpage_dirs = [
        'MotzzWebsite-main/about-us/assets',
        'MotzzWebsite-main/about-us/assets/img',
        'MotzzWebsite-main/about-us/assets/js',
        'MotzzWebsite-main/contact-us/assets',
        'MotzzWebsite-main/contact-us/assets/img',
        'MotzzWebsite-main/contact-us/assets/js',
        'MotzzWebsite-main/laboratorytesting/assets',
        'MotzzWebsite-main/laboratorytesting/assets/img',
        'MotzzWebsite-main/laboratorytesting/assets/js',
        'MotzzWebsite-main/sampling/assets',
        'MotzzWebsite-main/sampling/assets/img',
        'MotzzWebsite-main/sampling/assets/js',
        'MotzzWebsite-main/forms/assets',
        'MotzzWebsite-main/forms/assets/img',
        'MotzzWebsite-main/forms/assets/js'
    ]
    
    for asset_dir in subpage_dirs:
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
            print(f"Created directory: {asset_dir}")
    
    # Copy assets to subpages
    assets = [
        ('MotzzWebsite-main/assets/img/logo.svg', 'MotzzWebsite-main/about-us/assets/img/logo.svg'),
        ('MotzzWebsite-main/assets/img/logo.svg', 'MotzzWebsite-main/contact-us/assets/img/logo.svg'),
        ('MotzzWebsite-main/assets/img/logo.svg', 'MotzzWebsite-main/laboratorytesting/assets/img/logo.svg'),
        ('MotzzWebsite-main/assets/img/logo.svg', 'MotzzWebsite-main/sampling/assets/img/logo.svg'),
        ('MotzzWebsite-main/assets/img/logo.svg', 'MotzzWebsite-main/forms/assets/img/logo.svg'),
        ('MotzzWebsite-main/assets/js/theme.min.js', 'MotzzWebsite-main/about-us/assets/js/theme.min.js'),
        ('MotzzWebsite-main/assets/js/theme.min.js', 'MotzzWebsite-main/contact-us/assets/js/theme.min.js'),
        ('MotzzWebsite-main/assets/js/theme.min.js', 'MotzzWebsite-main/laboratorytesting/assets/js/theme.min.js'),
        ('MotzzWebsite-main/assets/js/theme.min.js', 'MotzzWebsite-main/sampling/assets/js/theme.min.js'),
        ('MotzzWebsite-main/assets/js/theme.min.js', 'MotzzWebsite-main/forms/assets/js/theme.min.js')
    ]
    
    for src, dst in assets:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

if __name__ == "__main__":
    main()

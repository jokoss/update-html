import os
import shutil

def main():
    # Copy assets to the correct locations
    copy_assets()

def copy_assets():
    # Create the necessary directories
    asset_dirs = [
        'MotzzWebsite-main/MotzzWebsite-main/assets',
        'MotzzWebsite-main/MotzzWebsite-main/assets/css',
        'MotzzWebsite-main/MotzzWebsite-main/assets/favicon',
        'MotzzWebsite-main/MotzzWebsite-main/assets/vendor',
        'MotzzWebsite-main/MotzzWebsite-main/assets/vendor/boxicons/css',
        'MotzzWebsite-main/MotzzWebsite-main/assets/vendor/swiper'
    ]
    
    for asset_dir in asset_dirs:
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
            print(f"Created directory: {asset_dir}")
    
    # Copy CSS files
    css_files = [
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/MotzzWebsite-main/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/MotzzWebsite-main/assets/css/site.css')
    ]
    
    for src, dst in css_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
    
    # Copy favicon files
    favicon_files = [
        ('MotzzWebsite-main/assets/favicon/apple-touch-icon.png', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/apple-touch-icon.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-32x32.png', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/favicon-32x32.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-16x16.png', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/favicon-16x16.png'),
        ('MotzzWebsite-main/assets/favicon/site.webmanifest', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/site.webmanifest'),
        ('MotzzWebsite-main/assets/favicon/safari-pinned-tab.svg', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/safari-pinned-tab.svg'),
        ('MotzzWebsite-main/assets/favicon/favicon.ico', 'MotzzWebsite-main/MotzzWebsite-main/assets/favicon/favicon.ico')
    ]
    
    for src, dst in favicon_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
    
    # Create placeholder vendor files
    vendor_files = [
        'MotzzWebsite-main/MotzzWebsite-main/assets/vendor/boxicons/css/boxicons.min.css',
        'MotzzWebsite-main/MotzzWebsite-main/assets/vendor/swiper/swiper-bundle.min.css'
    ]
    
    for vendor_file in vendor_files:
        if not os.path.exists(vendor_file):
            with open(vendor_file, 'w') as f:
                f.write('/* Placeholder file */')
            print(f"Created placeholder file: {vendor_file}")

if __name__ == "__main__":
    main()

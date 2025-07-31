import os
import shutil

def main():
    # Fix the remaining asset issues
    fix_assets()

def fix_assets():
    # Create the necessary directories in the services directory
    service_dirs = [
        'MotzzWebsite-main/services/assets',
        'MotzzWebsite-main/services/assets/css',
        'MotzzWebsite-main/services/assets/favicon',
        'MotzzWebsite-main/services/agriculture/assets',
        'MotzzWebsite-main/services/agriculture/assets/css',
        'MotzzWebsite-main/services/agriculture/assets/favicon',
        'MotzzWebsite-main/sampling-info/assets',
        'MotzzWebsite-main/sampling-info/assets/css',
        'MotzzWebsite-main/sampling-info/assets/favicon'
    ]
    
    for asset_dir in service_dirs:
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
            print(f"Created directory: {asset_dir}")
    
    # Copy CSS files to services directory
    css_files = [
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/services/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/services/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/services/agriculture/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/services/agriculture/assets/css/site.css'),
        ('MotzzWebsite-main/assets/css/theme.min.css', 'MotzzWebsite-main/sampling-info/assets/css/theme.min.css'),
        ('MotzzWebsite-main/assets/css/site.css', 'MotzzWebsite-main/sampling-info/assets/css/site.css')
    ]
    
    for src, dst in css_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")
    
    # Copy favicon files to services directory
    favicon_files = [
        ('MotzzWebsite-main/assets/favicon/apple-touch-icon.png', 'MotzzWebsite-main/services/assets/favicon/apple-touch-icon.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-32x32.png', 'MotzzWebsite-main/services/assets/favicon/favicon-32x32.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-16x16.png', 'MotzzWebsite-main/services/assets/favicon/favicon-16x16.png'),
        ('MotzzWebsite-main/assets/favicon/site.webmanifest', 'MotzzWebsite-main/services/assets/favicon/site.webmanifest'),
        ('MotzzWebsite-main/assets/favicon/safari-pinned-tab.svg', 'MotzzWebsite-main/services/assets/favicon/safari-pinned-tab.svg'),
        ('MotzzWebsite-main/assets/favicon/favicon.ico', 'MotzzWebsite-main/services/assets/favicon/favicon.ico'),
        ('MotzzWebsite-main/assets/favicon/apple-touch-icon.png', 'MotzzWebsite-main/services/agriculture/assets/favicon/apple-touch-icon.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-32x32.png', 'MotzzWebsite-main/services/agriculture/assets/favicon/favicon-32x32.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-16x16.png', 'MotzzWebsite-main/services/agriculture/assets/favicon/favicon-16x16.png'),
        ('MotzzWebsite-main/assets/favicon/site.webmanifest', 'MotzzWebsite-main/services/agriculture/assets/favicon/site.webmanifest'),
        ('MotzzWebsite-main/assets/favicon/safari-pinned-tab.svg', 'MotzzWebsite-main/services/agriculture/assets/favicon/safari-pinned-tab.svg'),
        ('MotzzWebsite-main/assets/favicon/favicon.ico', 'MotzzWebsite-main/services/agriculture/assets/favicon/favicon.ico'),
        ('MotzzWebsite-main/assets/favicon/apple-touch-icon.png', 'MotzzWebsite-main/sampling-info/assets/favicon/apple-touch-icon.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-32x32.png', 'MotzzWebsite-main/sampling-info/assets/favicon/favicon-32x32.png'),
        ('MotzzWebsite-main/assets/favicon/favicon-16x16.png', 'MotzzWebsite-main/sampling-info/assets/favicon/favicon-16x16.png'),
        ('MotzzWebsite-main/assets/favicon/site.webmanifest', 'MotzzWebsite-main/sampling-info/assets/favicon/site.webmanifest'),
        ('MotzzWebsite-main/assets/favicon/safari-pinned-tab.svg', 'MotzzWebsite-main/sampling-info/assets/favicon/safari-pinned-tab.svg'),
        ('MotzzWebsite-main/assets/favicon/favicon.ico', 'MotzzWebsite-main/sampling-info/assets/favicon/favicon.ico')
    ]
    
    for src, dst in favicon_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

if __name__ == "__main__":
    main()

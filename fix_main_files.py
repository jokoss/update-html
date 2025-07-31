import os
import shutil

def main():
    # Fix the main files
    fix_main_files()

def fix_main_files():
    # Create symlinks for the main files
    main_files = [
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/about-us/index.html'),
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/contact-us/index.html'),
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/laboratorytesting/index.html'),
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/sampling/index.html'),
        ('MotzzWebsite-main/index.html', 'MotzzWebsite-main/forms/index.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/about-us/analytical-testing.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/contact-us/analytical-testing.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/laboratorytesting/analytical-testing.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/sampling/analytical-testing.html'),
        ('MotzzWebsite-main/analytical-testing.html', 'MotzzWebsite-main/forms/analytical-testing.html')
    ]
    
    for src, dst in main_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

if __name__ == "__main__":
    main()

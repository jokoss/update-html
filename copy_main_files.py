import os
import shutil

def main():
    # Copy main files to subpages
    copy_main_files()

def copy_main_files():
    # Create copies of the main files
    main_files = [
        ('MotzzWebsite-main/forms.html', 'MotzzWebsite-main/about-us/forms.html'),
        ('MotzzWebsite-main/forms.html', 'MotzzWebsite-main/contact-us/forms.html'),
        ('MotzzWebsite-main/forms.html', 'MotzzWebsite-main/laboratorytesting/forms.html'),
        ('MotzzWebsite-main/forms.html', 'MotzzWebsite-main/sampling/forms.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/about-us/license-accreditations.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/contact-us/license-accreditations.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/laboratorytesting/license-accreditations.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/sampling/license-accreditations.html'),
        ('MotzzWebsite-main/license-accreditations.html', 'MotzzWebsite-main/forms/license-accreditations.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/about-us/professional-membership.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/contact-us/professional-membership.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/laboratorytesting/professional-membership.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/sampling/professional-membership.html'),
        ('MotzzWebsite-main/professional-membership.html', 'MotzzWebsite-main/forms/professional-membership.html'),
        ('MotzzWebsite-main/about-us.html', 'MotzzWebsite-main/contact-us/about-us.html'),
        ('MotzzWebsite-main/about-us.html', 'MotzzWebsite-main/laboratorytesting/about-us.html'),
        ('MotzzWebsite-main/about-us.html', 'MotzzWebsite-main/sampling/about-us.html'),
        ('MotzzWebsite-main/about-us.html', 'MotzzWebsite-main/forms/about-us.html'),
        ('MotzzWebsite-main/terms-conditions.html', 'MotzzWebsite-main/about-us/terms-conditions.html'),
        ('MotzzWebsite-main/terms-conditions.html', 'MotzzWebsite-main/contact-us/terms-conditions.html'),
        ('MotzzWebsite-main/terms-conditions.html', 'MotzzWebsite-main/laboratorytesting/terms-conditions.html'),
        ('MotzzWebsite-main/terms-conditions.html', 'MotzzWebsite-main/sampling/terms-conditions.html'),
        ('MotzzWebsite-main/terms-conditions.html', 'MotzzWebsite-main/forms/terms-conditions.html'),
        ('MotzzWebsite-main/privacy-policy.html', 'MotzzWebsite-main/about-us/privacy-policy.html'),
        ('MotzzWebsite-main/privacy-policy.html', 'MotzzWebsite-main/contact-us/privacy-policy.html'),
        ('MotzzWebsite-main/privacy-policy.html', 'MotzzWebsite-main/laboratorytesting/privacy-policy.html'),
        ('MotzzWebsite-main/privacy-policy.html', 'MotzzWebsite-main/sampling/privacy-policy.html'),
        ('MotzzWebsite-main/privacy-policy.html', 'MotzzWebsite-main/forms/privacy-policy.html')
    ]
    
    for src, dst in main_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"Copied {src} to {dst}")

if __name__ == "__main__":
    main()

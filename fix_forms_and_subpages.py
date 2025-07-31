import os
import re

def update_html_file(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply all replacements
    for old_text, new_text in replacements.items():
        content = content.replace(old_text, new_text)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")

def main():
    # Create forms directory and placeholder PDFs
    create_forms_directory()
    
    # Fix forms.html
    fix_forms_page()
    
    # Fix subpage header and footer
    fix_subpage_header_footer()

def create_forms_directory():
    # Create forms directory
    forms_dir = 'MotzzWebsite-main/forms'
    download_dir = os.path.join(forms_dir, 'download')
    
    if not os.path.exists(forms_dir):
        os.makedirs(forms_dir)
        print(f"Created directory: {forms_dir}")
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")
    
    # Create placeholder PDF files
    pdf_files = [
        'Client_Information.pdf',
        'Chain_of_Custody.pdf'
    ]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(download_dir, pdf_file)
        if not os.path.exists(pdf_path):
            # Create an empty file
            with open(pdf_path, 'wb') as f:
                # Write a minimal PDF header
                f.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000015 00000 n \n0000000060 00000 n \n0000000111 00000 n \ntrailer\n<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF\n')
            print(f"Created placeholder PDF: {pdf_path}")

def fix_forms_page():
    # Update forms.html
    forms_html = 'MotzzWebsite-main/forms.html'
    if os.path.exists(forms_html):
        replacements = {
            'sampling-info/sampling-information-water.html': './sampling-info/water.html',
            'sampling-info/sampling-information-soil.html': './sampling-info/soil.html',
            'href="/forms.html"': 'href="./forms.html"',
            'href="/terms-conditions.html"': 'href="./terms-conditions.html"',
            'href="/privacy-policy.html"': 'href="./privacy-policy.html"'
        }
        update_html_file(forms_html, replacements)

def fix_subpage_header_footer():
    # Fix subpage header and footer
    subpage_files = [
        'MotzzWebsite-main/subpage-header.html',
        'MotzzWebsite-main/subpage-footer.html'
    ]
    
    for file_path in subpage_files:
        if os.path.exists(file_path):
            replacements = {
                'href="../index.html"': 'href="../index.html"',
                'href="../analytical-testing.html"': 'href="../analytical-testing.html"',
                'href="../about-us.html"': 'href="../about-us.html"',
                'href="../license-accreditations.html"': 'href="../license-accreditations.html"',
                'href="../professional-membership.html"': 'href="../professional-membership.html"',
                'href="../forms.html"': 'href="../forms.html"',
                'href="../terms-conditions.html"': 'href="../terms-conditions.html"',
                'href="../privacy-policy.html"': 'href="../privacy-policy.html"',
                'src="../assets/': 'src="../assets/'
            }
            update_html_file(file_path, replacements)
    
    # Fix all subpages to use the correct header and footer loading
    subpage_dirs = [
        'MotzzWebsite-main/services',
        'MotzzWebsite-main/services/agriculture',
        'MotzzWebsite-main/sampling-info',
        'MotzzWebsite-main/about-us',
        'MotzzWebsite-main/contact-us',
        'MotzzWebsite-main/laboratorytesting',
        'MotzzWebsite-main/sampling'
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
                        # Already has the correct loading, skip
                        continue
                    
                    # Determine the relative path to the root
                    rel_path = '../'
                    if 'agriculture' in subpage_dir:
                        rel_path = '../../'
                    
                    # Add jQuery and header/footer loading
                    if '</body>' in content:
                        new_content = content.replace('</body>', f'''<script src="https://code.jquery.com/jquery-3.5.0.js"></script>
<script>
  $(function(){{
    $("#header").load("{rel_path}subpage-header.html"); 
    $("#footer").load("{rel_path}subpage-footer.html"); 
  }});
</script>
</body>''')
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"Added header/footer loading to {file_path}")

if __name__ == "__main__":
    main()

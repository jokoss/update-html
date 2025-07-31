import os
import re

def main():
    # Fix the paths in subpage header and footer
    fix_subpage_header_footer()
    
    # Create a proper forms directory structure
    create_forms_directory()

def fix_subpage_header_footer():
    # Read the main header and footer
    with open('MotzzWebsite-main/header.html', 'r', encoding='utf-8') as f:
        header_content = f.read()
    
    with open('MotzzWebsite-main/footer.html', 'r', encoding='utf-8') as f:
        footer_content = f.read()
    
    # Create subpage versions with proper paths
    subpage_header_content = header_content.replace('href="./', 'href="../')
    subpage_header_content = subpage_header_content.replace('src="./', 'src="../')
    
    subpage_footer_content = footer_content.replace('href="./', 'href="../')
    subpage_footer_content = subpage_footer_content.replace('src="./', 'src="../')
    
    # Write the updated subpage header and footer
    with open('MotzzWebsite-main/subpage-header.html', 'w', encoding='utf-8') as f:
        f.write(subpage_header_content)
    
    with open('MotzzWebsite-main/subpage-footer.html', 'w', encoding='utf-8') as f:
        f.write(subpage_footer_content)
    
    print("Updated subpage header and footer with proper paths")

def create_forms_directory():
    # Create forms directory structure
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
    
    # Create a forms index.html
    forms_index_path = os.path.join(forms_dir, 'index.html')
    if not os.path.exists(forms_index_path):
        with open(forms_index_path, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Motzz Laboratory - Forms</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" media="screen" href="../assets/css/theme.min.css">
    <link rel="stylesheet" media="screen" href="../assets/css/site.css">
  </head>
  <body>
    <header id="header" class="header">
      <!-- Header content will be loaded via JavaScript -->
    </header>
    
    <main class="page-wrapper">
      <section class="container py-5">
        <h1>Forms</h1>
        <p>Download our forms:</p>
        <ul>
          <li><a href="./download/Client_Information.pdf">Client Information Form</a></li>
          <li><a href="./download/Chain_of_Custody.pdf">Chain of Custody Form</a></li>
        </ul>
      </section>
    </main>
    
    <footer id="footer" class="footer bg-secondary pt-5 pb-4 pb-lg-5">
      <!-- Footer content will be loaded via JavaScript -->
    </footer>
    
    <script src="https://code.jquery.com/jquery-3.5.0.js"></script>
    <script>
      $(function(){
        $("#header").load("../subpage-header.html"); 
        $("#footer").load("../subpage-footer.html"); 
      });
    </script>
    <script src="../assets/vendor/bootstrap/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../assets/js/theme.min.js"></script>
  </body>
</html>''')
        print(f"Created forms index.html: {forms_index_path}")

if __name__ == "__main__":
    main()

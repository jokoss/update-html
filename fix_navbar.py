import os
import re

def main():
    # Fix navbar on subpages
    fix_navbar_on_subpages()

def fix_navbar_on_subpages():
    # Update all subpages to use the dynamic header and footer
    subpage_dirs = [
        'MotzzWebsite-main/about-us',
        'MotzzWebsite-main/contact-us',
        'MotzzWebsite-main/laboratorytesting',
        'MotzzWebsite-main/sampling',
        'MotzzWebsite-main/forms',
        'MotzzWebsite-main/services'
    ]
    
    for subpage_dir in subpage_dirs:
        if os.path.exists(subpage_dir):
            for file in os.listdir(subpage_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(subpage_dir, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace static header with placeholder
                    header_pattern = r'<header.*?</header>'
                    if re.search(header_pattern, content, re.DOTALL):
                        content = re.sub(header_pattern, '<header id="header"></header>', content, flags=re.DOTALL)
                        print(f"Replaced static header with placeholder in {file_path}")
                    
                    # Replace static footer with placeholder if it exists
                    footer_pattern = r'<footer.*?</footer>'
                    if re.search(footer_pattern, content, re.DOTALL):
                        content = re.sub(footer_pattern, '<footer id="footer"></footer>', content, flags=re.DOTALL)
                        print(f"Replaced static footer with placeholder in {file_path}")
                    
                    # Add jQuery code to load header and footer if it doesn't exist
                    jquery_code = '''
<script src="https://code.jquery.com/jquery-3.5.0.js"></script>
<script>
  $(function(){
    $("#header").load("../header.html"); 
    $("#footer").load("../footer.html"); 
  });
</script>
'''
                    if 'jQuery' not in content and '$(function(){' not in content:
                        # Add before closing body tag
                        content = content.replace('</body>', jquery_code + '</body>')
                        print(f"Added jQuery code to load header and footer in {file_path}")
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    main()

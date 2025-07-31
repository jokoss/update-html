import os
import re

def main():
    # Fix nested subdirectories
    fix_nested_subdirectories()
    print("Nested subdirectories fixed successfully!")

def fix_nested_subdirectories():
    # Update all nested subdirectories to fix CSS and JS includes
    nested_subpage_dirs = [
        'MotzzWebsite-main/services/agriculture'
    ]
    
    for subpage_dir in nested_subpage_dirs:
        if os.path.exists(subpage_dir):
            for file in os.listdir(subpage_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(subpage_dir, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Remove meta refresh tag if it exists
                    meta_refresh_pattern = r'<meta\s+http-equiv="refresh".*?/>'
                    if re.search(meta_refresh_pattern, content, re.DOTALL | re.IGNORECASE):
                        content = re.sub(meta_refresh_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
                        print(f"Removed meta refresh tag from {file_path}")
                    
                    # Fix CSS paths
                    content = content.replace('href="assets/css/', 'href="../../assets/css/')
                    content = content.replace('href="assets/vendor/', 'href="../../assets/vendor/')
                    content = content.replace('href="assets/favicon/', 'href="../../assets/favicon/')
                    
                    # Fix JS paths
                    content = content.replace('src="assets/js/', 'src="../../assets/js/')
                    content = content.replace('src="assets/vendor/', 'src="../../assets/vendor/')
                    
                    # Define head_end_tag
                    head_end_tag = '</head>'
                    
                    # Add jQuery to the head section if not already present
                    jquery_script = '<script src="https://code.jquery.com/jquery-3.5.0.js"></script>'
                    if jquery_script not in content and head_end_tag in content:
                        content = content.replace(head_end_tag, f'{jquery_script}\n  {head_end_tag}')
                        print(f"Added jQuery to head in {file_path}")
                    
                    # Add header and footer placeholders if not already present
                    if '<header id="header"></header>' not in content:
                        # Find the main content div or body tag
                        main_content_pattern = r'<main class="page-wrapper">'
                        if re.search(main_content_pattern, content, re.DOTALL):
                            content = re.sub(main_content_pattern, '<main class="page-wrapper">\n\n      <!-- Navbar -->\n      <header id="header"></header>\n      \n      <div class="container headerspacer">\n        &nbsp;\n      </div>', content, flags=re.DOTALL)
                            print(f"Added header placeholder to {file_path}")
                    
                    if '<footer id="footer"></footer>' not in content:
                        # Find the closing main tag
                        main_end_pattern = r'</main>'
                        if re.search(main_end_pattern, content, re.DOTALL):
                            content = re.sub(main_end_pattern, '</main>\n\n    <!-- Footer -->\n    <footer id="footer"></footer>', content, flags=re.DOTALL)
                            print(f"Added footer placeholder to {file_path}")
                    
                    # Add jQuery load script for header and footer
                    jquery_load_script = '''<script>
  $(function(){
    $("#header").load("../../header.html"); 
    $("#footer").load("../../footer.html"); 
  });
</script>'''
                    
                    # Remove existing jQuery load script if it exists
                    if '$(function(){' in content and '$("#header").load(' in content:
                        # Use regex to find and remove the script
                        jquery_load_pattern = r'<script>\s*\$\(function\(\)\{\s*\$\("#header"\)\.load\(.*?\);\s*\$\("#footer"\)\.load\(.*?\);\s*\}\);\s*</script>'
                        content = re.sub(jquery_load_pattern, '', content, flags=re.DOTALL)
                    
                    # Add jQuery load script after jQuery is loaded in head
                    if head_end_tag in content and jquery_script in content and jquery_load_script not in content:
                        content = content.replace(head_end_tag, f'{jquery_load_script}\n  {head_end_tag}')
                        print(f"Added jQuery load script to head in {file_path}")
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    main()

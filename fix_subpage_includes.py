import os
import re

def main():
    # Fix subpage includes
    fix_subpage_includes()

def fix_subpage_includes():
    # Update all subpages to fix CSS and JS includes
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
                    
                    # Remove meta refresh tag if it exists
                    meta_refresh_pattern = r'<meta\s+http-equiv="refresh".*?/>'
                    if re.search(meta_refresh_pattern, content, re.DOTALL | re.IGNORECASE):
                        content = re.sub(meta_refresh_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
                        print(f"Removed meta refresh tag from {file_path}")
                    
                    # Fix CSS paths
                    content = content.replace('href="assets/css/', 'href="../assets/css/')
                    content = content.replace('href="assets/vendor/', 'href="../assets/vendor/')
                    content = content.replace('href="assets/favicon/', 'href="../assets/favicon/')
                    
                    # Fix JS paths
                    content = content.replace('src="assets/js/', 'src="../assets/js/')
                    content = content.replace('src="assets/vendor/', 'src="../assets/vendor/')
                    
                    # Move jQuery to the head section
                    jquery_script = '<script src="https://code.jquery.com/jquery-3.5.0.js"></script>'
                    if jquery_script in content:
                        content = content.replace(jquery_script, '')
                        # Add jQuery to head
                        head_end_tag = '</head>'
                        if head_end_tag in content:
                            content = content.replace(head_end_tag, f'{jquery_script}\n  {head_end_tag}')
                            print(f"Moved jQuery to head in {file_path}")
                    
                    # Ensure jQuery is loaded before it's used
                    jquery_load_script = '''<script>
  $(function(){
    $("#header").load("../header.html"); 
    $("#footer").load("../footer.html"); 
  });
</script>'''
                    
                    # Remove existing jQuery load script if it exists
                    if '$(function(){' in content and '$("#header").load(' in content:
                        # Use regex to find and remove the script
                        jquery_load_pattern = r'<script>\s*\$\(function\(\)\{\s*\$\("#header"\)\.load\(.*?\);\s*\$\("#footer"\)\.load\(.*?\);\s*\}\);\s*</script>'
                        content = re.sub(jquery_load_pattern, '', content, flags=re.DOTALL)
                    
                    # Add jQuery load script after jQuery is loaded in head
                    if head_end_tag in content and jquery_script in content:
                        content = content.replace(head_end_tag, f'{jquery_load_script}\n  {head_end_tag}')
                        print(f"Added jQuery load script to head in {file_path}")
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated {file_path}")

if __name__ == "__main__":
    main()

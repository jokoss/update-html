import os
import re

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine the relative path to the root
    rel_path = os.path.relpath('MotzzWebsite-main', os.path.dirname(file_path))
    if rel_path == '.':
        rel_path = '.'
    else:
        rel_path = '..'
    
    # Replace absolute paths with relative paths
    content = content.replace('href="/assets/', f'href="{rel_path}/assets/')
    content = content.replace('src="/assets/', f'src="{rel_path}/assets/')
    
    # Update header and footer loading
    content = content.replace('$("#header").load("/header.html")', f'$("#header").load("{rel_path}/subpage-header.html")')
    content = content.replace('$("#footer").load("/footer.html")', f'$("#footer").load("{rel_path}/subpage-footer.html")')
    
    # Update script and CSS paths
    content = content.replace('src="/assets/', f'src="{rel_path}/assets/')
    
    # Update navigation links
    content = content.replace('href="/index.html"', f'href="{rel_path}/index.html"')
    content = content.replace('href="/analytical-testing.html"', f'href="{rel_path}/analytical-testing.html"')
    content = content.replace('href="/about-us.html"', f'href="{rel_path}/about-us.html"')
    content = content.replace('href="/license-accreditations.html"', f'href="{rel_path}/license-accreditations.html"')
    content = content.replace('href="/professional-membership.html"', f'href="{rel_path}/professional-membership.html"')
    
    # Add header and footer placeholders if they don't exist
    if '<header id="header" class="header"></header>' in content:
        content = content.replace('<header id="header" class="header"></header>', 
                                 '<header id="header" class="header">\n        <!-- Header content will be loaded via JavaScript -->\n      </header>')
    
    if '<footer id="footer" class="footer bg-secondary pt-5 pb-4 pb-lg-5"></footer>' in content:
        content = content.replace('<footer id="footer" class="footer bg-secondary pt-5 pb-4 pb-lg-5"></footer>', 
                                 '<footer id="footer" class="footer bg-secondary pt-5 pb-4 pb-lg-5">\n      <!-- Footer content will be loaded via JavaScript -->\n    </footer>')
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")

def main():
    # Update all HTML files in the services directory
    services_dir = 'MotzzWebsite-main/services'
    for root, dirs, files in os.walk(services_dir):
        for file in files:
            if file.endswith('.html'):
                update_html_file(os.path.join(root, file))
    
    # Update all HTML files in the sampling-info directory
    sampling_dir = 'MotzzWebsite-main/sampling-info'
    if os.path.exists(sampling_dir):
        for root, dirs, files in os.walk(sampling_dir):
            for file in files:
                if file.endswith('.html'):
                    update_html_file(os.path.join(root, file))

if __name__ == "__main__":
    main()

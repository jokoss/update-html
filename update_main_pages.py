import os
import re

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace absolute paths with relative paths
    content = content.replace('href="/assets/', 'href="./assets/')
    content = content.replace('src="/assets/', 'src="./assets/')
    
    # Update script and CSS paths
    content = content.replace('src="/assets/', 'src="./assets/')
    
    # Update navigation links
    content = content.replace('href="/index.html"', 'href="./index.html"')
    content = content.replace('href="/analytical-testing.html"', 'href="./analytical-testing.html"')
    content = content.replace('href="/about-us.html"', 'href="./about-us.html"')
    content = content.replace('href="/license-accreditations.html"', 'href="./license-accreditations.html"')
    content = content.replace('href="/professional-membership.html"', 'href="./professional-membership.html"')
    content = content.replace('href="/contact-us/', 'href="./contact-us/')
    content = content.replace('href="/services/', 'href="./services/')
    content = content.replace('href="/sampling-info/', 'href="./sampling-info/')
    content = content.replace('href="/forms/', 'href="./forms/')
    
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
    # Update main HTML files in the root directory
    root_dir = 'MotzzWebsite-main'
    for file in os.listdir(root_dir):
        if file.endswith('.html') and file not in ['header.html', 'footer.html', 'subpage-header.html', 'subpage-footer.html']:
            update_html_file(os.path.join(root_dir, file))

if __name__ == "__main__":
    main()

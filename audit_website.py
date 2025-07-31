import os
import re
from collections import defaultdict

def main():
    # Audit the website
    audit_website()

def audit_website():
    # Base directory
    base_dir = 'MotzzWebsite-main'
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f'Found {len(html_files)} HTML files')
    
    # Check for jQuery include
    jquery_inclusion = []
    jquery_missing = []
    
    # Check for header and footer placeholders
    header_placeholder = []
    header_missing = []
    footer_placeholder = []
    footer_missing = []
    
    # Check for header and footer loading code
    header_loading = []
    header_loading_missing = []
    footer_loading = []
    footer_loading_missing = []
    
    # Check for CSS and JS includes
    css_inclusion = defaultdict(list)
    js_inclusion = defaultdict(list)
    
    # Check for Bootstrap JS
    bootstrap_js = []
    bootstrap_js_missing = []
    
    # Check for issues in subpages
    subpage_dirs = [
        os.path.join(base_dir, 'about-us'),
        os.path.join(base_dir, 'contact-us'),
        os.path.join(base_dir, 'laboratorytesting'),
        os.path.join(base_dir, 'sampling'),
        os.path.join(base_dir, 'forms'),
        os.path.join(base_dir, 'services')
    ]
    
    subpage_files = []
    for subpage_dir in subpage_dirs:
        if os.path.exists(subpage_dir):
            for file in os.listdir(subpage_dir):
                if file.endswith('.html'):
                    subpage_files.append(os.path.join(subpage_dir, file))
    
    print(f'Found {len(subpage_files)} subpage HTML files')
    
    # Check each subpage file
    for html_file in subpage_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for jQuery include
            if 'jquery' in content.lower():
                jquery_inclusion.append(html_file)
            else:
                jquery_missing.append(html_file)
            
            # Check for header placeholder
            if '<header id="header"></header>' in content:
                header_placeholder.append(html_file)
            else:
                header_missing.append(html_file)
            
            # Check for footer placeholder
            if '<footer id="footer"></footer>' in content:
                footer_placeholder.append(html_file)
            else:
                footer_missing.append(html_file)
            
            # Check for header loading code
            if '$("#header").load(' in content:
                header_loading.append(html_file)
            else:
                header_loading_missing.append(html_file)
            
            # Check for footer loading code
            if '$("#footer").load(' in content:
                footer_loading.append(html_file)
            else:
                footer_loading_missing.append(html_file)
            
            # Check for CSS includes
            if 'site.css' in content:
                css_inclusion['site.css'].append(html_file)
            if 'theme.min.css' in content:
                css_inclusion['theme.min.css'].append(html_file)
            
            # Check for JS includes
            if 'theme.min.js' in content:
                js_inclusion['theme.min.js'].append(html_file)
            
            # Check for Bootstrap JS
            if 'bootstrap.bundle.min.js' in content:
                bootstrap_js.append(html_file)
            else:
                bootstrap_js_missing.append(html_file)
    
    # Print results
    print('\nJQuery Inclusion:')
    print(f'Included in {len(jquery_inclusion)}/{len(subpage_files)} files')
    if jquery_missing:
        print(f'Missing in {len(jquery_missing)} files:')
        for file in jquery_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(jquery_missing) > 5:
            print(f'  ... and {len(jquery_missing) - 5} more files')
    
    print('\nHeader Placeholder:')
    print(f'Present in {len(header_placeholder)}/{len(subpage_files)} files')
    if header_missing:
        print(f'Missing in {len(header_missing)} files:')
        for file in header_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(header_missing) > 5:
            print(f'  ... and {len(header_missing) - 5} more files')
    
    print('\nFooter Placeholder:')
    print(f'Present in {len(footer_placeholder)}/{len(subpage_files)} files')
    if footer_missing:
        print(f'Missing in {len(footer_missing)} files:')
        for file in footer_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(footer_missing) > 5:
            print(f'  ... and {len(footer_missing) - 5} more files')
    
    print('\nHeader Loading Code:')
    print(f'Present in {len(header_loading)}/{len(subpage_files)} files')
    if header_loading_missing:
        print(f'Missing in {len(header_loading_missing)} files:')
        for file in header_loading_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(header_loading_missing) > 5:
            print(f'  ... and {len(header_loading_missing) - 5} more files')
    
    print('\nFooter Loading Code:')
    print(f'Present in {len(footer_loading)}/{len(subpage_files)} files')
    if footer_loading_missing:
        print(f'Missing in {len(footer_loading_missing)} files:')
        for file in footer_loading_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(footer_loading_missing) > 5:
            print(f'  ... and {len(footer_loading_missing) - 5} more files')
    
    print('\nCSS Inclusion:')
    for css, files in css_inclusion.items():
        print(f'{css}: {len(files)}/{len(subpage_files)} files')
        missing = set(subpage_files) - set(files)
        if missing:
            print(f'  Missing in {len(missing)} files:')
            for file in list(missing)[:5]:
                print(f'    {os.path.relpath(file, base_dir)}')
            if len(missing) > 5:
                print(f'    ... and {len(missing) - 5} more files')
    
    print('\nJS Inclusion:')
    for js, files in js_inclusion.items():
        print(f'{js}: {len(files)}/{len(subpage_files)} files')
        missing = set(subpage_files) - set(files)
        if missing:
            print(f'  Missing in {len(missing)} files:')
            for file in list(missing)[:5]:
                print(f'    {os.path.relpath(file, base_dir)}')
            if len(missing) > 5:
                print(f'    ... and {len(missing) - 5} more files')
    
    print('\nBootstrap JS:')
    print(f'Included in {len(bootstrap_js)}/{len(subpage_files)} files')
    if bootstrap_js_missing:
        print(f'Missing in {len(bootstrap_js_missing)} files:')
        for file in bootstrap_js_missing[:5]:
            print(f'  {os.path.relpath(file, base_dir)}')
        if len(bootstrap_js_missing) > 5:
            print(f'  ... and {len(bootstrap_js_missing) - 5} more files')

if __name__ == "__main__":
    main()

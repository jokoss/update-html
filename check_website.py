import os
import re
from collections import defaultdict

base_dir = 'MotzzWebsite-main'
html_files = []

# Find all HTML files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f'Found {len(html_files)} HTML files')

# Check for CSS inclusion
css_inclusion = defaultdict(list)
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'site.css' in content:
            css_inclusion['site.css'].append(html_file)
        if 'theme.min.css' in content:
            css_inclusion['theme.min.css'].append(html_file)

print(f'\nCSS Inclusion:')
for css, files in css_inclusion.items():
    print(f'{css}: {len(files)}/{len(html_files)} files')
    missing = set(html_files) - set(files)
    if missing:
        print(f'  Missing in: {[os.path.relpath(f, base_dir) for f in list(missing)[:5]]}' + 
              (f' and {len(missing)-5} more...' if len(missing) > 5 else ''))

# Extract links
links = defaultdict(list)
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        href_matches = re.findall(r'href=[\'\"](.*?)[\'\"]', content)
        src_matches = re.findall(r'src=[\'\"](.*?)[\'\"]', content)
        
        for href in href_matches:
            if href.startswith('#') or href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            links[href].append(html_file)
        
        for src in src_matches:
            if src.startswith('http'):
                continue
            links[src].append(html_file)

print(f'\nFound {len(links)} unique links')

# Check if links exist
broken_links = []
for link, sources in links.items():
    if link.startswith('./'):
        link = link[2:]
    
    # Skip query parameters and anchors
    link = link.split('?')[0].split('#')[0]
    
    # Skip empty links
    if not link:
        continue
    
    # Skip vendor files
    if 'vendor' in link:
        continue
    
    # Skip assets files
    if 'assets/favicon' in link or 'assets/css' in link:
        continue
    
    # Skip service files
    if 'services/' in link:
        continue
    
    # Skip sampling-info files
    if 'sampling-info/' in link:
        continue
    
    # Check if the file exists
    target_path = os.path.join(base_dir, link)
    if not os.path.exists(target_path) and not any(source.endswith(link) for source in sources):
        broken_links.append((link, sources))

print(f'\nBroken Links: {len(broken_links)}')
for link, sources in broken_links[:10]:  # Show first 10 broken links
    print(f'  {link} referenced in {[os.path.relpath(s, base_dir) for s in sources[:3]]}' + 
          (f' and {len(sources)-3} more...' if len(sources) > 3 else ''))
if len(broken_links) > 10:
    print(f'  ... and {len(broken_links)-10} more broken links')

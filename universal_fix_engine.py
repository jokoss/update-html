#!/usr/bin/env python3
"""
Universal Fix Engine
Automated repair system for all website navigation issues
"""

import os
import re
import json
from pathlib import Path

class UniversalFixEngine:
    def __init__(self, base_directory, diagnostic_report_file=None):
        self.base_directory = base_directory
        self.fixes_applied = []
        self.statistics = {
            'files_processed': 0,
            'files_fixed': 0,
            'critical_fixes': 0,
            'warning_fixes': 0,
            'info_fixes': 0
        }
        
        # Load diagnostic report if available
        self.diagnostic_report = None
        if diagnostic_report_file and os.path.exists(diagnostic_report_file):
            with open(diagnostic_report_file, 'r') as f:
                self.diagnostic_report = json.load(f)
    
    def calculate_relative_path(self, file_path):
        """Calculate the relative path from a file to the base directory."""
        file_dir = os.path.dirname(file_path)
        rel_path = os.path.relpath(self.base_directory, file_dir)
        rel_path = rel_path.replace('\\', '/')
        
        if rel_path == '.':
            return './'
        elif not rel_path.endswith('/'):
            return rel_path + '/'
        return rel_path
    
    def is_template_file(self, file_path):
        """Check if file is a template/partial file that shouldn't have full navigation."""
        filename = os.path.basename(file_path).lower()
        template_indicators = [
            'header.html', 'footer.html', 'subpage-header.html', 'subpage-footer.html',
            'template', 'partial', 'include'
        ]
        return any(indicator in filename for indicator in template_indicators)
    
    def is_vendor_file(self, file_path):
        """Check if file is a vendor/library file that shouldn't be modified."""
        return 'vendor' in file_path.lower() or 'assets' in file_path.lower()
    
    def should_skip_file(self, file_path):
        """Determine if a file should be skipped from navigation fixes."""
        return self.is_template_file(file_path) or self.is_vendor_file(file_path)
    
    def add_header_div(self, content, file_path):
        """Add header div to content if missing."""
        if 'id="header"' in content:
            return content, False
        
        # Skip template files
        if self.should_skip_file(file_path):
            return content, False
        
        # Find the best place to insert header div
        if '<main class="page-wrapper">' in content:
            # Insert after main opening tag
            content = content.replace(
                '<main class="page-wrapper">',
                '<main class="page-wrapper">\n      <div id="header"></div>'
            )
        elif '<body>' in content:
            # Insert after body opening tag
            content = content.replace(
                '<body>',
                '<body>\n    <div id="header"></div>'
            )
        elif '<div class="page-loading' in content:
            # Insert after page loading div
            pattern = r'(<div class="page-loading[^>]*>.*?</div>)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                content = content.replace(
                    match.group(1),
                    match.group(1) + '\n\n    <div id="header"></div>'
                )
        else:
            # Fallback: insert at the beginning of body content
            body_match = re.search(r'<body[^>]*>', content)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n    <div id="header"></div>' + content[insert_pos:]
        
        return content, True
    
    def add_footer_div(self, content, file_path):
        """Add footer div to content if missing."""
        if 'id="footer"' in content:
            return content, False
        
        # Skip template files
        if self.should_skip_file(file_path):
            return content, False
        
        # Find the best place to insert footer div
        if '</main>' in content:
            # Insert before main closing tag
            content = content.replace(
                '</main>',
                '      <div id="footer"></div>\n    </main>'
            )
        elif '</body>' in content:
            # Insert before body closing tag
            content = content.replace(
                '</body>',
                '    <div id="footer"></div>\n  </body>'
            )
        else:
            # Fallback: append before closing body
            body_close = content.rfind('</body>')
            if body_close != -1:
                content = content[:body_close] + '    <div id="footer"></div>\n  ' + content[body_close:]
        
        return content, True
    
    def add_navigation_script(self, content, file_path):
        """Add include-nav.js script if missing."""
        if 'include-nav.js' in content:
            return content, False
        
        # Skip template files
        if self.should_skip_file(file_path):
            return content, False
        
        rel_path = self.calculate_relative_path(file_path)
        script_tag = f'<script src="{rel_path}assets/js/include-nav.js"></script>'
        
        # Insert before closing body tag
        if '</body>' in content:
            content = content.replace('</body>', f'    {script_tag}\n</body>')
        else:
            # Fallback: append to end
            content += f'\n{script_tag}'
        
        return content, True
    
    def fix_asset_paths(self, content, file_path):
        """Fix asset paths to use correct relative paths."""
        rel_path = self.calculate_relative_path(file_path)
        changes_made = False
        
        # Skip if already using correct path
        if rel_path == './':
            return content, False
        
        # Fix CSS paths
        css_pattern = r'href="\.\/assets\/'
        if re.search(css_pattern, content):
            content = re.sub(css_pattern, f'href="{rel_path}assets/', content)
            changes_made = True
        
        # Fix JS paths
        js_pattern = r'src="\.\/assets\/'
        if re.search(js_pattern, content):
            content = re.sub(js_pattern, f'src="{rel_path}assets/', content)
            changes_made = True
        
        # Fix image paths
        img_pattern = r'src="\.\/assets\/'
        if re.search(img_pattern, content):
            content = re.sub(img_pattern, f'src="{rel_path}assets/', content)
            changes_made = True
        
        # Fix absolute paths
        if '/assets/' in content:
            content = content.replace('/assets/', f'{rel_path}assets/')
            changes_made = True
        
        return content, changes_made
    
    def remove_jquery_navigation(self, content):
        """Remove jQuery navigation code."""
        changes_made = False
        
        # Remove jQuery CDN
        jquery_cdn_pattern = r'<script src="https://code\.jquery\.com/jquery-[^"]*"></script>\s*'
        if re.search(jquery_cdn_pattern, content):
            content = re.sub(jquery_cdn_pattern, '', content)
            changes_made = True
        
        # Remove jQuery navigation code
        jquery_nav_patterns = [
            r'<script>\s*\$\(function\(\)\{\s*\$\("#header"\)\.load\("[^"]*"\);\s*\$\("#footer"\)\.load\("[^"]*"\);\s*\}\);\s*</script>',
            r'\$\(function\(\)\{\s*\$\("#header"\)\.load\("[^"]*"\);\s*\$\("#footer"\)\.load\("[^"]*"\);\s*\}\);'
        ]
        
        for pattern in jquery_nav_patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                changes_made = True
        
        return content, changes_made
    
    def fix_malformed_elements(self, content):
        """Fix malformed HTML elements."""
        changes_made = False
        
        # Fix escaped quotes in header tags
        malformed_patterns = [
            (r'<header id=\\"header\\"></header>', '<div id="header"></div>'),
            (r'<footer id=\\"footer\\"></footer>', '<div id="footer"></div>'),
            (r'<header id="header"></header>', '<div id="header"></div>'),
            (r'<footer id="footer"></footer>', '<div id="footer"></div>')
        ]
        
        for pattern, replacement in malformed_patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes_made = True
        
        return content, changes_made
    
    def clean_whitespace(self, content):
        """Clean up excessive whitespace."""
        # Remove excessive blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        return content
    
    def fix_single_file(self, file_path):
        """Apply all fixes to a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content = original_content
            fixes_applied = []
            
            # Apply all fixes
            content, changed = self.remove_jquery_navigation(content)
            if changed:
                fixes_applied.append('Removed jQuery navigation')
            
            content, changed = self.fix_malformed_elements(content)
            if changed:
                fixes_applied.append('Fixed malformed elements')
            
            content, changed = self.add_header_div(content, file_path)
            if changed:
                fixes_applied.append('Added header div')
            
            content, changed = self.add_footer_div(content, file_path)
            if changed:
                fixes_applied.append('Added footer div')
            
            content, changed = self.add_navigation_script(content, file_path)
            if changed:
                fixes_applied.append('Added navigation script')
            
            content, changed = self.fix_asset_paths(content, file_path)
            if changed:
                fixes_applied.append('Fixed asset paths')
            
            # Clean up whitespace
            content = self.clean_whitespace(content)
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.fixes_applied.append({
                    'file': file_path,
                    'fixes': fixes_applied
                })
                
                print(f"  ✅ Fixed: {', '.join(fixes_applied)}")
                return True
            else:
                print(f"  ✓ No changes needed")
                return False
                
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
            return False
    
    def find_all_html_files(self):
        """Find all HTML files to process."""
        html_files = []
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        return html_files
    
    def run_universal_fix(self):
        """Run the universal fix engine on all files."""
        print("🔧 UNIVERSAL FIX ENGINE")
        print("=" * 50)
        
        html_files = self.find_all_html_files()
        print(f"📁 Found {len(html_files)} HTML files to process")
        print()
        
        fixed_files = 0
        for i, html_file in enumerate(html_files, 1):
            print(f"[{i:2d}/{len(html_files)}] Processing: {html_file}")
            
            if self.fix_single_file(html_file):
                fixed_files += 1
            
            self.statistics['files_processed'] += 1
        
        self.statistics['files_fixed'] = fixed_files
        
        print(f"\n📊 FIX ENGINE RESULTS:")
        print(f"   Files Processed: {self.statistics['files_processed']}")
        print(f"   Files Fixed: {self.statistics['files_fixed']}")
        print(f"   Total Fixes Applied: {len(self.fixes_applied)}")
        
        # Save fix report
        fix_report = {
            'statistics': self.statistics,
            'fixes_applied': self.fixes_applied
        }
        
        with open('fix_report.json', 'w') as f:
            json.dump(fix_report, f, indent=2)
        
        print(f"\n💾 Fix report saved to: fix_report.json")
        print(f"🚀 Ready for Phase 3: Comprehensive Website Validation")
        
        return fix_report

def main():
    base_directory = "MotzzWebsite-main"
    
    if not os.path.exists(base_directory):
        print(f"❌ Error: Directory {base_directory} not found!")
        return
    
    # Load diagnostic report if available
    diagnostic_file = "diagnostic_report.json"
    
    fix_engine = UniversalFixEngine(base_directory, diagnostic_file)
    fix_report = fix_engine.run_universal_fix()

if __name__ == "__main__":
    main()

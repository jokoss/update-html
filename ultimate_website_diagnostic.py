#!/usr/bin/env python3
"""
Ultimate Website Diagnostic System
Comprehensive analysis and detection of all website issues
"""

import os
import re
from pathlib import Path
import json
from urllib.parse import urljoin, urlparse

class WebsiteDiagnostic:
    def __init__(self, base_directory):
        self.base_directory = base_directory
        self.issues = []
        self.html_files = []
        self.statistics = {
            'total_files': 0,
            'files_with_issues': 0,
            'critical_issues': 0,
            'warning_issues': 0,
            'info_issues': 0
        }
        
    def find_all_html_files(self):
        """Find all HTML files in the directory structure."""
        html_files = []
        for root, dirs, files in os.walk(self.base_directory):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        return html_files
    
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
    
    def add_issue(self, file_path, issue_type, severity, description, fix_suggestion=None):
        """Add an issue to the issues list."""
        issue = {
            'file': file_path,
            'type': issue_type,
            'severity': severity,  # 'critical', 'warning', 'info'
            'description': description,
            'fix_suggestion': fix_suggestion
        }
        self.issues.append(issue)
        self.statistics[f'{severity}_issues'] += 1
    
    def analyze_html_structure(self, file_path, content):
        """Analyze HTML structure for navigation issues."""
        issues_found = False
        
        # Check for header div
        if 'id="header"' not in content:
            self.add_issue(
                file_path, 
                'missing_header_div', 
                'critical',
                'Missing header div element',
                'Add <div id="header"></div> in appropriate location'
            )
            issues_found = True
        
        # Check for footer div
        if 'id="footer"' not in content:
            self.add_issue(
                file_path, 
                'missing_footer_div', 
                'warning',
                'Missing footer div element',
                'Add <div id="footer"></div> before closing body tag'
            )
            issues_found = True
        
        # Check for include-nav.js
        if 'include-nav.js' not in content:
            self.add_issue(
                file_path, 
                'missing_navigation_script', 
                'critical',
                'Missing include-nav.js script',
                'Add <script src="[path]/assets/js/include-nav.js"></script>'
            )
            issues_found = True
        
        # Check for jQuery conflicts
        if 'jquery' in content.lower() and ('$("#header")' in content or '$("#footer")' in content):
            self.add_issue(
                file_path, 
                'jquery_navigation_conflict', 
                'critical',
                'Conflicting jQuery navigation system detected',
                'Remove jQuery navigation code and use include-nav.js only'
            )
            issues_found = True
        
        # Check for malformed header tags
        if re.search(r'<header id=\\"header\\">', content):
            self.add_issue(
                file_path, 
                'malformed_header_tag', 
                'critical',
                'Malformed header tag with escaped quotes',
                'Replace with proper <div id="header"></div>'
            )
            issues_found = True
        
        return issues_found
    
    def analyze_asset_paths(self, file_path, content):
        """Analyze asset path consistency."""
        issues_found = False
        expected_path = self.calculate_relative_path(file_path)
        
        # Check CSS paths
        css_matches = re.findall(r'href="([^"]*\.css)"', content)
        for css_path in css_matches:
            if css_path.startswith('./assets/') and expected_path != './':
                self.add_issue(
                    file_path, 
                    'incorrect_css_path', 
                    'warning',
                    f'CSS path "{css_path}" should be "{expected_path}assets/..."',
                    f'Update to href="{expected_path}assets/..."'
                )
                issues_found = True
        
        # Check JS paths
        js_matches = re.findall(r'src="([^"]*\.js)"', content)
        for js_path in js_matches:
            if js_path.startswith('./assets/') and expected_path != './':
                self.add_issue(
                    file_path, 
                    'incorrect_js_path', 
                    'warning',
                    f'JS path "{js_path}" should be "{expected_path}assets/..."',
                    f'Update to src="{expected_path}assets/..."'
                )
                issues_found = True
        
        # Check image paths
        img_matches = re.findall(r'src="([^"]*\.(jpg|jpeg|png|gif|svg))"', content)
        for img_path, ext in img_matches:
            if img_path.startswith('./assets/') and expected_path != './':
                self.add_issue(
                    file_path, 
                    'incorrect_image_path', 
                    'info',
                    f'Image path "{img_path}" should be "{expected_path}assets/..."',
                    f'Update to src="{expected_path}assets/..."'
                )
                issues_found = True
        
        return issues_found
    
    def analyze_navigation_links(self, file_path, content):
        """Analyze navigation link consistency."""
        issues_found = False
        expected_path = self.calculate_relative_path(file_path)
        
        # Check for hardcoded absolute paths
        if '/assets/' in content:
            self.add_issue(
                file_path, 
                'absolute_asset_paths', 
                'warning',
                'Contains absolute asset paths that may break in subdirectories',
                'Convert to relative paths'
            )
            issues_found = True
        
        # Check internal links
        internal_links = re.findall(r'href="([^"]*\.html)"', content)
        for link in internal_links:
            if link.startswith('./') and expected_path != './':
                # This might need adjustment based on directory depth
                pass  # Will be handled by the fix engine
        
        return issues_found
    
    def check_file_existence(self, file_path, content):
        """Check if referenced files actually exist."""
        issues_found = False
        base_dir = os.path.dirname(file_path)
        
        # Check CSS files
        css_files = re.findall(r'href="([^"]*\.css)"', content)
        for css_file in css_files:
            if not css_file.startswith('http'):
                full_path = os.path.join(base_dir, css_file)
                if not os.path.exists(full_path):
                    self.add_issue(
                        file_path, 
                        'missing_css_file', 
                        'critical',
                        f'Referenced CSS file does not exist: {css_file}',
                        'Check file path or create missing file'
                    )
                    issues_found = True
        
        # Check JS files
        js_files = re.findall(r'src="([^"]*\.js)"', content)
        for js_file in js_files:
            if not js_file.startswith('http'):
                full_path = os.path.join(base_dir, js_file)
                if not os.path.exists(full_path):
                    self.add_issue(
                        file_path, 
                        'missing_js_file', 
                        'critical',
                        f'Referenced JS file does not exist: {js_file}',
                        'Check file path or create missing file'
                    )
                    issues_found = True
        
        return issues_found
    
    def analyze_single_file(self, file_path):
        """Analyze a single HTML file for all types of issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_has_issues = False
            
            # Run all analysis functions
            if self.analyze_html_structure(file_path, content):
                file_has_issues = True
            
            if self.analyze_asset_paths(file_path, content):
                file_has_issues = True
            
            if self.analyze_navigation_links(file_path, content):
                file_has_issues = True
            
            if self.check_file_existence(file_path, content):
                file_has_issues = True
            
            if file_has_issues:
                self.statistics['files_with_issues'] += 1
            
            return file_has_issues
            
        except Exception as e:
            self.add_issue(
                file_path, 
                'file_read_error', 
                'critical',
                f'Error reading file: {str(e)}',
                'Check file permissions and encoding'
            )
            return True
    
    def run_comprehensive_analysis(self):
        """Run comprehensive analysis on all HTML files."""
        print("🔍 ULTIMATE WEBSITE DIAGNOSTIC SYSTEM")
        print("=" * 50)
        
        # Find all HTML files
        self.html_files = self.find_all_html_files()
        self.statistics['total_files'] = len(self.html_files)
        
        print(f"📁 Found {len(self.html_files)} HTML files to analyze")
        print()
        
        # Analyze each file
        for i, html_file in enumerate(self.html_files, 1):
            print(f"[{i:2d}/{len(self.html_files)}] Analyzing: {html_file}")
            self.analyze_single_file(html_file)
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive diagnostic report."""
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC REPORT")
        print("=" * 50)
        
        # Statistics
        print(f"📈 STATISTICS:")
        print(f"   Total Files Analyzed: {self.statistics['total_files']}")
        print(f"   Files with Issues: {self.statistics['files_with_issues']}")
        print(f"   Critical Issues: {self.statistics['critical_issues']}")
        print(f"   Warning Issues: {self.statistics['warning_issues']}")
        print(f"   Info Issues: {self.statistics['info_issues']}")
        print(f"   Total Issues: {len(self.issues)}")
        
        # Group issues by type
        issues_by_type = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in issues_by_type:
                issues_by_type[issue_type] = []
            issues_by_type[issue_type].append(issue)
        
        print(f"\n🔍 ISSUES BY TYPE:")
        for issue_type, type_issues in issues_by_type.items():
            print(f"   {issue_type}: {len(type_issues)} files affected")
        
        # Critical issues first
        critical_issues = [i for i in self.issues if i['severity'] == 'critical']
        if critical_issues:
            print(f"\n🚨 CRITICAL ISSUES ({len(critical_issues)}):")
            for issue in critical_issues[:10]:  # Show first 10
                print(f"   ❌ {issue['file']}: {issue['description']}")
            if len(critical_issues) > 10:
                print(f"   ... and {len(critical_issues) - 10} more critical issues")
        
        # Summary
        print(f"\n📋 SUMMARY:")
        if self.statistics['critical_issues'] == 0:
            print("   ✅ No critical issues found!")
        else:
            print(f"   ⚠️  {self.statistics['critical_issues']} critical issues need immediate attention")
        
        if self.statistics['files_with_issues'] == 0:
            print("   🎉 Website appears to be fully functional!")
        else:
            print(f"   🔧 {self.statistics['files_with_issues']} files need repairs")
        
        return {
            'statistics': self.statistics,
            'issues': self.issues,
            'issues_by_type': issues_by_type
        }

def main():
    base_directory = "MotzzWebsite-main"
    
    if not os.path.exists(base_directory):
        print(f"❌ Error: Directory {base_directory} not found!")
        return
    
    diagnostic = WebsiteDiagnostic(base_directory)
    report = diagnostic.run_comprehensive_analysis()
    
    # Save detailed report to file
    with open('diagnostic_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: diagnostic_report.json")
    print(f"🚀 Ready for Phase 2: Automated Universal Fix Engine")

if __name__ == "__main__":
    main()

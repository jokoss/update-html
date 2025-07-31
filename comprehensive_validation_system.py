#!/usr/bin/env python3
"""
Comprehensive Website Validation System
Live testing and validation of all website functionality
"""

import os
import json
import time
import subprocess
import threading
from pathlib import Path
import requests
from urllib.parse import urljoin, urlparse
import re

class WebsiteValidator:
    def __init__(self, base_directory, server_port=8002):
        self.base_directory = base_directory
        self.server_port = server_port
        self.server_process = None
        self.base_url = f"http://localhost:{server_port}/MotzzWebsite-main/"
        self.validation_results = []
        self.statistics = {
            'total_pages_tested': 0,
            'pages_passed': 0,
            'pages_failed': 0,
            'navigation_tests_passed': 0,
            'navigation_tests_failed': 0,
            'asset_tests_passed': 0,
            'asset_tests_failed': 0
        }
    
    def start_local_server(self):
        """Start a local HTTP server for testing."""
        try:
            print("🚀 Starting local server...")
            # Use Python's built-in HTTP server
            self.server_process = subprocess.Popen([
                'python', '-m', 'http.server', str(self.server_port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(3)
            
            # Test if server is running
            try:
                response = requests.get(f"http://localhost:{self.server_port}/", timeout=5)
                print(f"✅ Server started successfully on port {self.server_port}")
                return True
            except requests.exceptions.RequestException:
                print(f"❌ Failed to start server on port {self.server_port}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_local_server(self):
        """Stop the local HTTP server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 Server stopped")
    
    def test_page_loads(self, page_url, page_name):
        """Test if a page loads successfully."""
        try:
            response = requests.get(page_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for basic HTML structure
                has_html = '<html' in content.lower()
                has_head = '<head>' in content.lower()
                has_body = '<body>' in content.lower()
                
                # Check for navigation elements
                has_header_div = 'id="header"' in content
                has_footer_div = 'id="footer"' in content
                has_nav_script = 'include-nav.js' in content
                
                # Check for errors
                has_404_error = '404' in content and 'not found' in content.lower()
                has_js_errors = 'error' in content.lower() and 'javascript' in content.lower()
                
                result = {
                    'page': page_name,
                    'url': page_url,
                    'status': 'PASS' if response.status_code == 200 and not has_404_error else 'FAIL',
                    'status_code': response.status_code,
                    'has_html_structure': has_html and has_head and has_body,
                    'has_header_div': has_header_div,
                    'has_footer_div': has_footer_div,
                    'has_navigation_script': has_nav_script,
                    'has_404_error': has_404_error,
                    'content_length': len(content),
                    'issues': []
                }
                
                # Add issues
                if not has_header_div:
                    result['issues'].append('Missing header div')
                if not has_footer_div:
                    result['issues'].append('Missing footer div')
                if not has_nav_script:
                    result['issues'].append('Missing navigation script')
                if has_404_error:
                    result['issues'].append('Page shows 404 error')
                
                return result
                
            else:
                return {
                    'page': page_name,
                    'url': page_url,
                    'status': 'FAIL',
                    'status_code': response.status_code,
                    'issues': [f'HTTP {response.status_code} error']
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'page': page_name,
                'url': page_url,
                'status': 'FAIL',
                'status_code': 0,
                'issues': [f'Request failed: {str(e)}']
            }
    
    def test_asset_loading(self, page_url):
        """Test if page assets load correctly."""
        try:
            response = requests.get(page_url, timeout=10)
            if response.status_code != 200:
                return {'css_assets': [], 'js_assets': [], 'image_assets': [], 'failed_assets': []}
            
            content = response.text
            base_url = page_url.rsplit('/', 1)[0] + '/'
            
            # Find CSS files
            css_files = re.findall(r'href="([^"]*\.css)"', content)
            js_files = re.findall(r'src="([^"]*\.js)"', content)
            img_files = re.findall(r'src="([^"]*\.(jpg|jpeg|png|gif|svg))"', content)
            
            failed_assets = []
            
            # Test a few critical assets
            critical_assets = []
            for css_file in css_files[:3]:  # Test first 3 CSS files
                if not css_file.startswith('http'):
                    asset_url = urljoin(base_url, css_file)
                    critical_assets.append(('CSS', css_file, asset_url))
            
            for js_file in js_files[:3]:  # Test first 3 JS files
                if not js_file.startswith('http'):
                    asset_url = urljoin(base_url, js_file)
                    critical_assets.append(('JS', js_file, asset_url))
            
            for asset_type, asset_path, asset_url in critical_assets:
                try:
                    asset_response = requests.head(asset_url, timeout=5)
                    if asset_response.status_code != 200:
                        failed_assets.append(f'{asset_type}: {asset_path} (HTTP {asset_response.status_code})')
                except:
                    failed_assets.append(f'{asset_type}: {asset_path} (Failed to load)')
            
            return {
                'css_assets': len(css_files),
                'js_assets': len(js_files),
                'image_assets': len(img_files),
                'failed_assets': failed_assets
            }
            
        except Exception as e:
            return {
                'css_assets': 0,
                'js_assets': 0,
                'image_assets': 0,
                'failed_assets': [f'Asset test failed: {str(e)}']
            }
    
    def get_test_pages(self):
        """Get list of critical pages to test."""
        test_pages = [
            ('Homepage', 'index.html'),
            ('About Us', 'about-us.html'),
            ('Analytical Testing', 'analytical-testing.html'),
            ('Forms', 'forms.html'),
            ('License & Accreditations', 'license-accreditations.html'),
            ('Professional Membership', 'professional-membership.html'),
            ('Privacy Policy', 'privacy-policy.html'),
            ('Terms & Conditions', 'terms-conditions.html'),
            
            # Service pages
            ('Agriculture Services', 'services/analytical-testing-agriculture.html'),
            ('Microbiology Services', 'services/analytical-testing-microbiology.html'),
            ('Environmental Services', 'services/analytical-testing-environmental.html'),
            ('Construction Materials', 'services/analytical-testing-construction-materials.html'),
            ('Dietary Supplements', 'services/analytical-testing-dietary-supplements.html'),
            
            # Sampling info pages
            ('Plant Tissue Sampling', 'sampling-info/plant-tissue.html'),
            ('Soil Sampling', 'sampling-info/soil.html'),
            ('Water Sampling', 'sampling-info/water.html'),
            
            # Subdirectory pages
            ('About Us (subdirectory)', 'about-us/index.html'),
            ('Contact Us', 'contact-us/index.html'),
            ('Forms (subdirectory)', 'forms/index.html'),
        ]
        
        return test_pages
    
    def run_comprehensive_validation(self):
        """Run comprehensive validation of the entire website."""
        print("🧪 COMPREHENSIVE WEBSITE VALIDATION SYSTEM")
        print("=" * 60)
        
        # Start server
        if not self.start_local_server():
            print("❌ Cannot start server. Validation aborted.")
            return None
        
        try:
            test_pages = self.get_test_pages()
            print(f"📋 Testing {len(test_pages)} critical pages...")
            print()
            
            for i, (page_name, page_path) in enumerate(test_pages, 1):
                page_url = urljoin(self.base_url, page_path)
                print(f"[{i:2d}/{len(test_pages)}] Testing: {page_name}")
                print(f"    URL: {page_url}")
                
                # Test page loading
                page_result = self.test_page_loads(page_url, page_name)
                
                # Test asset loading
                asset_result = self.test_asset_loading(page_url)
                page_result['assets'] = asset_result
                
                # Update statistics
                self.statistics['total_pages_tested'] += 1
                if page_result['status'] == 'PASS':
                    self.statistics['pages_passed'] += 1
                    if page_result.get('has_header_div') and page_result.get('has_navigation_script'):
                        self.statistics['navigation_tests_passed'] += 1
                    else:
                        self.statistics['navigation_tests_failed'] += 1
                    
                    if not asset_result.get('failed_assets'):
                        self.statistics['asset_tests_passed'] += 1
                    else:
                        self.statistics['asset_tests_failed'] += 1
                else:
                    self.statistics['pages_failed'] += 1
                    self.statistics['navigation_tests_failed'] += 1
                    self.statistics['asset_tests_failed'] += 1
                
                # Print result
                if page_result['status'] == 'PASS':
                    issues = page_result.get('issues', [])
                    if not issues:
                        print(f"    ✅ PASS - Page loads perfectly")
                    else:
                        print(f"    ⚠️  PASS with issues: {', '.join(issues)}")
                else:
                    issues = page_result.get('issues', [])
                    print(f"    ❌ FAIL - {', '.join(issues)}")
                
                # Print asset info
                if asset_result.get('failed_assets'):
                    print(f"    🔗 Asset issues: {len(asset_result['failed_assets'])} failed")
                else:
                    total_assets = asset_result.get('css_assets', 0) + asset_result.get('js_assets', 0)
                    print(f"    🔗 Assets: {total_assets} loaded successfully")
                
                self.validation_results.append(page_result)
                print()
                
                # Small delay between requests
                time.sleep(0.5)
            
            return self.generate_validation_report()
            
        finally:
            self.stop_local_server()
    
    def generate_validation_report(self):
        """Generate comprehensive validation report."""
        print("=" * 60)
        print("📊 VALIDATION REPORT")
        print("=" * 60)
        
        # Overall statistics
        print(f"📈 OVERALL RESULTS:")
        print(f"   Total Pages Tested: {self.statistics['total_pages_tested']}")
        print(f"   Pages Passed: {self.statistics['pages_passed']}")
        print(f"   Pages Failed: {self.statistics['pages_failed']}")
        
        success_rate = (self.statistics['pages_passed'] / self.statistics['total_pages_tested']) * 100
        print(f"   Success Rate: {success_rate:.1f}%")
        
        print(f"\n🧭 NAVIGATION TESTS:")
        print(f"   Navigation Tests Passed: {self.statistics['navigation_tests_passed']}")
        print(f"   Navigation Tests Failed: {self.statistics['navigation_tests_failed']}")
        
        print(f"\n🔗 ASSET TESTS:")
        print(f"   Asset Tests Passed: {self.statistics['asset_tests_passed']}")
        print(f"   Asset Tests Failed: {self.statistics['asset_tests_failed']}")
        
        # Failed pages
        failed_pages = [r for r in self.validation_results if r['status'] == 'FAIL']
        if failed_pages:
            print(f"\n❌ FAILED PAGES ({len(failed_pages)}):")
            for page in failed_pages:
                issues = ', '.join(page.get('issues', []))
                print(f"   • {page['page']}: {issues}")
        
        # Pages with issues
        pages_with_issues = [r for r in self.validation_results if r['status'] == 'PASS' and r.get('issues')]
        if pages_with_issues:
            print(f"\n⚠️  PAGES WITH MINOR ISSUES ({len(pages_with_issues)}):")
            for page in pages_with_issues:
                issues = ', '.join(page.get('issues', []))
                print(f"   • {page['page']}: {issues}")
        
        # Summary
        print(f"\n📋 SUMMARY:")
        if self.statistics['pages_failed'] == 0:
            print("   🎉 ALL PAGES PASSED! Website is fully functional!")
        elif self.statistics['pages_failed'] <= 2:
            print(f"   ✅ Excellent! Only {self.statistics['pages_failed']} pages need attention")
        elif self.statistics['pages_failed'] <= 5:
            print(f"   👍 Good! {self.statistics['pages_failed']} pages need fixes")
        else:
            print(f"   ⚠️  {self.statistics['pages_failed']} pages need attention")
        
        if self.statistics['navigation_tests_passed'] >= self.statistics['total_pages_tested'] * 0.9:
            print("   🧭 Navigation system is working excellently!")
        else:
            print("   🧭 Navigation system needs some improvements")
        
        # Save detailed report
        validation_report = {
            'statistics': self.statistics,
            'results': self.validation_results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('validation_report.json', 'w') as f:
            json.dump(validation_report, f, indent=2)
        
        print(f"\n💾 Detailed validation report saved to: validation_report.json")
        
        return validation_report

def main():
    base_directory = "MotzzWebsite-main"
    
    if not os.path.exists(base_directory):
        print(f"❌ Error: Directory {base_directory} not found!")
        return
    
    validator = WebsiteValidator(base_directory)
    validation_report = validator.run_comprehensive_validation()
    
    if validation_report:
        print(f"\n🏁 VALIDATION COMPLETE!")
        print(f"   Success Rate: {(validation_report['statistics']['pages_passed'] / validation_report['statistics']['total_pages_tested']) * 100:.1f}%")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Final Comprehensive Website Test
Tests all pages and generates a complete report
"""

import requests
import json
import os
from datetime import datetime

def test_url(url, description):
    """Test a single URL and return results"""
    try:
        response = requests.get(url, timeout=10)
        return {
            'url': url,
            'description': description,
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'content_length': len(response.content),
            'error': None
        }
    except Exception as e:
        return {
            'url': url,
            'description': description,
            'status_code': None,
            'success': False,
            'content_length': 0,
            'error': str(e)
        }

def main():
    base_url = "http://localhost:8002"
    
    # Define all pages to test
    test_pages = [
        # Main pages
        ('/', 'Homepage'),
        ('/index.html', 'Index Page'),
        ('/about-us.html', 'About Us'),
        ('/analytical-testing.html', 'Analytical Testing'),
        ('/forms.html', 'Forms'),
        ('/license-accreditations.html', 'License & Accreditations'),
        ('/professional-membership.html', 'Professional Membership'),
        ('/privacy-policy.html', 'Privacy Policy'),
        ('/terms-conditions.html', 'Terms & Conditions'),
        
        # Service pages
        ('/services/analytical-testing-agriculture.html', 'Agriculture Testing'),
        ('/services/analytical-testing-cannabis-hemp.html', 'Cannabis & Hemp Testing'),
        ('/services/analytical-testing-construction-materials.html', 'Construction Materials Testing'),
        ('/services/analytical-testing-dietary-supplements.html', 'Dietary Supplements Testing'),
        ('/services/analytical-testing-environmental.html', 'Environmental Testing'),
        ('/services/analytical-testing-fertilizer.html', 'Fertilizer Testing'),
        ('/services/analytical-testing-microbiology.html', 'Microbiology Testing'),
        ('/services/analytical-testing-neutraceutical-vitamins.html', 'Nutraceutical & Vitamins Testing'),
        ('/services/analytical-testing-research-development.html', 'Research & Development Testing'),
        
        # Sampling info pages
        ('/sampling-info/plant-tissue.html', 'Plant Tissue Sampling'),
        ('/sampling-info/soil.html', 'Soil Sampling'),
        ('/sampling-info/water.html', 'Water Sampling'),
        
        # Include files
        ('/header.html', 'Header Include'),
        ('/footer.html', 'Footer Include'),
        
        # Assets
        ('/assets/css/site.css', 'Site CSS'),
        ('/assets/css/theme.min.css', 'Theme CSS'),
        ('/assets/js/include-nav.js', 'Navigation JS'),
        ('/assets/img/logo.svg', 'Logo'),
    ]
    
    print("🔍 Starting Comprehensive Website Test...")
    print(f"Testing {len(test_pages)} pages/resources...")
    print("=" * 60)
    
    results = []
    success_count = 0
    
    for path, description in test_pages:
        url = base_url + path
        result = test_url(url, description)
        results.append(result)
        
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{status} {description}")
        print(f"    URL: {url}")
        print(f"    Status: {result['status_code']}")
        if result['error']:
            print(f"    Error: {result['error']}")
        print()
        
        if result['success']:
            success_count += 1
    
    # Generate summary
    total_tests = len(test_pages)
    success_rate = (success_count / total_tests) * 100
    
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {success_count}")
    print(f"Failed: {total_tests - success_count}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Save detailed report
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': total_tests,
            'passed': success_count,
            'failed': total_tests - success_count,
            'success_rate': success_rate
        },
        'results': results
    }
    
    with open('final_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: final_test_report.json")
    
    if success_rate == 100:
        print("\n🎉 ALL TESTS PASSED! Website is fully functional!")
    else:
        print(f"\n⚠️  {total_tests - success_count} issues found. Check the report for details.")
    
    return success_rate == 100

if __name__ == "__main__":
    main()

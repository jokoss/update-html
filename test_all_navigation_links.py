#!/usr/bin/env python3
"""
Comprehensive Navigation Link Testing
Tests all navigation links and identifies broken ones
"""

import requests
import json
from datetime import datetime

def test_url(base_url, path, description):
    """Test a single URL and return results"""
    url = base_url + path
    try:
        response = requests.get(url, timeout=10)
        return {
            'path': path,
            'url': url,
            'description': description,
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'content_length': len(response.content),
            'error': None
        }
    except Exception as e:
        return {
            'path': path,
            'url': url,
            'description': description,
            'status_code': None,
            'success': False,
            'content_length': 0,
            'error': str(e)
        }

def main():
    base_url = "http://localhost:8002"
    
    # Navigation links from header.html
    navigation_links = [
        # Main navigation pages
        ('./about-us.html', 'About Us Page'),
        ('./license-accreditations.html', 'Accreditations Page'),
        ('./professional-membership.html', 'Membership Page'),
        ('./analytical-testing.html', 'All Services Page'),
        
        # Service pages
        ('./services/analytical-testing-agriculture.html', 'Agriculture Service'),
        ('./services/analytical-testing-microbiology.html', 'Microbiology Service'),
        ('./services/analytical-testing-environmental.html', 'Environmental Service'),
        ('./services/analytical-testing-construction-materials.html', 'Construction Materials Service'),
        ('./services/analytical-testing-dietary-supplements.html', 'Dietary Supplements Service'),
        ('./services/analytical-testing-research-development.html', 'Research & Development Service'),
        
        # Agriculture sub-services
        ('./services/agriculture/plant-tissue-petiole.html', 'Plant/Tissue/Petiole Service'),
        ('./services/agriculture/soil.html', 'Soil Service'),
        ('./services/agriculture/water.html', 'Water Service'),
        ('./services/agriculture/compost.html', 'Compost Service'),
        ('./services/agriculture/fertilizer.html', 'Fertilizer Service'),
        
        # Sampling info pages
        ('./sampling-info/plant-tissue.html', 'Plant/Tissue Sampling Info'),
        ('./sampling-info/water.html', 'Water Sampling Info'),
        ('./sampling-info/soil.html', 'Soil Sampling Info'),
        
        # Form downloads
        ('./forms/download/Client_Information.pdf', 'Client Information PDF'),
        ('./forms/download/Chain_of_Custody.pdf', 'Chain of Custody PDF'),
    ]
    
    print("🔍 Testing All Navigation Links...")
    print(f"Testing {len(navigation_links)} navigation links...")
    print("=" * 70)
    
    results = []
    working_links = []
    broken_links = []
    
    for path, description in navigation_links:
        # Remove the ./ prefix for testing
        clean_path = path[2:] if path.startswith('./') else path
        result = test_url(base_url, '/' + clean_path, description)
        results.append(result)
        
        status = "✅ WORKING" if result['success'] else "❌ BROKEN"
        print(f"{status} {description}")
        print(f"    Path: {path}")
        print(f"    URL: {result['url']}")
        print(f"    Status: {result['status_code']}")
        if result['error']:
            print(f"    Error: {result['error']}")
        print()
        
        if result['success']:
            working_links.append(result)
        else:
            broken_links.append(result)
    
    # Generate summary
    total_links = len(navigation_links)
    working_count = len(working_links)
    broken_count = len(broken_links)
    success_rate = (working_count / total_links) * 100
    
    print("=" * 70)
    print("📊 NAVIGATION LINK TEST SUMMARY")
    print("=" * 70)
    print(f"Total Links Tested: {total_links}")
    print(f"Working Links: {working_count}")
    print(f"Broken Links: {broken_count}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if broken_links:
        print("\n❌ BROKEN LINKS:")
        for link in broken_links:
            print(f"  - {link['description']}: {link['path']}")
    
    if working_links:
        print(f"\n✅ WORKING LINKS: {working_count}")
    
    # Save detailed report
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_links': total_links,
            'working': working_count,
            'broken': broken_count,
            'success_rate': success_rate
        },
        'working_links': working_links,
        'broken_links': broken_links,
        'all_results': results
    }
    
    with open('navigation_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: navigation_test_report.json")
    
    return broken_count == 0

if __name__ == "__main__":
    main()

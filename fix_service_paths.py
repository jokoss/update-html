import os
import re

def main():
    # Fix service paths in subpages
    fix_service_paths()

def fix_service_paths():
    # Update all subpages to use the correct service paths
    subpage_dirs = [
        'MotzzWebsite-main/about-us',
        'MotzzWebsite-main/contact-us',
        'MotzzWebsite-main/laboratorytesting',
        'MotzzWebsite-main/sampling',
        'MotzzWebsite-main/forms'
    ]
    
    for subpage_dir in subpage_dirs:
        if os.path.exists(subpage_dir):
            for file in os.listdir(subpage_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(subpage_dir, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace service paths with relative paths
                    content = content.replace('href="/services/analytical-testing-agriculture.html"', 'href="../services/analytical-testing-agriculture.html"')
                    content = content.replace('href="/services/analytical-testing-environmental.html"', 'href="../services/analytical-testing-environmental.html"')
                    content = content.replace('href="/services/analytical-testing-construction-materials.html"', 'href="../services/analytical-testing-construction-materials.html"')
                    content = content.replace('href="/services/analytical-testing-microbiology.html"', 'href="../services/analytical-testing-microbiology.html"')
                    content = content.replace('href="/services/analytical-testing-dietary-supplements.html"', 'href="../services/analytical-testing-dietary-supplements.html"')
                    content = content.replace('href="/services/analytical-testing-neutraceutical-vitamins.html"', 'href="../services/analytical-testing-neutraceutical-vitamins.html"')
                    content = content.replace('href="/services/analytical-testing-fertilizer.html"', 'href="../services/analytical-testing-fertilizer.html"')
                    content = content.replace('href="/services/analytical-testing-research-development.html"', 'href="../services/analytical-testing-research-development.html"')
                    content = content.replace('href="/services/analytical-testing-cannabis-hemp.html"', 'href="../services/analytical-testing-cannabis-hemp.html"')
                    
                    # Replace agriculture service paths
                    content = content.replace('href="/services/agriculture/plant-tissue-petiole.html"', 'href="../services/agriculture/plant-tissue-petiole.html"')
                    content = content.replace('href="/services/agriculture/soil.html"', 'href="../services/agriculture/soil.html"')
                    content = content.replace('href="/services/agriculture/compost.html"', 'href="../services/agriculture/compost.html"')
                    content = content.replace('href="/services/agriculture/fertilizer.html"', 'href="../services/agriculture/fertilizer.html"')
                    content = content.replace('href="/services/agriculture/water.html"', 'href="../services/agriculture/water.html"')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Updated service paths in {file_path}")

if __name__ == "__main__":
    main()

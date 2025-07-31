import os
import webbrowser
import time

def main():
    # Test the website
    test_website()

def test_website():
    # Open the main page
    main_page = os.path.abspath('MotzzWebsite-main/index.html')
    print(f"Opening main page: {main_page}")
    webbrowser.open(f"file://{main_page}")
    
    # Wait for the user to view the page
    time.sleep(2)
    
    # Open a subpage
    subpage = os.path.abspath('MotzzWebsite-main/about-us/index.html')
    print(f"Opening subpage: {subpage}")
    webbrowser.open(f"file://{subpage}")
    
    # Wait for the user to view the page
    time.sleep(2)
    
    # Open another subpage
    subpage = os.path.abspath('MotzzWebsite-main/contact-us/index.html')
    print(f"Opening subpage: {subpage}")
    webbrowser.open(f"file://{subpage}")
    
    # Wait for the user to view the page
    time.sleep(2)
    
    # Open a service page
    service_page = os.path.abspath('MotzzWebsite-main/services/analytical-testing-agriculture.html')
    print(f"Opening service page: {service_page}")
    webbrowser.open(f"file://{service_page}")
    
    print("Website testing complete!")

if __name__ == "__main__":
    main()

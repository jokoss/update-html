import http.server
import socketserver
import os
import webbrowser
import threading
import time

def open_browser():
    # Wait a moment for the server to start
    time.sleep(1)
    # Open the browser to the main page
    webbrowser.open('http://localhost:8000/MotzzWebsite-main/index.html')
    # Wait a moment before opening subpages
    time.sleep(2)
    # Open a subpage
    webbrowser.open('http://localhost:8000/MotzzWebsite-main/about-us/index.html')
    # Wait a moment before opening another subpage
    time.sleep(2)
    # Open another subpage
    webbrowser.open('http://localhost:8000/MotzzWebsite-main/contact-us/index.html')
    # Wait a moment before opening a service page
    time.sleep(2)
    # Open a service page
    webbrowser.open('http://localhost:8000/MotzzWebsite-main/services/analytical-testing-agriculture.html')

def run_server():
    # Set the port
    PORT = 8000
    
    # Change to the parent directory to serve from there
    os.chdir('..')
    
    # Create the server
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    
    print(f"Serving at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    # Start the browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_server()

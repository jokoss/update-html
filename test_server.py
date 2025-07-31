#!/usr/bin/env python3
"""
Simple HTTP server to test the Motzz Laboratory website locally.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def main():
    # Change to the MotzzWebsite-main directory
    os.chdir('MotzzWebsite-main')
    
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    print(f"Starting server at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at http://localhost:{PORT}")
            print(f"Open http://localhost:{PORT} in your browser to test the website")
            
            # Automatically open browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use. Try a different port or stop the existing server.")
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()

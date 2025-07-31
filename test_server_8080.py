#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = 8080
os.chdir("MotzzWebsite-main")

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()
except OSError as e:
    print(f"Port {PORT} is in use, trying port 8081...")
    PORT = 8081
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Server running at http://localhost:{PORT}/")
            print("Press Ctrl+C to stop")
            httpd.serve_forever()
    except OSError:
        print("Both ports 8080 and 8081 are in use. Please stop other servers first.")

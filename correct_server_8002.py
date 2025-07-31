#!/usr/bin/env python3
import http.server
import socketserver
import os

# Change to the MotzzWebsite-main directory
os.chdir("MotzzWebsite-main")

PORT = 8002
Handler = http.server.SimpleHTTPRequestHandler

print(f"Starting server from directory: {os.getcwd()}")
print(f"Server will be available at: http://localhost:{PORT}/")
print(f"Environmental page will be at: http://localhost:{PORT}/services/analytical-testing-environmental.html")
print("Press Ctrl+C to stop")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
except OSError as e:
    print(f"Error starting server: {e}")
    print("Port may already be in use.")

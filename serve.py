import http.server
import socketserver

PORT = 8002
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving MotzzWebsite-main at http://localhost:{PORT}")
    httpd.serve_forever()

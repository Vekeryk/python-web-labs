from http.server import HTTPServer, CGIHTTPRequestHandler

server_address = ('127.0.0.1', 8080)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
print('=== Start local webserver ===')
httpd.serve_forever()

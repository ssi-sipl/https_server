from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs

class UARTHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode('utf-8'))
        
        # Process the received data
        uart_data = data.get('uart_data', [''])[0]
        print(f"Received UART data: {uart_data}")
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'status': 'success', 'message': 'Data received'})
        self.wfile.write(response.encode('utf-8'))

# Set up the HTTP server
server_address = ('', 8080)  # Use port 8080 for HTTP
httpd = HTTPServer(server_address, UARTHandler)

print('HTTP Server running on port 8080...')
httpd.serve_forever()
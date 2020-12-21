import http.server
import socketserver
from http import HTTPStatus
from urllib.request import urlopen


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        with urlopen("http://backend.service.consul") as response:
            self.send_response(HTTPStatus.OK)
            self.end_headers()

            self.wfile.write(
                'The backend says: "{}"'.format(response.read()).encode("utf-8")
            )


httpd = socketserver.TCPServer(('', 80), Handler)
httpd.serve_forever()

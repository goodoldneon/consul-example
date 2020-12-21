import http.server
import socketserver
from http import HTTPStatus
from urllib.request import urlopen


BACKEND_SERVICE_HOST = "localhost"
BACKEND_SERVICE_PORT = 5000


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        with urlopen(f"http://{BACKEND_SERVICE_HOST}:{BACKEND_SERVICE_PORT}") as res:
            self.wfile.write(
                'The backend says: "{}"'.format(res.read()).encode("utf-8")
            )


httpd = socketserver.TCPServer(('', 80), Handler)
httpd.serve_forever()

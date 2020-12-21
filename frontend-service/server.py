import http.server
import socketserver
from http import HTTPStatus
from urllib.request import urlopen


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = ""
        status = HTTPStatus.OK

        if self.path == "/":
            self.wfile.write(b"Try /hostname or /proxy")
        elif self.path == "/hostname":
            url = "http://backend-service.service.consul"
        elif self.path == "/proxy":
            url = "http://localhost:5000"
        else:
            status = HTTPStatus.NOT_FOUND

        self.send_response(status)
        self.end_headers()

        if url != "":
            with urlopen(url) as response:
                self.wfile.write(
                    'The backend says: "{}"'.format(response.read()).encode("utf-8")
                )


httpd = socketserver.TCPServer(('', 80), Handler)
httpd.serve_forever()

"""Module for the server"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import mimetypes
import sys

PORT = 8000


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Basic server class"""

    def do_GET(self):
        # pylint: disable=C0103
        """GET method"""
        try:
            if self.path == "/":
                self.path = "../index.html"
            else:
                self.path = "../" + self.path
            f = open(self.path, "rb")

            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(self.path))
            self.end_headers()
            self.wfile.write(f.read())

            f.close()
        except IOError:
            print(sys.exc_info())
            self.send_error(404, "File Not Found: % s" % self.path)

    def do_POST(self):
        # pylint: disable=C0103
        """POST method"""
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b"This is POST request.")
        response.write(b"Received: ")
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(("localhost", PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()

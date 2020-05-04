from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

PORT = 8000


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            f = open("../index.html", "rb")

            self.send_response(200)
            self.send_header("Content - type", "text / html")
            self.end_headers()
            self.wfile.write(f.read())

            f.close()
            return
        except IOError:
            self.send_error(404, "File Not Found: % s" % self.path)

    def do_POST(self):
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

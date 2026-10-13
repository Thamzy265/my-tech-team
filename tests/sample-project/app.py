"""Tiny notes service used as a sample project."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

NOTES = []


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/notes":
            self._send(200, NOTES)
        else:
            self._send(404, {"error": "not found"})


def make_server(port=8765):
    return HTTPServer(("127.0.0.1", port), Handler)


if __name__ == "__main__":
    make_server().serve_forever()

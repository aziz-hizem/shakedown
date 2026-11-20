from http.server import BaseHTTPRequestHandler, HTTPServer # Python's built-in web server


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # Called for every GET request
        if self.path == "/health":
            body = b"ok"     # what kubernetes will check later
        else:
            body = b"Hello from the shakedown sample app"

        self.send_response(200)    # HTTP 200 = success
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)


# 0.0.0.0 = listen on every network interface
HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

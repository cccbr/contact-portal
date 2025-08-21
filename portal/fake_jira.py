# pylint: skip-file
""" We Are Bell Ringing: Fake Implimentation of Jira
A Fake HTTP Server to Accept Jira Payloads
:author: Martyn Bristow

Test:
>> curl localhost:8001
>> curl --data '' localhost:8001
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps


class FakeJira(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "OK")
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(dumps({"issues": []}), "UTF-8"))

    def do_POST(self):
        self.send_response(201, "OK")
        content_length = int(self.headers["Content-Length"])
        post_data_bytes = self.rfile.read(content_length)
        post_data_str = post_data_bytes.decode("UTF-8")
        print(post_data_str)
        self.end_headers()
        self.wfile.write(b"")


def run(server_class=HTTPServer, handler_class=FakeJira):
    server_address = ("localhost", 8001)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()

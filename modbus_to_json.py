#!/usr/bin/env python3

import argparse

from os import path
from http.server import BaseHTTPRequestHandler, HTTPServer

from t300 import T300

modbus_device:str = None

class JsonServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        dev = T300(device_name)
        self.wfile.write(dev.as_json())


def run_server():
    parser = argparse.ArgumentParser("modbus_to_json")
    parser.add_argument("dev", help="Device path to read data from")
    parser.add_argument("--address", default="127.0.0.1", help="IP Address to listen on")
    parser.add_argument("--port", default=6001, help="Port to listen on", type=int)
    args = parser.parse_args()

    if not path.exists(args.dev):
        print(f"Device '{args.dev}' does not exist.")
        return

    global device_name
    device_name = args.dev

    webServer = HTTPServer((args.address, args.port), JsonServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()

if __name__ == "__main__":
    run_server()
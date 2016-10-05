"""
    @AUTHOR: Gurkengewuerz
    @REVIEW: 05.10.2016
    @DESCRIPTION: An API for IPINFO with Cache Function
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from Config import *
from Managers import *
import json


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(str(self.path))
        if self.path.startswith("/api"):
            message = {"error": "No valid IP Adress"}
            params = parse_qs(urlparse(self.path).query)
            if "ip" in params:
                ip = str(params["ip"][0])
                print("New Request for IP: " + ip + " from " + str(self.client_address))
                if IPValidator().is_valid_ipv4_address(ip) or IPValidator().is_valid_ipv6_address(ip) is True:
                    rm = RequestManager(ip)
                    message = rm.makeRequest()
                    message["status"] = rm.getStatus()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(message), "utf8"))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "API available at /api/?ip=<insert IP here>"
            self.wfile.write(bytes(message, "utf8"))
        return


def run():
    DB.sql_do(
        "CREATE TABLE IF NOT EXISTS `data_storage` (" +
        "`id` INTEGER PRIMARY KEY AUTOINCREMENT," +
        "`date`	INTEGER NOT NULL," +
        "`ip`	TEXT NOT NULL," +
        "`hostname`	TEXT," +
        "`org`	TEXT," +
        "`country`	TEXT," +
        "`region`	TEXT," +
        "`city`	TEXT," +
        "`postal`	TEXT," +
        "`loc`	TEXT" +
        ");"
    )

    print('starting server...')
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('server running...')
    httpd.serve_forever()


run()

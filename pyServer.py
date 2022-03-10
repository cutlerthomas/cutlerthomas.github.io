from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from opDB import opDB
from logging.config import listen
import json

class myRequestHandler(BaseHTTPRequestHandler):

    def handleListFavorites(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        #write to the "wfile" response body
        db = opDB('opChars_db.db')
        allRecords = db.readAllChars()
        self.wfile.write(bytes(json.dumps(allRecords), "utf-8"))

    def handleCreateFavorite(self):
        length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(length)).decode("utf-8")
        print("the raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("the parsed request body:", parsed_body)
        op_name = parsed_body["name"][0]
        op_age = parsed_body["age"][0]
        op_height = parsed_body["height"][0]
        op_weight = parsed_body["weight"][0]
        op_affiliation = parsed_body["affiliation"][0]
        op_df = parsed_body["df"][0]
        db = opDB('opChars_db.db')
        allRecords = db.readAllChars()
        if op_name in allRecords:
            self.send_response(409)
        else:
            db.addChar(op_name, op_age, op_height, op_weight, op_df, op_affiliation)
            self.send_response(201)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def handleRetrieveChar(self, char_id):
        db = opDB('opChars_db.db')
        oneChar = db.readOneChar(char_id)
        if oneChar:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(oneChar), "utf-8"))
        else:
            self.handleNotFound()

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Resource not found", "utf-8"))

    def handleDeleteChar(self, char_id):
        db = opDB('opChars_db.db')
        oneChar = db.readOneChar(char_id)
        if oneChar:
            db.deleteChar(char_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.handleNotFound()

    def handleUpdateChar(self, char_id):
        length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(length)).decode("utf-8")
        print("the raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("the parsed request body:", parsed_body)
        name = parsed_body["name"][0]
        age = parsed_body["age"][0]
        height = parsed_body["height"][0]
        weight = parsed_body["weight"][0]
        affiliation = parsed_body["affiliation"][0]
        df = parsed_body["df"][0]
        db = opDB('opChars_db.db')
        oneChar = db.readOneChar(char_id)
        if oneChar:
            db.updateChar(char_id, name, age, height, weight, affiliation, df)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.handleNotFound()

    # handle get requests
    def do_GET(self):
        print("the request path is:", self.path)
        path_parts = self.path.split("/")
        if len(path_parts) > 2:
            collection_name = path_parts[1]
            char_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            char_id = None
        print (collection_name, char_id)
        if collection_name == "chars":
            if char_id == None:
                self.handleListFavorites()
            else:
                self.handleRetrieveChar(char_id)
        else:
            self.handleNotFound()

    # handle post requests
    def do_POST(self):
        print("the request path is", self.path)
        if self.path == "/chars":
            self.handleCreateFavorite()
        else:
            self.handleNotFound()

    def do_PUT(self):
        print("the request path is:", self.path)
        path_parts = self.path.split("/")
        if len(path_parts) > 2:
            collection_name = path_parts[1]
            char_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            char_id = None
        print(collection_name, char_id)
        if collection_name == "chars":
            if char_id == None:
                print("no id given")
            else:
                self.handleUpdateChar(char_id)
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        print("the request path is:", self.path)
        path_parts = self.path.split("/")
        if len(path_parts) > 2:
            collection_name = path_parts[1]
            char_id = path_parts[2]
        else:
            collection_name = path_parts[1]
            char_id = None
        print (collection_name, char_id)
        if collection_name == "chars":
            if char_id == None:
                print("No id given")
            else:
                self.handleDeleteChar(char_id)
        else:
            self.handleNotFound()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, myRequestHandler)
    print("Server running")
    server.serve_forever()

if __name__ == "__main__":
    run()
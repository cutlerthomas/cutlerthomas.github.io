import email
from functools import WRAPPER_ASSIGNMENTS
from http import server
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import ssl
from urllib.parse import parse_qs
from opDB import opDB, userDB
from logging.config import listen
import json
from passlib.hash import bcrypt
from sessionStore import SessionStore

SESSION_STORE = SessionStore()

class myRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        super().end_headers()

    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            morsel["samesite"] = "None"
            morsel["secure"] = True
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session_data(self):
        self.loadCookie()
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            self.sessionData = SESSION_STORE.loadSessionData(sessionId)
            if self.sessionData == None:
                sessionId = SESSION_STORE.createSession()
                self.sessionData = SESSION_STORE.loadSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
        else:
            sessionId = SESSION_STORE.createSession()
            self.sessionData = SESSION_STORE.loadSessionData(sessionId)
            self.cookie["sessionId"] = sessionId
        print("MY SESSION DATA:", self.sessionData)

    def handleListFavorites(self):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        #write to the "wfile" response body
        db = opDB()
        allRecords = db.readAllChars()
        self.wfile.write(bytes(json.dumps(allRecords), "utf-8"))

    def handleCreateFavorite(self):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
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
        db = opDB()
        allRecords = db.readAllChars()
        if op_name in allRecords:
            self.send_response(409)
        else:
            db.addChar(op_name, op_age, op_height, op_weight, op_df, op_affiliation)
            self.send_response(201)
            self.end_headers()

    def handleRetrieveChar(self, char_id):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
        db = opDB()
        oneChar = db.readOneChar(char_id)
        if oneChar:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
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
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
        db = opDB()
        oneChar = db.readOneChar(char_id)
        if oneChar:
            db.deleteChar(char_id)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        else:
            self.handleNotFound()

    def handleUpdateChar(self, char_id):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
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
        db = opDB()
        oneChar = db.readOneChar(char_id)
        if oneChar:
            db.updateChar(char_id, name, age, height, weight, affiliation, df)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        else:
            self.handleNotFound()
 
    def handleCreateUser(self):
        length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(length)).decode("utf-8")
        print("the raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("the parsed request body:", parsed_body)
        firstname = parsed_body["firstname"][0]
        lastname = parsed_body["lastname"][0]
        email = parsed_body["email"][0]
        password = parsed_body["encrypted_password"][0]
        db = userDB()
        allRecords = db.readAllUsers()
        encrypted_password = bcrypt.hash(password)
        if db.findUserEmail(email) != None:
            self.send_response(409)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Email already registered", "utf-8"))
        else:
            db.addUser(firstname, lastname, email, encrypted_password)
            self.send_response(201)
            self.end_headers()

    def handleCreateSession(self):
        length = self.headers["Content-Length"]
        request_body = self.rfile.read(int(length)).decode("utf-8")
        print("the raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("the parsed request body:", parsed_body)
        email = parsed_body["email"][0]
        password = parsed_body["encrypted_password"][0]
        db = userDB()
        user = db.findUserEmail(email)
        if user != None:
            if bcrypt.verify(password, user["encrypted_password"]):
                self.send_response(201)
                self.end_headers()
                self.sessionData["userId"] = user["id"]
            else:
                self.send_response(401)
                self.end_headers()
        else:
            self.send_response(401)
            self.end_headers()

    def handleListUsers(self):
        if "userId" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        #write to the "wfile" response body
        db = userDB()
        allRecords = db.readAllUsers()
        self.wfile.write(bytes(json.dumps(allRecords), "utf-8"))

    # handle get requests
    def do_GET(self):
        self.load_session_data()
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
        elif collection_name == "users":
            if char_id == None:
                self.handleListUsers()
        else:
            self.handleNotFound()

    # handle post requests
    def do_POST(self):
        self.load_session_data()
        print("the request path is", self.path)
        if self.path == "/chars":
            self.handleCreateFavorite()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleCreateSession()
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.load_session_data()
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
        self.load_session_data()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        self.load_session_data()
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
    server = ThreadedHTTPServer(listen, myRequestHandler)
    print("Server running")
    server.serve_forever()

if __name__ == "__main__":
    run()



# code for later
# 
import base64, os


class SessionStore:

    def __init__(self):
        self.sessions = {}

    def createSession(self):
        newSessionId = self.generateSessionId()
        self.sessions[newSessionId] = {}
        return newSessionId

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def loadSessionData(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
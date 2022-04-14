
import sqlite3
from time import CLOCK_THREAD_CPUTIME_ID

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

con = sqlite3.connect(":memory:")
con.row_factory = dict_factory
cur = con.cursor()
cur.execute("select 1 as a")
print(cur.fetchone()["a"])

con.close()



class opDB:


    def __init__(self):
        self.connection = sqlite3.connect("opChars_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def addChar(self, name, age, height, weight, df, affiliation): 
        #INPUTS: all char fields (no id)
        #OUTPUTS: none
        data = [name, age, height, weight, affiliation, df]
        self.cursor.execute("INSERT INTO opChars (name, age, height, weight, affiliation, df) VALUES (?, ?, ?, ?, ?, ?)", data)
        self.connection.commit()

    def readAllChars(self):
        #INPUTS: none
        #OUTPUTS: list of all chars
        self.cursor.execute("SELECT * FROM opChars")
        return self.cursor.fetchall()

    def readOneChar(self, char_id): 
        #INPUTS: id num
        #OUTPUTS: a single char
        data = [char_id]
        self.cursor.execute("SELECT * FROM opChars WHERE id = ?", data)
        return self.cursor.fetchone()

    def updateChar(self, char_id, name, age, height, weight, affiliation, df): 
        #INPUTS: all char fields (yes id)
        #OUTPUTS: none
        data = [name, age, height, weight, affiliation, df, char_id]
        self.cursor.execute("UPDATE opChars SET name = ?, age = ?, height = ?, weight = ?, affiliation = ?, df = ? WHERE id = ?", data)
        self.connection.commit()

    def deleteChar(self, char_id): 
        #INPUTS: id num
        #OUTPUTS: none
        data = [char_id]
        self.cursor.execute("DELETE FROM opChars WHERE id = ?", data)
        self.connection.commit()

class userDB:

    def __init__(self):
        self.connection = sqlite3.connect("opUsers_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def addUser(self, fisrtname, lastname, email, encrypted_password): 
        data = [fisrtname, lastname, email, encrypted_password]
        self.cursor.execute("INSERT INTO opUsers (firstname, lastname, email, encrypted_password) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def readAllUsers(self):
        self.cursor.execute("SELECT * FROM opUsers")
        return self.cursor.fetchall()

    def findUserEmail(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM opUsers WHERE email = ?", data)
        return self.cursor.fetchone()
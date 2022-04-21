import psycopg2
import psycopg2.extras
import os
import urllib.parse
#import sqlite3
from time import CLOCK_THREAD_CPUTIME_ID

#def dict_factory(cursor, row):
#   d = {}
#    for idx, col in enumerate(cursor.description):
#        d[col[0]] = row[idx]
#    return d






class opDB:


    def __init__(self):
        #self.connection = sqlite3.connect("opChars_db.db")
        #self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createCharsTable(self):
        #create new char table in database
        self.cursor.execute("CREATE TABLE IF NOT EXISTS opChars (id SERIAL PRIMARY KEY, name TEXT, age INT, height TEXT, weight TEXT, affiliation TEXT, df TEXT)")
        self.connection.commit()

    def addChar(self, name, age, height, weight, df, affiliation): 
        #INPUTS: all char fields (no id)
        #OUTPUTS: none
        data = [name, age, height, weight, affiliation, df]
        self.cursor.execute("INSERT INTO opChars (name, age, height, weight, affiliation, df) VALUES (%s, %s, %s, %s, %s, %s)", data)
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
        self.cursor.execute("SELECT * FROM opChars WHERE id = %s", data)
        return self.cursor.fetchone()

    def updateChar(self, char_id, name, age, height, weight, affiliation, df): 
        #INPUTS: all char fields (yes id)
        #OUTPUTS: none
        data = [name, age, height, weight, affiliation, df, char_id]
        self.cursor.execute("UPDATE opChars SET name = %s, age = %s, height = %s, weight = %s, affiliation = %s, df = %s WHERE id = %s", data)
        self.connection.commit()

    def deleteChar(self, char_id): 
        #INPUTS: id num
        #OUTPUTS: none
        data = [char_id]
        self.cursor.execute("DELETE FROM opChars WHERE id = %s", data)
        self.connection.commit()

class userDB:

    def __init__(self):
        #self.connection = sqlite3.connect("opUsers_db.db")
        #self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def addUser(self, fisrtname, lastname, email, encrypted_password): 
        data = [fisrtname, lastname, email, encrypted_password]
        self.cursor.execute("INSERT INTO opUsers (firstname, lastname, email, encrypted_password) VALUES (%s, %s, %s, %s)", data)
        self.connection.commit()

    def readAllUsers(self):
        self.cursor.execute("SELECT * FROM opUsers")
        return self.cursor.fetchall()

    def findUserEmail(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM opUsers WHERE email = %s", data)
        return self.cursor.fetchone()

    def createUsersTable(self):
        #create new char table in database
        self.cursor.execute("CREATE TABLE IF NOT EXISTS opUsers (id SERIAL PRIMARY KEY, firstname TEXT, lastname TEXT, email TEXT, encrypted_password TEXT)")
        self.connection.commit()
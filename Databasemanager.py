import sqlite3
import os.path
import bcrypt

# filename to form database
file = "Sqlite3.db"


def connect_to_database():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    return c, conn


def create_table():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("""Create TABLE Accounts (
                Username TEXT,
                Password TEXT, 
                Passcode INTEGER,
                Balance REAL
        )""")
    conn.commit()
    conn.close()

def check_if_user_exists(username):
    c, conn = connect_to_database()
    c.execute("SELECT * FROM Accounts WHERE Username=?", (username,))
    if c.fetchall():
        return True #returns True if user exists

if not os.path.isfile(file):
    try:
        conn = sqlite3.connect(file)
        create_table()
        print("Database Sqlite3.db formed.")
    except:
        print("error with creating the database.")


def register(message_data):
    c, conn = connect_to_database()
    username, password = message_data.split(":")[0], message_data.split(":")[1]
    if not check_if_user_exists(username):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO Accounts VALUES(?, ?, ?, ?)", (username, hashed_password, 0, 0))
        conn.commit()
        conn.close()
        return "registration successful"
    return "registration failed"


def login(message_data):
    c,conn = connect_to_database()
    username, password = message_data.split(":")[0], message_data.split(":")[1]
    c.execute("SELECT Password FROM Accounts WHERE Username=?", (username,))
    try:
        hashed = c.fetchone()[0]
        if (bcrypt.checkpw(password.encode(), hashed)):
            return True
        return False
    except TypeError:
        return False




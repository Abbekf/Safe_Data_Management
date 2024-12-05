import sqlite3
from getpass import getpass
import bcrypt

# Create a table to stoe users with hased passwords
def create_user_table():
    """Create a table to store users with hashed passwords"""
    connection = sqlite3.connect("Secure_users.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE, 
    password_hash TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()


# SECURE: Hash the password before storing it
def register_user():
    """Registers a new user with hashed password"""
    while True:
        isALetter = False
        isANumber = False
        username = input("Enter username: ")
        for x in username:
            if x.isalpha():
                isALetter = True
            elif x.isdigit():
                isANumber = True
        if isALetter == True and isANumber == True and len(username) > 2:
            break


    while True:
        password = getpass("Enter your password: ").strip()
        isANumber = False
        isupper = False
        islower = False
        for x in password:
            if x.isupper():
                isupper = True
            elif x.islower():
                islower = True
            elif x.isdigit():
                isANumber = True
        if islower == True and isupper == True and isANumber == True and len(password) > 7:
            break

    # Hasha lösenordet
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    connection = sqlite3.connect("secure_users.db")
    cursor = connection.cursor()

    try:
        query = "INSERT INTO users(username,password_hash)VALUES(?,?)"
        cursor.execute(query, (username, hashed_password))
        connection.commit()
        print("User registered succesfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    finally:
        connection.close()

    
# SECURE: Verify user credentials with hashed password
def login_user():
    """Verify user credentials and login."""
    
    username = input("Enter your username: ").strip()
    password = getpass("Enter your password: ").strip()

    connection = sqlite3.connect("secure_users.db")
    cursor = connection.cursor()

    # Säkra SQL-frågor med paramatriserade frågor
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if result and bcrypt.checkpw(password.encode("utf-8"), result[0]):
        print("Login succesful!")
    else:
        print("Login failed!")
    connection.close()
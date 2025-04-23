import sqlite3

# Connect to the SQLite database (make sure the path is correct)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Query all users
c.execute("SELECT * FROM users")
print(c.fetchall())

conn.close()


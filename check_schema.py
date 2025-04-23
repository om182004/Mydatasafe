import sqlite3

# Connect to the SQLite database (make sure the path is correct)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Show the current schema of the users table
c.execute("PRAGMA table_info(users);")
columns = c.fetchall()
for column in columns:
    print(column)

conn.close()


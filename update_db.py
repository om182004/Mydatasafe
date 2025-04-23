import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Add username column if it's missing
c.execute("ALTER TABLE users ADD COLUMN username TEXT")
conn.commit()
conn.close()

print("Database schema updated!")




import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Drop old table if needed (optional)
# c.execute("DROP TABLE IF EXISTS users")

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()
print("✅ users.db initialized successfully.")

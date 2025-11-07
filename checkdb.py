import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

print("Tables:")
for t in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(t)

print("\nUsers:")
for row in c.execute("SELECT * FROM users;"):
    print(row)

conn.close()


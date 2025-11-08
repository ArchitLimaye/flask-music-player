import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create playlists table
c.execute('''
CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    name TEXT NOT NULL
)
''')

# Create playlist_songs table
c.execute('''
CREATE TABLE IF NOT EXISTS playlist_songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES playlists (id)
)
''')

conn.commit()
conn.close()
print("✅ Playlist tables created successfully.")

import sqlite3

# Connect (or create new)
conn = sqlite3.connect('musicplayer.db')
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    password TEXT NOT NULL,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# ---------------- SONGS TABLE ----------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT,
    genre TEXT,
    duration TEXT,
    file_path TEXT NOT NULL,
    image_path TEXT,
    release_year INTEGER,
    uploaded_by INTEGER,
    FOREIGN KEY (uploaded_by) REFERENCES users (id)
);
''')

# ---------------- SAMPLE SONGS ----------------
songs_data = [
    ("Blinding Lights", "The Weeknd", "After Hours", "Pop", "3:22", "songs/blindingLights.mp3", "images/blindingLights.png", 2020, None),
    ("Specialz", "King Gnu", "Specialz", "J-Rock", "4:01", "songs/specialz.mp3", "images/specialz.jpg", 2023, None),
    ("Superpower", "Kiss of Life", "Superpower", "K-Pop", "3:41", "songs/superpower.mp3", "images/superpower.webp", 2024, None),
    ("Iris Out", "Kenshi Yonezu", "STRAY SHEEP", "J-Pop", "4:16", "songs/irisOut.mp3", "images/irisOut.webp", 2020, None),
    ("Let The World Burn", "Chris Grey", "Single", "Rock", "3:45", "songs/lettheworldburn.mp3", "images/lettheworldburn.jpg", 2022, None),
    ("Starboy", "The Weeknd", "Starboy", "Pop", "3:50", "songs/starboy.mp3", "images/starboy.jpg", 2016, None)
]

cursor.executemany('''
INSERT INTO songs (title, artist, album, genre, duration, file_path, image_path, release_year, uploaded_by)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', songs_data)

# Commit changes
conn.commit()
conn.close()

print("✅ Database created successfully: musicplayer.db")
print("📦 Tables: users, songs")

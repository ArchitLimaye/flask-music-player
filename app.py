from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random  # ✅ Added for shuffling recommendations

app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Helper Functions --- #
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


SONGS = [
    {"id": 1, "title": "Iris Out", "artist": "Kenshi Yonezu", "file": "irisOut.mp3", "image": "irisOut.webp"},
    {"id": 2, "title": "Blinding Lights", "artist": "The Weeknd", "file": "blindingLights.mp3", "image": "blindingLights.png"},
    {"id": 3, "title": "Let the world burn", "artist": "Chris Grey", "file": "lettheworldburn.mp3", "image": "lettheworldburn.jpg"},
    {"id": 4, "title": "Saphire", "artist": "Ed Sheeran", "file": "saphire.mp3", "image": "saphire.png"},
    {"id": 5, "title": "Specialz", "artist": "King Gnu", "file": "specialz.mp3", "image": "specialz.jpg"},
    {"id": 6, "title": "Superpower", "artist": "Kiss of Life", "file": "superpower.mp3", "image": "superpower.webp"},
    {"id": 7, "title": "Just Keep Watching", "artist": "Tate McRae", "file": "justkeepwatching.mp3", "image": "justkeepwatching.png"},
    {"id": 8, "title": "StarBoy", "artist": "The Weeknd", "file": "starboy.mp3", "image": "starboy.jpg"},
    {"id": 9, "title": "KuLoSa", "artist": "Oxlade", "file": "kulosa.mp3", "image": "kulosa.jpg"},
    {"id": 10, "title": "Espresso", "artist": "Sabrina Carpenter", "file": "espresso.mp3", "image": "espresso.png"},
    {"id": 11, "title": "Middle of the night", "artist": "Elley Duhe", "file": "middleofthenight.mp3", "image": "middleofthenight.png"},
    {"id": 12, "title": "One Dance", "artist": "Drake", "file": "onedance.mp3", "image": "onedance.png"},
    {"id": 13, "title": "Shape of you", "artist": "Ed Sheeran", "file": "shapeofyou.mp3", "image": "shapeofyou.png"},
    {"id": 14, "title": "Taki Taki", "artist": "Dj Snake", "file": "takitaki.mp3", "image": "takitaki.png"},
    {"id": 15, "title": "Let me Love You", "artist": "Justin Bieber", "file": "letmeloveyou.mp3", "image": "letmeloveyou.jpg"},
    {"id": 16, "title": "Perfect", "artist": "Ed Sheeran", "file": "perfect.mp3", "image": "perfect.jpg"}
]


# --- Routes --- #
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', songs=SONGS, user=session['user'])


@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    query = request.args.get('query', '').lower()
    results = [s for s in SONGS if query in s['title'].lower() or query in s['artist'].lower()]
    return render_template('search.html', results=results, query=query, user=session['user'])


@app.route('/player/<int:song_id>')
def player(song_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    song = next((s for s in SONGS if s["id"] == song_id), None)
    if not song:
        return "Song not found", 404

    # ✅ Smart recommendation system
    same_artist = [s for s in SONGS if s["artist"] == song["artist"] and s["id"] != song_id]
    other_songs = [s for s in SONGS if s["artist"] != song["artist"]]
    random.shuffle(other_songs)

    # Combine: prioritize same artist, then fill from others
    related = same_artist + other_songs
    random.shuffle(related)
    related = related[:6]

    return render_template("player.html", song=song, related=related, songs=SONGS, user=session['user'])


# --- Authentication --- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("⚠️ Username already exists!", "error")
            conn.close()
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()

        flash("✅ Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash("✅ Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("❌ Invalid username or password!", "error")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("👋 You have been logged out.", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

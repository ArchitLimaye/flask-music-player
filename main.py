import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import random
from flask import Flask
from deepface import DeepFace
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import random


app = Flask(__name__)
app.secret_key = "supersecretkey"

# --- Folders for image uploads --- #
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# --- DB Connection Helper --- #
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


# --- SONG DATA --- #
SONGS = [
    {"id": 1, "title": "Iris Out", "artist": "Kenshi Yonezu", "file": "irisOut.mp3", "image": "irisOut.webp", "genre": "Lo-fi", "language": "English"},
    {"id": 2, "title": "Blinding Lights", "artist": "The Weeknd", "file": "blindingLights.mp3", "image": "blindingLights.png", "genre": "Pop", "language": "English"},
    {"id": 3, "title": "Let the world burn", "artist": "Chris Grey", "file": "lettheworldburn.mp3", "image": "lettheworldburn.jpg", "genre": "Rock", "language": "English"},
    {"id": 4, "title": "Saphire", "artist": "Ed Sheeran", "file": "saphire.mp3", "image": "saphire.png", "genre": "Acoustic", "language": "English"},
    {"id": 5, "title": "Specialz", "artist": "King Gnu", "file": "specialz.mp3", "image": "specialz.jpg", "genre": "Rock", "language": "English"},
    {"id": 6, "title": "Superpower", "artist": "Kiss of Life", "file": "superpower.mp3", "image": "superpower.webp", "genre": "Pop", "language": "English"},
    {"id": 7, "title": "Just Keep Watching", "artist": "Tate McRae", "file": "justkeepwatching.mp3", "image": "justkeepwatching.png", "genre": "Acoustic", "language": "English"},
    {"id": 8, "title": "StarBoy", "artist": "The Weeknd", "file": "starboy.mp3", "image": "starboy.jpg", "genre": "EDM", "language": "English"},
    {"id": 9, "title": "KuLoSa", "artist": "Oxlade", "file": "kulosa.mp3", "image": "kulosa.jpg", "genre": "Lo-fi", "language": "English"},
    {"id": 10, "title": "Espresso", "artist": "Sabrina Carpenter", "file": "espresso.mp3", "image": "espresso.png", "genre": "Pop", "language": "English"},
    {"id": 11, "title": "Middle of the night", "artist": "Elley Duhe", "file": "middleofthenight.mp3", "image": "middleofthenight.png", "genre": "EDM", "language": "English"},
    {"id": 12, "title": "One Dance", "artist": "Drake", "file": "onedance.mp3", "image": "onedance.png", "genre": "Rap/Hip-Hop", "language": "English"},
    {"id": 13, "title": "Shape of you", "artist": "Ed Sheeran", "file": "shapeofyou.mp3", "image": "shapeofyou.png", "genre": "Pop", "language": "English"},
    {"id": 14, "title": "Taki Taki", "artist": "Dj Snake", "file": "takitaki.mp3", "image": "takitaki.png", "genre": "EDM", "language": "English"},
    {"id": 15, "title": "Let me Love You", "artist": "Justin Bieber", "file": "letmeloveyou.mp3", "image": "letmeloveyou.jpg", "genre": "Pop", "language": "English"},
    {"id": 16, "title": "Perfect", "artist": "Ed Sheeran", "file": "perfect.mp3", "image": "perfect.jpg", "genre": "Acoustic", "language": "English"},
    {"id": 17, "title": "Moral of the Story", "artist": "Ashe", "file": "moralofthestory.mp3", "image": "moralofthestory.jpg", "genre": "Acoustic", "language": "English"},
    {"id": 18, "title": "Runaway", "artist": "Aurora", "file": "runaway.mp3", "image": "runaway.png", "genre": "Lo-fi", "language": "English"},
    {"id": 19, "title": "Snowman", "artist": "Sia", "file": "snowman.mp3", "image": "snowman.jpeg", "genre": "Lo-fi", "language": "English"},
    {"id": 20, "title": "Cheap Thrills", "artist": "Sia", "file": "cheapthrills.mp3", "image": "cheapthrills.png", "genre": "Pop", "language": "English"},
    {"id": 21, "title": "Happy", "artist": "Pharrell Williams", "file": "happy.mp3", "image": "happy.jpg", "genre": "Pop", "language": "English"},
    {"id": 22, "title": "Believer", "artist": "Imagine Dragons", "file": "beliver.mp3", "image": "believer.jpg", "genre": "Rock", "language": "English"},
    {"id": 23, "title": "Night Changes", "artist": "One Direction", "file": "nightchanges.mp3", "image": "nightchanges.png", "genre": "Acoustic", "language": "English"},
    {"id": 24, "title": "Closer", "artist": "Chainsmokers", "file": "closer.mp3", "image": "closer.png", "genre": "EDM", "language": "English"},
    {"id": 25, "title": "Lover", "artist": "Taylor Swift", "file": "lover.mp3", "image": "lover.png", "genre": "Pop", "language": "English"},
    {"id": 26, "title": "Story of my Life", "artist": "One Direction", "file": "storyofmylife.mp3", "image": "storyofmylife.png", "genre": "Pop", "language": "English"},
    {"id": 27, "title": "Perfect", "artist": "One Direction", "file": "perfect2.mp3", "image": "perfect2.png", "genre": "Acoustic", "language": "English"},
    {"id": 28, "title": "Until I Found You", "artist": "Stephen Sanchez", "file": "untilifoundyou.mp3", "image": "untilifoundyou.png", "genre": "Lo-fi", "language": "English"},
    {"id": 29, "title": "Good For You", "artist": "Selena Gomez", "file": "goodforyou.mp3", "image": "goodforyou.png", "genre": "Pop", "language": "English"},
    {"id": 30, "title": "I Wanna Be Yours", "artist": "Arctic Monkeys", "file": "iwannabeyours.mp3", "image": "iwannabeyours.jpg", "genre": "Rock", "language": "English"},
    {"id": 31, "title": "Animals", "artist": "Maroon 5", "file": "animals.mp3", "image": "animals.png", "genre": "Pop", "language": "English"},
    {"id": 32, "title": "As It Was", "artist": "Harry Styles", "file": "asitwas.mp3", "image": "asitwas.png", "genre": "Pop", "language": "English"},
    {"id": 33, "title": "Softcore", "artist": "The Neighbourhood", "file": "softcore.mp3", "image": "neighbourhood.jpg", "genre": "Lo-fi", "language": "English"},
    {"id": 34, "title": "Danza Kuduro", "artist": "Don Omar ft. Lucenzo", "file": "danzakuduro.mp3", "image": "danzakudro.jpg", "genre": "EDM", "language": "Spanish"},
    {"id": 35, "title": "Tainu Khabar Nahi", "artist": "Arijit Singh", "file": "tainukhabarnahi.mp3", "image": "tainukhabarnahi.jpg", "genre": "Acoustic", "language": "Hindi"},
    {"id": 36, "title": "Jeena Jeena", "artist": "Atif Aslam", "file": "jeenajeena.mp3", "image": "jeenajeena.jpeg", "genre": "Acoustic", "language": "Hindi"},
    {"id": 37, "title": "Akhiyan Gulab", "artist": "Mitraz", "file": "akhiyangulab.mp3", "image": "akhiyaangulab.jpg", "genre": "Acoustic", "language": "Hindi"},
    {"id": 38, "title": "Apna Bana Le", "artist": "Arijit Singh", "file": "apnabanale.mp3", "image": "apnabanale.jpg", "genre": "Acoustic", "language": "Hindi"},
    {"id": 35, "title": "Tainu Khabar Nahi", "artist": "Arijit Singh", "file": "tainukhabarnahi.mp3", "image": "tainukhabarnahi.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 36, "title": "Jeena Jeena", "artist": "Atif Aslam", "file": "jeenajeena.mp3", "image": "jeenajeena.jpeg", "genre": "Acoustic", "language": "Hindi"},
{"id": 37, "title": "Akhiyan Gulab", "artist": "Mitraz", "file": "akhiyangulab.mp3", "image": "akhiyaangulab.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 38, "title": "Apna Bana Le", "artist": "Arijit Singh", "file": "apnabanale.mp3", "image": "apnabanale.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 39, "title": "Mast Magan", "artist": "Arijit Singh", "file": "mastmagan.mp3", "image": "mastmagan.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 40, "title": "Chaleya", "artist": "Arijit Singh", "file": "chaleya.mp3", "image": "chaleya.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 41, "title": "Jo Tum Na Ho", "artist": "Arijit Singh", "file": "jotumnoho.mp3", "image": "jotumnaho.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 42, "title": "Deva Deva", "artist": "Arijit Singh", "file": "devadeva.mp3", "image": "devadeva.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 43, "title": "Deewani Mastani", "artist": "Shreya Ghoshal", "file": "deewanimastani.mp3", "image": "deewanimastani.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 44, "title": "Let Me Down Slowly", "artist": "Alec Benjamin", "file": "letmedownslowly.mp3", "image": "letmedownslowly.png", "genre": "Pop", "language": "English"},
{"id": 45, "title": "Love Me Like You Do", "artist": "Ellie Goulding", "file": "lovemelikeyoudo.mp3", "image": "lovemelikeyoudo.jpeg", "genre": "Pop", "language": "English"},
{"id": 46, "title": "Señorita", "artist": "Shawn Mendes & Camila Cabello", "file": "senorita.mp3", "image": "senorita.png", "genre": "Pop", "language": "English"},
{"id": 47, "title": "What Makes You Beautiful", "artist": "One Direction", "file": "whatmakesyoubeautiful.mp3", "image": "whatmakesyoubeautiful.jpeg", "genre": "Pop", "language": "English"},
{"id": 43, "title": "Deewani Mastani", "artist": "Shreya Ghoshal", "file": "deewanimastani.mp3", "image": "deewanimastani.jpg", "genre": "Acoustic", "language": "Hindi"},
{"id": 44, "title": "Let Me Down Slowly", "artist": "Alec Benjamin", "file": "letmedownslowly.mp3", "image": "letmedownslowly.png", "genre": "Pop", "language": "English"},
{"id": 45, "title": "Love Me Like You Do", "artist": "Ellie Goulding", "file": "lovemelikeyoudo.mp3", "image": "lovemelikeyoudo.jpeg", "genre": "Pop", "language": "English"},
{"id": 46, "title": "Allah Duhai Hai", "artist": "Atif Aslam", "file": "allahduhaihai.mp3", "image": "allahduhaihai.jpg", "genre": "EDM", "language": "Hindi"},




]



# --- ROUTES --- #


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    sort_by = request.args.get('sort', None)

    # ✅ Always start fresh with a clean copy
    songs_list = SONGS[:]  

    # Randomize by default
    random.shuffle(songs_list)

    # Sort when requested
    if sort_by == 'language':
        songs_list = sorted(songs_list, key=lambda x: x['language'])

    return render_template('index.html', songs=songs_list, user=session['user'], sort_by=sort_by)

@app.route('/search')
def search():
    if 'user' not in session:
        return redirect(url_for('login'))
    query = request.args.get('query', '').lower()
    results = [s for s in SONGS if query in s['title'].lower() or query in s['artist'].lower() or query in s['genre'].lower()]
    return render_template('search.html', results=results, query=query, user=session['user'])


# === PLAYER PAGE === #
@app.route('/player/<int:song_id>')
def player(song_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    song = next((s for s in SONGS if s["id"] == song_id), None)
    if not song:
        return "Song not found", 404

    same_genre = [s for s in SONGS if s["genre"].lower() == song["genre"].lower() and s["id"] != song_id]
    same_artist = [s for s in SONGS if s["artist"] == song["artist"] and s["id"] != song_id]
    remaining = [s for s in SONGS if s["id"] != song_id and s not in same_genre + same_artist]
    random.shuffle(same_genre)
    random.shuffle(same_artist)
    random.shuffle(remaining)
    related = (same_genre[:4] + same_artist[:2] + remaining[:4])[:6]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE user = ?", (session['user'],))
    user_playlists = cursor.fetchall()
    cursor.execute("SELECT playlist_id FROM playlist_songs WHERE song_id = ?", (song_id,))
    existing_playlists = [row['playlist_id'] for row in cursor.fetchall()]
    conn.close()

    return render_template(
        "player.html",
        song=song,
        related=related,
        songs=SONGS,
        user=session['user'],
        user_playlists=user_playlists,
        existing_playlists=existing_playlists
    )


# === FACIAL EMOTION DETECTION === #
@app.route('/emotion')
def emotion_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('emotion.html', user=session['user'])


@app.route('/detect_emotion', methods=['POST'])
def detect_emotion():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'image' not in request.files:
        flash("⚠️ Please upload an image.", "error")
        return redirect(url_for('emotion_page'))

    image = request.files['image']
    if image.filename == "":
        flash("⚠️ No image selected!", "error")
        return redirect(url_for('emotion_page'))

    if not allowed_file(image.filename):
        flash("⚠️ Only image files (png, jpg, jpeg, webp) are allowed.", "error")
        return redirect(url_for('emotion_page'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filepath)

    try:
        result = DeepFace.analyze(img_path=filepath, actions=["emotion"], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]
        emotion = result.get("dominant_emotion", "Neutral").capitalize()

        emotion_genre_map = {
            "Happy": "Pop",
            "Sad": "Acoustic",
            "Angry": "Rock",
            "Neutral": "Lo-fi",
            "Surprise": "EDM",
            "Fear": "Lo-fi",
            "Disgust": "Rap/Hip-Hop"
        }

        genre = emotion_genre_map.get(emotion, "Pop")
        recommended = [s for s in SONGS if s["genre"].lower() == genre.lower()]
        random.shuffle(recommended)
        recommended = recommended[:6]

        return render_template(
            "emotion_result.html",
            emotion=emotion,
            genre=genre,
            image_file=image.filename,
            recommended=recommended,
            user=session['user']
        )
    except Exception as e:
        flash(f"❌ Error detecting emotion: {e}", "error")
        return redirect(url_for('emotion_page'))


# === PLAYLIST SYSTEM === #
@app.route('/playlists')
def playlists():
    if 'user' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE user = ?", (session['user'],))
    playlists = cursor.fetchall()
    conn.close()
    return render_template('playlists.html', playlists=playlists, user=session['user'])


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    if 'user' not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO playlists (user, name) VALUES (?, ?)", (session['user'], name))
    conn.commit()
    conn.close()
    flash(f"✅ Playlist '{name}' created!", "success")
    return redirect(url_for('playlists'))


@app.route('/playlist/<int:playlist_id>')
def view_playlist(playlist_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE id = ? AND user = ?", (playlist_id, session['user']))
    playlist = cursor.fetchone()
    if not playlist:
        conn.close()
        flash("⚠️ Playlist not found!", "error")
        return redirect(url_for('playlists'))

    cursor.execute("SELECT song_id FROM playlist_songs WHERE playlist_id = ?", (playlist_id,))
    song_ids = [row['song_id'] for row in cursor.fetchall()]
    songs = [s for s in SONGS if s['id'] in song_ids]
    conn.close()
    return render_template('view_playlist.html', playlist=playlist, songs=songs, user=session['user'])


# === AJAX ADD TO PLAYLIST === #
@app.route('/add_to_playlist/<int:song_id>', methods=['POST'])
def add_to_playlist(song_id):
    if 'user' not in session:
        return jsonify({"status": "unauthorized", "message": "Please log in first."}), 401

    playlist_id = request.form.get('playlist_id')
    if not playlist_id:
        return jsonify({"status": "error", "message": "Missing playlist ID"}), 400

    try:
        playlist_id = int(playlist_id)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid playlist ID"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists WHERE id = ? AND user = ?", (playlist_id, session['user']))
    playlist = cursor.fetchone()
    if not playlist:
        conn.close()
        return jsonify({"status": "error", "message": "Invalid playlist or access denied"}), 403

    cursor.execute("SELECT * FROM playlist_songs WHERE playlist_id = ? AND song_id = ?", (playlist_id, song_id))
    if cursor.fetchone():
        conn.close()
        return jsonify({"status": "exists", "message": "Already in playlist"}), 200

    cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (?, ?)", (playlist_id, song_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "🎵 Song added successfully!"}), 200


# === AUTHENTICATION === #
@app.route('/register', methods=['GET', 'POST'])
def register():
    session.pop('_flashes', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            flash("⚠️ Username already exists!", "error")
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
    session.pop('_flashes', None)
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


# =====================================================================
#                    ADDITIONS (NON-DESTRUCTIVE)
# =====================================================================

# --- Genre playlists page ---
@app.route("/genremusic")
def show_genre_music():
    if 'user' not in session:
        return redirect(url_for('login'))

    genre_groups = {}
    for s in SONGS:
        genre_groups.setdefault(s["genre"], []).append(s)

    return render_template("genremusic.html", genre_groups=genre_groups, user=session["user"])

# --- Artist playlists page ---
@app.route("/artistmusic")
def show_artist_music():
    if 'user' not in session:
        return redirect(url_for('login'))

    artist_groups = {}
    for s in SONGS:
        artist_groups.setdefault(s["artist"], []).append(s)

    return render_template("artistmusic.html", artist_groups=artist_groups, user=session["user"])

# --- View songs by a single genre ---
@app.route("/genre/<genre>")
def view_genre_songs(genre):
    if 'user' not in session:
        return redirect(url_for('login'))
    genre_songs = [s for s in SONGS if s["genre"].lower() == genre.lower()]
    return render_template("view_playlist.html", songs=genre_songs, title=f"{genre} Songs", user=session["user"])

# --- View songs by a single artist ---
@app.route("/artist/<artist>")
def view_artist_songs(artist):
    if 'user' not in session:
        return redirect(url_for('login'))
    artist_songs = [s for s in SONGS if s["artist"].lower() == artist.lower()]
    return render_template("view_playlist.html", songs=artist_songs, title=f"{artist} Songs", user=session["user"])

# --- Lyra assistant endpoint ---
@app.route("/lyra", methods=["POST"])
def lyra_reply():
    user_msg = (request.json or {}).get("message", "").lower()

    if any(k in user_msg for k in ["recommend", "menu", "options"]):
        reply = {
            "type": "options",
            "message": "✨ Choose how you'd like me to recommend music:",
            "buttons": [
                {"label": "🎧 Genre Based", "link": "/genremusic"},
                {"label": "🎤 Artist Based", "link": "/artistmusic"},
                {"label": "😄 Facial Emotion", "link": "/emotion"}
            ]
        }
    elif any(k in user_msg for k in ["hi", "hello", "hey"]):
        reply = {"type": "text", "message": "Hey there! 👋 I’m Lyra — your music companion. Type 'recommend' to see options!"}
    elif any(k in user_msg for k in ["Weeknd ", "weeknd "]):
        reply = {"type": "text", "message": "🔥 The Weeknd always delivers! Try 'Starboy' or 'Blinding Lights'."}
    elif any(k in user_msg for k in ["Ed Sheeran ", "Ed sheeran "]):
        reply = {"type": "text", "message": "I Love his songs! Try listening to Perfect and Shape of you"}    
    else:
        reply = {"type": "text", "message": "I'm Lyra 🎶 — try typing 'recommend' to see my recommendation modes!"}

    return jsonify(reply)

# =====================================================================

if __name__ == '__main__':
    app.run(debug=True)

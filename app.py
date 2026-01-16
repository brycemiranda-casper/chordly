from flask import Flask, render_template, request, jsonify
from search_by_name import search_by_name_logic
from recognize_from_path import recognize_from_path_logic
from db import get_db_connection
import os

app = Flask(__name__)

# --- DEPLOYMENT CONFIG ---
PORT = int(os.environ.get("PORT", 5000))
UPLOAD_FOLDER = 'temp_uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- DATABASE BOOTSTRAP ---
# This automatically creates your table in Aiven if it doesn't exist
def create_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_chords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                artist VARCHAR(255),
                chord_text TEXT NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database table checked/created successfully!")
    except Exception as e:
        print(f"Database bootstrap error: {e}")

# Run the check immediately when the app starts
create_tables()

@app.route("/", methods=["GET", "POST"])
def index():
    chords_text = None
    result = None

    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            mode = data.get("mode")
        else:
            mode = request.form.get("mode")

        # 1. SEARCH BY SONG NAME
        if mode == "name":
            song_name = request.form.get("song_name", "").strip()
            result = search_by_name_logic(song_name)

        # 2. IDENTIFY BY FILE UPLOAD
        elif mode == "file":
            if "song_file" not in request.files:
                return "No file part", 400
            
            file = request.files["song_file"]
            if file.filename == '':
                return "No selected file", 400
                
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            result = recognize_from_path_logic(path)

        # Process the result for the chords_text
        if result and result.get("chords"):
            chords_text = result["chords"]
        elif result and result.get("chord_file"):
            chord_path = os.path.join("chords", result["chord_file"])
            if os.path.exists(chord_path):
                with open(chord_path, "r", encoding="utf-8") as f:
                    chords_text = f.read()
            else:
                chords_text = "Chord file not found."

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({
                "chords_text": chords_text,
                "result": result
            })

        return render_template(
            "result.html",
            chords_text=chords_text,
            result=result
        )

    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    success_msg = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        artist = request.form.get("artist", "").strip()
        chords = request.form.get("chords", "").strip()

        if not title or not chords:
            return "Title and chords are required", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user_chords (title, artist, chord_text) VALUES (%s, %s, %s)",
                (title, artist, chords)
            )
            conn.commit()
            success_msg = "Chord sheet uploaded successfully!"
        except Exception as e:
            return f"Database error: {e}", 500
        finally:
            cursor.close()
            conn.close()

    return render_template("upload.html", success=success_msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)
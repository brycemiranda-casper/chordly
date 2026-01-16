from db import get_db_connection
import os

CHORDS_DIR = "../chords"

def get_chords(song_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT title, artist, chord_file FROM songs WHERE id = %s",
        (song_id,)
    )
    song = cursor.fetchone()

    cursor.close()
    conn.close()

    if not song or not song["chord_file"]:
        print("Chord sheet not found.")
        return

    chord_path = os.path.join(CHORDS_DIR, song["chord_file"])

    if not os.path.exists(chord_path):
        print("Chord file missing:", chord_path)
        return

    print(f"\n===== {song['title']} - {song['artist']} =====\n")
    with open(chord_path, "r", encoding="utf-8") as f:
        print(f.read())

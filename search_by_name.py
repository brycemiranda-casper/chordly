from db import get_db_connection
import re

def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def search_by_name_logic(user_input):
    conn = get_db_connection()

    
    cursor = conn.cursor(dictionary=True, buffered=True)   
    
    cursor.execute(
        "SELECT title, artist, chord_text FROM user_chords WHERE title LIKE %s",
        ("%" + user_input + "%",)
    )
    user_result = cursor.fetchone()

    if user_result:
        cursor.close()
        conn.close()
        return {
            "title": user_result["title"],
            "artist": user_result["artist"],
            "chords": user_result["chord_text"]
        }

    
        
    cursor.execute("""
        SELECT id, title, artist, chord_file
        FROM songs
    """)
    songs = cursor.fetchall()

    cursor.close()
    conn.close()

    if not songs:
        return None

    input_words = normalize(user_input).split()

    best_match = None
    best_score = 0

    for song in songs:
        title_norm = normalize(song["title"])
        score = sum(1 for w in input_words if w in title_norm)

        if score > best_score:
            best_score = score
            best_match = song

    return best_match if best_score > 0 else None

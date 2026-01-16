from fingerprint import generate_fingerprint
from db import get_db_connection

SIMILARITY_THRESHOLD = 0.15

def fingerprint_similarity(fp1, fp2):
    length = min(len(fp1), len(fp2))
    if length == 0:
        return 0
    return sum(1 for i in range(length) if fp1[i] == fp2[i]) / length


def recognize_from_path_logic(file_path):
    unknown_fp, unknown_duration = generate_fingerprint(file_path)

    if unknown_fp is None:
        return None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()

    best_match = None
    best_score = 0

    for song in songs:
        if abs(song["duration"] - unknown_duration) > 5:
            continue

        score = fingerprint_similarity(unknown_fp, song["fingerprint"])

        if score > best_score:
            best_score = score
            best_match = song

    cursor.close()
    conn.close()

    if best_match and best_score >= SIMILARITY_THRESHOLD:
        return best_match

    return None

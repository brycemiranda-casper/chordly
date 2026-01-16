import mysql.connector
import os

def get_db_connection():
    # This looks for the variables you typed into Render
    # If it can't find them (like on your laptop), it uses the "localhost" defaults
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASS', 'brycee2044'),
        database=os.environ.get('DB_NAME', 'chordify_audio'),
        port=os.environ.get('DB_PORT', '28995')
    )
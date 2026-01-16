import mysql.connector
import os

def get_db_connection():
    # This grabs the Aiven info from the Render Environment tab
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASS'),
        database=os.environ.get('DB_NAME'),
        port=int(os.environ.get('DB_PORT', 28995))
    )



#import mysql.connector
#def get_db_connection():
#    return mysql.connector.connect(
#        host="localhost",
#        user="root",
#        password="brycee2044",
#        database="chordify_audio"
#    )

import sqlite3

def create_database():
    conn = sqlite3.connect('temp.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            imdb_id TEXT,
            overview TEXT,
            detailed_description TEXT,
            overview_embedding BLOB
        )
    ''')

    conn.commit()
    conn.close()
    print("The database and the table were successfully created")

if __name__ == "__main__":
    create_database()

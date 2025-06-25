#initialize SQL3 database
import sqlite3

#init
def init_db(db_path="data/inventory.db"):
    #connect and create file if needed
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    #create table if needed
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL
        )
    """)

    #persist changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Initialized inventory.db with table 'inventory'")
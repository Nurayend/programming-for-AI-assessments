import sqlite3
import os

def init_database():
    """
    Initializes the SQLite database using the schema.sql file.
    This creates the tables and populates them with initial mock data.
    """
    db_filename = 'data/university.db'
    sql_filename = 'data/schema.sql'
    
    # Check if the SQL schema file exists
    if not os.path.exists(sql_filename):
        print(f"[ERROR] File '{sql_filename}' not found.")
        return

    try:
        # Connect to SQLite (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        
        print("[INFO] Reading SQL schema...")
        with open(sql_filename, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        print("[INFO] Executing SQL script...")
        cursor.executescript(sql_script)
        
        conn.commit()
        print(f"[SUCCESS] Database '{db_filename}' created and initialized.")
        
        # Verification: Print students to confirm data insertion
        print("\n--- Verification: Student List ---")
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        for s in students:
            print(s)
            
    except sqlite3.Error as e:
        print(f"[DATABASE ERROR] {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_database()
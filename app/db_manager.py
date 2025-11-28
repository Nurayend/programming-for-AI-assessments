"""
FILE: app/database_manager.py
DESCRIPTION:
    This is the "engine" of our application. It handles all direct interactions 
    with the SQLite database.

TEAM TASKS:
    1. Create a class (e.g., 'DatabaseManager') to handle connections.
    2. Implement 'CREATE' methods: add_student(), log_survey(), submit_assignment().
    3. Implement 'READ' methods: get_student_by_id(), get_all_surveys().
    4. Ensure all SQL queries use '?' placeholders to prevent SQL Injection.
    
    *Requirement: This file must demonstrate the ability to store and retrieve 
    data from a relational database[cite: 54, 73].*
"""
import sqlite3

# Connecting to the database
conn = sqlite3.connect('university.db')
cur = conn.cursor()

# Reading a file schema.sql
with open('data/schema.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Running all scripts
cur.executescript(sql_script)

conn.commit()
conn.close()

# to check that schema.sql is filled correct (it is)
# print("Database created and filled with mock data")
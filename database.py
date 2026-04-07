import sqlite3

conn = sqlite3.connect("clinic.db", check_same_thread=False)
cursor = conn.cursor()

# Patients
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    symptoms TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Queue with more info
cursor.execute("""
CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    score INTEGER,
    priority TEXT,
    status TEXT DEFAULT 'waiting',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

import sqlite3

conn = sqlite3.connect("clinic.db", check_same_thread=False)
cursor = conn.cursor()
import sqlite3

# Connect to database (this creates the file if it doesn't exist)
conn = sqlite3.connect("clinic.db", check_same_thread=False)
cursor = conn.cursor()

# Create the patients table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    symptoms TEXT NOT NULL
)
""")

# Create the queue table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    score INTEGER,
    priority TEXT,
    status TEXT DEFAULT 'waiting',
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

conn.commit()
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

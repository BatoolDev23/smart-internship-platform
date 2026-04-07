import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "smart_internship.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Students Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        university TEXT,
        major TEXT,
        skills TEXT,
        experience_years INTEGER,
        knowledge_areas TEXT,
        location TEXT,
        gpa REAL,
        language TEXT DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Internships Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS internships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_en TEXT NOT NULL,
        title_ar TEXT NOT NULL,
        company_en TEXT,
        company_ar TEXT,
        description_en TEXT,
        description_ar TEXT,
        required_skills TEXT,
        required_experience INTEGER,
        knowledge_areas TEXT,
        location TEXT,
        duration_weeks INTEGER,
        is_remote BOOLEAN,
        university_filter TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Applications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        internship_id INTEGER,
        match_score REAL,
        skills_score REAL,
        experience_score REAL,
        knowledge_score REAL,
        location_score REAL,
        status TEXT DEFAULT 'pending',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (internship_id) REFERENCES internships(id)
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

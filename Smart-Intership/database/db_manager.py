import sqlite3
from database.schema import DB_PATH
import pandas as pd

class DBManager:
    def __init__(self):
        self.db_path = DB_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_student(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        
        cursor.execute(f"INSERT INTO students ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        student_id = cursor.lastrowid
        conn.close()
        return student_id
        
    def get_internships(self):
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM internships", conn)
        conn.close()
        return df
        
    def save_application(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        
        cursor.execute(f"INSERT INTO applications ({columns}) VALUES ({placeholders})", values)
        conn.commit()
        app_id = cursor.lastrowid
        conn.close()
        return app_id

    def check_application_exists(self, student_id, internship_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM applications WHERE student_id=? AND internship_id=?", (student_id, internship_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None

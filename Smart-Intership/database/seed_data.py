import sqlite3
from database.schema import init_db, DB_PATH
import os

def seed_database():
    # First ensure schema is initialized
    init_db()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM internships")
    if cursor.fetchone()[0] > 0:
        print("Database already seeded.")
        conn.close()
        return

    # Dummy data
    internships = [
        {
            "title_en": "Software Engineering Intern",
            "title_ar": "متدرب هندسة برمجيات",
            "company_en": "TechPioneers Jordan",
            "company_ar": "رواد التقنية الأردن",
            "description_en": "Join our backend team to build scalable Python systems.",
            "description_ar": "انضم إلى فريق تطوير الواجهات الخلفية لبناء أنظمة بايثون قابلة للتوسع.",
            "required_skills": "Python, SQL, FastApi, Git",
            "required_experience": 0,
            "knowledge_areas": "Backend, API Design, Databases",
            "location": "Amman",
            "duration_weeks": 12,
            "is_remote": 0,
            "university_filter": "all"
        },
        {
            "title_en": "Data Science Trainee",
            "title_ar": "متدرب علم بيانات",
            "company_en": "DataMinds",
            "company_ar": "عقول البيانات",
            "description_en": "Work on real-world ML models using scikit-learn and pandas.",
            "description_ar": "العمل على نماذج تعلم الآلة في العالم الحقيقي باستخدام scikit-learn.",
            "required_skills": "Python, Machine Learning, Pandas, SQL",
            "required_experience": 1,
            "knowledge_areas": "Data Science, ML, Analytics",
            "location": "Irbid",
            "duration_weeks": 8,
            "is_remote": 1,
            "university_filter": "Al-Huson University College"
        },
        {
            "title_en": "Frontend Web Intern",
            "title_ar": "متدرب تطوير واجهات أمامية",
            "company_en": "Amman Web Solutions",
            "company_ar": "حلول عمان لتطوير الويب",
            "description_en": "Create interactive UI using React and modern CSS.",
            "description_ar": "إنشاء واجهات مستخدم تفاعلية باستخدام React و CSS الحديث.",
            "required_skills": "HTML, CSS, JavaScript, React",
            "required_experience": 0,
            "knowledge_areas": "Frontend, UI/UX, Web Design",
            "location": "Amman",
            "duration_weeks": 16,
            "is_remote": 0,
            "university_filter": "Al-Balqa Applied University"
        },
        {
            "title_en": "AI Research Assistant (Intern)",
            "title_ar": "مساعد باحث في الذكاء الاصطناعي (متدرب)",
            "company_en": "AI Horizons Labs",
            "company_ar": "مختبرات آفاق الذكاء الاصطناعي",
            "description_en": "Assist in researching LLMs and NLP techniques.",
            "description_ar": "المساعدة في البحث في النماذج اللغوية الكبيرة وتقنيات معالجة اللغة الطبيعية.",
            "required_skills": "Python, NLP, Deep Learning, PyTorch",
            "required_experience": 1,
            "knowledge_areas": "AI, NLP, Research",
            "location": "Irbid",
            "duration_weeks": 24,
            "is_remote": 1,
            "university_filter": "Al-Huson University College"
        },
        {
            "title_en": "Cybersecurity Analyst Intern",
            "title_ar": "متدرب تحليل أمن سيبراني",
            "company_en": "SecureNet Jordan",
            "company_ar": "شبكة الأمن الأردن",
            "description_en": "Learn penetration testing and vulnerability assessment.",
            "description_ar": "تعلم اختبار الاختراق وتقييم الثغرات الأمنية.",
            "required_skills": "Networking, Linux, Penetration Testing, Security",
            "required_experience": 0,
            "knowledge_areas": "Cybersecurity, Networking",
            "location": "Irbid",
            "duration_weeks": 12,
            "is_remote": 0,
            "university_filter": "Al-Balqa Applied University"
        }
    ]

    for data in internships:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        cursor.execute(f"INSERT INTO internships ({columns}) VALUES ({placeholders})", values)

    conn.commit()
    print("Database seeded with sample internships!")
    conn.close()

if __name__ == "__main__":
    seed_database()

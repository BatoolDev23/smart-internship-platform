import streamlit as st
from ui.translations import t
from ui.components import header

def show():
    header()
    lang = st.session_state.get('language', 'en')
    texts = t[lang]
    
    st.markdown(f"<h2>{texts['form_title']}</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader(texts['personal_info'])
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(texts['full_name'], value=st.session_state.get('student_data', {}).get('name', ''))
            email = st.text_input(texts['email'], value=st.session_state.get('student_data', {}).get('email', ''))
        with col2:
            university = st.selectbox(texts['university'], 
                                    ["Al-Balqa Applied University", "Al-Huson University College"],
                                    index=0 if st.session_state.get('student_data', {}).get('university') == "Al-Balqa Applied University" else 1)
            major = st.text_input(texts['major'], value=st.session_state.get('student_data', {}).get('major', ''))
            
        col3, col4 = st.columns(2)
        with col3:
            gpa = st.number_input(texts['gpa'], min_value=0.0, max_value=4.0, value=float(st.session_state.get('student_data', {}).get('gpa', 3.0)), step=0.1)
        with col4:
            location = st.text_input(texts['location'], value=st.session_state.get('student_data', {}).get('location', ''))

    with st.container(border=True):
        st.subheader(texts['skills_exp'])
        skills = st.text_area(texts['skills'], value=st.session_state.get('student_data', {}).get('skills', 'Python, SQL, Communication'), help="Separate by commas")
        knowledge_areas = st.text_area(texts['knowledge_areas'], value=st.session_state.get('student_data', {}).get('knowledge_areas', 'Machine Learning, Web Development'), help="Separate by commas")
        experience_years = st.slider(texts['experience_years'], min_value=0, max_value=10, value=int(st.session_state.get('student_data', {}).get('experience_years', 0)))

    if st.button(texts['submit'], type="primary"):
        if not name or not email:
            st.error("Name and Email are required.")
        else:
            std_data = {
                'name': name,
                'email': email,
                'university': university,
                'major': major,
                'gpa': gpa,
                'location': location,
                'skills': skills,
                'knowledge_areas': knowledge_areas,
                'experience_years': experience_years,
                'language': lang
            }
            st.session_state.student_data = std_data
            
            with st.spinner(texts['processing']):
                from database.db_manager import DBManager
                db = DBManager()
                # Store student in DB
                student_id = db.create_student(std_data)
                st.session_state.student_id = student_id
                
            st.session_state.current_page = "recommendations"
            st.rerun()

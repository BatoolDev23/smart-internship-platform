import streamlit as st

# Must be the first streamlit call
st.set_page_config(
    page_title="SmartSkill Internships",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui.translations import t
from ui.pages import home, about, student_form, recommendations

# Initialize DB on start if not exists
from database.seed_data import seed_database
try:
    seed_database()
except Exception as e:
    pass

# Initialize session state for language and page navigation
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

lang = st.session_state.language
texts = t[lang]

# Sidebar
with st.sidebar:
    st.title("SmartSkill")
    st.write("---")
    
    # Navigation Buttons
    if st.button(texts['home'], use_container_width=True, type="primary" if st.session_state.current_page == 'home' else "secondary"):
        st.session_state.current_page = 'home'
        st.rerun()
        
    if st.button(texts['about'], use_container_width=True, type="primary" if st.session_state.current_page == 'about' else "secondary"):
        st.session_state.current_page = 'about'
        st.rerun()
        
    if st.button(texts['student_profile'], use_container_width=True, type="primary" if st.session_state.current_page == 'student_form' else "secondary"):
        st.session_state.current_page = 'student_form'
        st.rerun()
        
    if st.button(texts['recommendations'], use_container_width=True, type="primary" if st.session_state.current_page == 'recommendations' else "secondary"):
        st.session_state.current_page = 'recommendations'
        st.rerun()

    st.write("---")
    st.subheader(texts['settings'])
    
    # Language Toggle
    new_lang = st.radio(
        texts['language'],
        options=['en', 'ar'],
        format_func=lambda x: 'English' if x == 'en' else 'العربية',
        index=0 if lang == 'en' else 1
    )
    if new_lang != lang:
        st.session_state.language = new_lang
        st.rerun()

# Router
if st.session_state.current_page == 'home':
    home.show()
elif st.session_state.current_page == 'about':
    about.show()
elif st.session_state.current_page == 'student_form':
    student_form.show()
elif st.session_state.current_page == 'recommendations':
    recommendations.show()

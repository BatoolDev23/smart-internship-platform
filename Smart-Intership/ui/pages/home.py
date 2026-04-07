import streamlit as st
from ui.translations import t
from ui.components import header, render_3d_animation

def show():
    header()
    lang = st.session_state.get('language', 'en')
    texts = t[lang]
    
    # Hero Section
    st.markdown(f'<div class="app-header" style="text-align: center;">{texts["app_title"]}</div>', unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.write("")
        st.markdown(f"## {texts['hero_title']}")
        st.markdown(f"<h4 style='color: #666; font-weight: 500;'>{texts['hero_subtitle']}</h4>", unsafe_allow_html=True)
        st.write("---")
        st.write("Built with cutting-edge AI (TF-IDF & Cosine Similarity) and fluent UI principles, we match your core skills, knowledge domains, and experience precisely with professional internship opportunities specifically curated for Al-Balqa Applied University students.")
        
        st.write("")
        if st.button(texts['get_started'], type="primary"):
            st.session_state.current_page = "student_form"
            st.rerun()
            
        st.write("")
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.metric("Corporate Success Rate", "98.2%", "+2.1% this week")
        with subcol2:
            st.metric("Active Internships", "250+", "Updated live")

    with col2:
        render_3d_animation()

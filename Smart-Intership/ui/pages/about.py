import streamlit as st
from ui.translations import t
from ui.components import header

def show():
    header()
    lang = st.session_state.get('language', 'en')
    texts = t[lang]
    
    st.markdown(f'<div class="app-header" style="text-align: center;">{texts.get("about_title", "About SmartSkill")}</div>', unsafe_allow_html=True)
    st.write("")
    
    # Hero Image for About Us
    st.image(
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        caption="Empowering the Next Generation of Professionals",
        use_column_width=True
    )
    st.write("")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Our Mission")
        st.write("At SmartSkill Internships, our goal is to bridge the gap between academic theory and industry practice directly for the talented students of Al-Balqa Applied University and Al-Huson University College.")
        st.write("We provide a powerful, AI-driven networking layer that assesses students' knowledge, core skills, and locational preferences to seamlessly connect them with enterprise internships.")
    
    with col2:
        st.markdown("### The Technology")
        st.write("Our platform leverages advanced Natural Language Processing including Term Frequency-Inverse Document Frequency (TF-IDF) embedding and Cosine Similarity matrices.")
        st.write("This allows the system to read and understand the nuanced differences in technical skill sets, scoring them flawlessly against corporate requirements without human bias or error.")

    st.write("---")
    
    st.markdown("<h3 style='text-align: center;'>Our Corporate Partners</h3>", unsafe_allow_html=True)
    st.write("")
    
    # A gallery of 3 professional corporate images representing partners or industry
    img_col1, img_col2, img_col3 = st.columns(3)
    with img_col1:
        st.image("https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=600&q=80", caption="Financial Tech")
    with img_col2:
        st.image("https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?auto=format&fit=crop&w=600&q=80", caption="Software Engineering")
    with img_col3:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80", caption="Data Science")

    st.write("")
    st.info("System built entirely via local processing for maximum privacy, utilizing Streamlit components, scikit-learn AI models, and SQLite data engines.")

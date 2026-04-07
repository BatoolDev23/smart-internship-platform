import streamlit as st
from ui.translations import t
from ui.components import header, score_badge, get_lat_lon
from database.db_manager import DBManager
from ai.match_scorer import MatchScorer
import time
import pydeck as pdk
import pandas as pd
import random

def show():
    header()
    lang = st.session_state.get('language', 'en')
    texts = t[lang]
    
    if 'student_data' not in st.session_state or not st.session_state.student_data:
        st.warning(texts['no_profile'])
        if st.button("Go to Profile"):
            st.session_state.current_page = "student_form"
            st.rerun()
        return
        
    st.markdown(f"<h2>{texts['recommendations_title']}</h2>", unsafe_allow_html=True)
    
    db = DBManager()
    internships_df = db.get_internships()
    
    scorer = MatchScorer()
    # Loading state to show AI is working
    if 'scores_calculated' not in st.session_state:
        with st.spinner(texts['processing']):
            time.sleep(1) # Fake delay for UX (AI thinking)
            scored_df = scorer.score_applications(st.session_state.student_data, internships_df)
            st.session_state.scored_df = scored_df
            st.session_state.scores_calculated = True
    else:
        scored_df = st.session_state.scored_df
        
    if scored_df.empty:
        st.info("No internships currently available.")
        return
        
    # Split layout for elegant corporate dashboard
    map_col, list_col = st.columns([1, 1.2])
    
    with map_col:
        st.markdown("### Geographic 3D Distribution")
        st.caption("Internship Match Scores visually represented by height & color mapping. Hover to interact.")
        map_data = []
        for _, row in scored_df.iterrows():
            lat, lon = get_lat_lon(row['location'])
            # Add slight jitter so same-city points don't entirely overlap perfectly
            lat += random.uniform(-0.015, 0.015)
            lon += random.uniform(-0.015, 0.015)
            
            # Color mapping: Corporate blue for high match, gray for lower
            color = [0, 120, 212, 180] if row['match_score'] >= 70 else [140, 150, 160, 180]
            
            map_data.append({
                'title': row['title_en'],
                'lat': lat,
                'lon': lon,
                'score': row['match_score'],
                'color': color
            })
            
        map_df = pd.DataFrame(map_data)
        
        # 3D PyDeck without API keys (Streamlit default Carto)
        view_state = pdk.ViewState(latitude=32.25, longitude=35.5, zoom=7, pitch=55)
        
        column_layer = pdk.Layer(
            'ColumnLayer',
            data=map_df,
            get_position='[lon, lat]',
            get_elevation='score',
            elevation_scale=50,
            radius=2500,
            get_fill_color='color',
            pickable=True,
            auto_highlight=True,
        )
        
        st.pydeck_chart(pdk.Deck(
            map_style='light',
            initial_view_state=view_state,
            layers=[column_layer],
            tooltip={"html": "<b>{title}</b><br>Match Score: {score}%"}
        ))
        
    with list_col:
        st.markdown("### Top Opportunities")
        with st.container(height=650): # Scrollable container for the list
            # Display results
            for _, row in scored_df.iterrows():
                # Read fields based on language
                title = row['title_ar'] if lang == 'ar' else row['title_en']
                company = row['company_ar'] if lang == 'ar' else row['company_en']
                desc = row['description_ar'] if lang == 'ar' else row['description_en']
                
                with st.container(border=True):
                    col1, col2 = st.columns([2.5, 1])
                    with col1:
                        st.markdown(f"#### {title}")
                        st.markdown(f"**{company}** | Location: {row['location']} | {texts['remote'] if row['is_remote'] else texts['onsite']}")
                        st.write(desc)
                        
                        # Requirements tags
                        st.caption(f"**{texts['skills']}:** {row['required_skills']}")
                        st.caption(f"**{texts['knowledge_areas']}:** {row['knowledge_areas']}")
                        st.caption(f"**{texts['experience_years']}:** {row['required_experience']} | **Duration:** {row['duration_weeks']} {texts['duration_weeks']}")
                        
                    with col2:
                        # Big score
                        st.markdown(f"<div style='text-align:center; font-size: 2.2rem; font-weight: 900; color: #0078D4;'>{row['match_score']:.0f}%</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center; font-size: 0.8rem; color: #8B95A5; font-weight: 600; text-transform: uppercase;'>{texts['match_score']}</div>", unsafe_allow_html=True)
                        
                        # Small sub-scores
                        st.write("")
                        st.markdown(score_badge(row['skills_score'], texts['skills_match']), unsafe_allow_html=True)
                        st.write("")
                        st.markdown(score_badge(row['knowledge_score'], texts['knowledge_match']), unsafe_allow_html=True)
                        
                        st.write("")
                        app_key = f"apply_{row['id']}"
                        
                        # Check if already applied
                        already_applied = False
                        if 'student_id' in st.session_state:
                            already_applied = db.check_application_exists(st.session_state.student_id, row['id'])
                            
                        if already_applied:
                            st.button(texts['applied'], disabled=True, key=app_key)
                        else:
                            if st.button(texts['apply_now'], type="primary", key=app_key, use_container_width=True):
                                if 'student_id' in st.session_state:
                                    app_data = {
                                        'student_id': st.session_state.student_id,
                                        'internship_id': row['id'],
                                        'match_score': row['match_score'],
                                        'skills_score': row['skills_score'],
                                        'experience_score': row['experience_score'],
                                        'knowledge_score': row['knowledge_score'],
                                        'location_score': row['location_score']
                                    }
                                    db.save_application(app_data)
                                    st.success(texts['success_apply'])
                                    time.sleep(1)
                                    st.rerun()

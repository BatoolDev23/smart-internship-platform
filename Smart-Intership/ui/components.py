import streamlit as st

def apply_rtl_if_arabic():
    """Apply RTL CSS if current language is Arabic"""
    if st.session_state.get('language') == 'ar':
        st.markdown('<style> .stApp { direction: rtl; text-align: right; font-family: "Cairo", sans-serif; } </style>', unsafe_allow_html=True)
        # Also fix metric directions
        st.markdown('<style> [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { direction: rtl; text-align: right; } </style>', unsafe_allow_html=True)

def load_css():
    """Load custom CSS styles"""
    try:
        with open('assets/style.css', 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Handle if css not available yet

def header():
    """Common header for pages"""
    load_css()
    apply_rtl_if_arabic()

def score_badge(score, label=""):
    """Returns HTML for a colored score badge"""
    if score >= 80:
        c = "score-high"
    elif score >= 50:
        c = "score-medium"
    else:
        c = "score-low"
    
    formatted_score = f"{score:.0f}%"
    return f'<span class="score-badge {c}">{label} {formatted_score}</span>'

def get_lat_lon(location):
    """Simple lat/lon lookup for internships based in Jordan"""
    loc = location.lower() if location else ""
    if 'amman' in loc or 'عمان' in loc:
        return 31.9522, 35.2332
    elif 'irbid' in loc or 'اربد' in loc:
        return 32.5514, 35.8515
    elif 'aqaba' in loc or 'عقبة' in loc:
        return 29.5267, 35.0078
    return 31.9522, 35.2332 # Default to Amman

def render_3d_animation():
    """Render a beautiful interactive 3D Spline animation component without APIs"""
    st.components.v1.html('''
    <div style="width: 100%; height: 450px; overflow: hidden; border-radius: 12px; background: transparent;">
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.0.51/build/spline-viewer.js"></script>
        <spline-viewer url="https://prod.spline.design/E0V38c10Sbd2mO4H/scene.splinecode" style="width: 100%; height: 100%;"></spline-viewer>
    </div>
    ''', height=460)

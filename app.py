import streamlit as st

# Page config
st.set_page_config(
    page_title="THE BEAR PATROL",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #EFF9E8 30%, #EFF9E8 100%);
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #658C6E 0%, #85A898 100%);
        border-radius: 1rem;
        margin-bottom: 2rem;
        border: 1px solid #DFCD80;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #658C6E 0%, #85A898 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #DFCD80;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #658C6E;
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(255, 184, 0, 0.3)
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .team-member {
        text-align: center;
        padding: 1rem;
        background: #DFCD80;
        border-radius: 0.5rem;
        border: 1px solid #F5E2B0;
    }
    
    h1, h2, h3 {
        color: #444f3f !important;
    }
    
    .bear-badge {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
            
    .stButton > button {
        background-color: #677345;
        color: #ffffff;
        border: none;
        border-radius: 0.25rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Button hover effect */
    .stButton > button:hover {
        background-color: #BFC997;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 184, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="hero-section">
        <div class="bear-badge">🐻</div>
        <h1 style="color: #ffb800; margin-bottom: 0;">THE BEAR PATROL</h1>
        <p style="color: #ffffff; font-size: 1.1rem;">S&P 500 Bear Market Early Warning System</p>
        <p style="color: #000000; font-size: 0.85rem; letter-spacing: 2px; margin-top: 1rem;">
            SHANI • ESTHER • MATTHEW • DESMOND
        </p>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown("## 🚀 Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Real-time Risk Scoring</h3>
        <p style="color: #ffffff;">AI-powered risk detection with 85%+ accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3>Social Sentiment Analysis</h3>
        <p style="color: #ffffff;">NLP-driven market sentiment from social media</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>Ensemble ML Models</h3>
        <p style="color: #ffffff;">Multiple models combined for robust predictions</p>
    </div>
    """, unsafe_allow_html=True)

# Navigation Buttons
st.markdown("---")
st.markdown("## 📊 Get Started")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("📈 View Public Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

with col2:
    if st.button("🔐 Admin Login", use_container_width=True):
        st.switch_page("pages/Admin_Login.py")

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem;">
        <span style="color: #677345; font-size: 0.8rem;">🔒 Admin-only analytics</span>
    </div>
    """, unsafe_allow_html=True)

# Team Section
st.markdown("---")
st.markdown("## 👥 The Bear Patrol Team")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👩‍💻</div>
        <h4>Shani</h4>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👩‍💼</div>
        <h4>Esther</h4>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👨‍🔧</div>
        <h4>Matthew</h4>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👨‍💻</div>
        <h4>Desmond</h4>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #787b86; font-size: 0.7rem; padding: 2rem;">
    🐻 THE BEAR PATROL | Protecting retail investors from market downturns<br>
    Powered by AI • Real-time Analytics • Institutional-grade Accuracy
</div>
""", unsafe_allow_html=True)
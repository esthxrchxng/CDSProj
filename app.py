import streamlit as st

# Page config
st.set_page_config(
    page_title="THE BEAR PATROL",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - DARK THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0e1117 !important;
    }

    .stApp, .stApp p, .stApp li, .stApp span {
        color: #e2e8f0;
    }

    .hero-section {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 1rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(252, 129, 129, 0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }

    .feature-card {
        background: rgba(22, 28, 45, 0.95);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.07);
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .feature-card:hover {
        border-color: rgba(96, 165, 250, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .team-member {
        text-align: center;
        padding: 1rem;
        background: rgba(22, 28, 45, 0.95);
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.07);
        transition: all 0.2s ease;
    }

    .team-member:hover {
        border-color: rgba(96, 165, 250, 0.3);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }

    h1, h2, h3, h4 {
        color: #e2e8f0 !important;
    }

    .bear-badge {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #334155 0%, #475569 100%);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }

    [data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="hero-section">
        <div class="bear-badge">🐻</div>
        <h1 style="background: linear-gradient(135deg, #e2e8f0 0%, #fc8181 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text; font-size: 2.5rem; font-weight: 700; margin-bottom: 0;">
            THE BEAR PATROL
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem;">S&P 500 Bear Market Early Warning System</p>
        <p style="color: #64748b; font-size: 0.85rem; letter-spacing: 2px; margin-top: 1rem;">
            SHANI &bull; ESTHER &bull; MATTHEW &bull; DESMOND
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
        <h3 style="color: #e2e8f0;">Real-time Risk Scoring</h3>
        <p style="color: #94a3b8;">AI-powered risk detection with 85%+ accuracy</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3 style="color: #e2e8f0;">Social Sentiment Analysis</h3>
        <p style="color: #94a3b8;">NLP-driven market sentiment from social media</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3 style="color: #e2e8f0;">Ensemble ML Models</h3>
        <p style="color: #94a3b8;">Multiple models combined for robust predictions</p>
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
        <span style="color: #64748b; font-size: 0.8rem;">🔒 Admin-only analytics</span>
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
        <h4 style="color: #e2e8f0;">Shani</h4>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👩‍💼</div>
        <h4 style="color: #e2e8f0;">Esther</h4>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👨‍🔧</div>
        <h4 style="color: #e2e8f0;">Matthew</h4>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="team-member">
        <div style="font-size: 2rem;">👨‍💻</div>
        <h4 style="color: #e2e8f0;">Desmond</h4>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #475569; font-size: 0.7rem; padding: 2rem;">
    🐻 THE BEAR PATROL | Protecting retail investors from market downturns<br>
    Powered by AI &bull; Real-time Analytics &bull; Institutional-grade Accuracy
</div>
""", unsafe_allow_html=True)

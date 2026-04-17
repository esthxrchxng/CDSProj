import streamlit as st

# Page config
st.set_page_config(
    page_title="Admin Login - THE BEAR PATROL",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - DARK THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0e1117 !important;
    }

    .stApp, .stApp p, .stApp label, .stApp span {
        color: #e2e8f0;
    }

    .login-container {
        max-width: 420px;
        margin: 2rem auto;
        padding: 2.5rem;
        background: rgba(22, 28, 45, 0.97);
        backdrop-filter: blur(10px);
        border-radius: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        text-align: center;
    }

    .login-header {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .warning-text {
        color: #fc8181;
        font-size: 0.8rem;
        margin-top: 1rem;
    }

    h1 {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0 0%, #fc8181 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    h3 {
        color: #e2e8f0;
        font-weight: 600;
    }

    p {
        color: #94a3b8;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 0.75rem;
        padding: 0.75rem 1rem;
        color: #e2e8f0 !important;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #fc8181 !important;
        box-shadow: 0 0 0 3px rgba(252, 129, 129, 0.15) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #475569;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }

    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
    }

    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    .divider span {
        padding: 0 1rem;
        color: #475569;
        font-size: 0.8rem;
    }

    [data-testid="stAlert"] {
        background: rgba(22, 28, 45, 0.95) !important;
        color: #e2e8f0 !important;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "bearpatrol2026"

# Login form
st.markdown("""
<div class="login-container">
    <div class="login-header">🐻</div>
    <h1>THE BEAR PATROL</h1>
    <h3>Admin Access</h3>
    <p style="margin-bottom: 2rem;">Enter your credentials to access the analytics dashboard</p>
</div>
""", unsafe_allow_html=True)

with st.form("login_form"):
    username = st.text_input("Username", placeholder="admin", label_visibility="collapsed")
    password = st.text_input("Password", type="password", placeholder="••••••••", label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("🔓 Sign In", use_container_width=True)
    with col2:
        if st.form_submit_button("🏠 Back to Home", use_container_width=True):
            st.switch_page("app.py")

    if submitted:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Login successful! Redirecting...")
            st.switch_page("pages/Admin_Dashboard.py")
        else:
            st.error("❌ Invalid credentials. Access denied.")
            st.markdown("""
            <div class="warning-text">
                ⚠️ Unauthorized access attempt detected. This incident has been logged.
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #475569; font-size: 0.7rem; margin-top: 2rem;">
    🔒 Restricted area | Authorized personnel only
</div>
""", unsafe_allow_html=True)

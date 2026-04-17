import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import pytz

# Page config
st.set_page_config(
    page_title="Admin Analytics - THE BEAR PATROL",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.error("🔒 Unauthorized access. Please login first.")
    st.stop()

# Custom CSS - DARK THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0e1117 !important;
    }

    .stApp, .stApp p, .stApp li, .stApp span, .stApp label {
        color: #e2e8f0;
    }

    .admin-badge {
        background: linear-gradient(135deg, #fc8181 0%, #e53e3e 100%);
        color: white;
        padding: 0.35rem 1rem;
        border-radius: 2rem;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
        letter-spacing: 0.5px;
    }

    .metric-card {
        background: rgba(22, 28, 45, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 0.5rem;
        color: #e2e8f0;
        transition: all 0.2s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .insight-box {
        background: rgba(22, 28, 45, 0.95);
        border-left: 4px solid #f6e05e;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        color: #e2e8f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    /* Headers */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0 0%, #fc8181 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
    }
    h2, h3, h4 {
        color: #e2e8f0;
        font-weight: 600;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(22, 28, 45, 0.95) !important;
        color: #e2e8f0 !important;
        border-radius: 0.5rem;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }

    /* Streamlit metrics */
    [data-testid="stMetricValue"] {
        color: #e2e8f0 !important;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }

    [data-testid="stAlert"] {
        background: rgba(22, 28, 45, 0.95) !important;
        color: #e2e8f0 !important;
        border-radius: 0.5rem;
    }

    /* Download button */
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv('jan_apr_2026_predictions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def create_risk_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Predicted_Risk_Score'],
        mode='lines',
        name='Risk Score',
        line=dict(color='#fc8181', width=3),
        fill='tozeroy',
        fillcolor='rgba(252, 129, 129, 0.1)'
    ))

    warning_df = df[df['Crash_Warning_Flag'] == 1]
    fig.add_trace(go.Scatter(
        x=warning_df['Date'],
        y=warning_df['Predicted_Risk_Score'],
        mode='markers',
        name='⚠️ Alert',
        marker=dict(color='#f6e05e', size=12, symbol='triangle-up',
                    line=dict(width=1, color='#0e1117'))
    ))

    fig.update_layout(
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', gridwidth=1,
                   title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8')),
        yaxis=dict(title="Risk Score", range=[0, 1], tickformat='.0%',
                   showgrid=True, gridcolor='rgba(255,255,255,0.06)', gridwidth=1,
                   title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color='#e2e8f0'), bgcolor='rgba(14,17,23,0.8)',
                    bordercolor='rgba(255,255,255,0.1)', borderwidth=1),
        hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
    )

    return fig


def create_sentiment_chart(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['weighted_sentiment'],
            name='Sentiment',
            line=dict(color='#60a5fa', width=2.5),
            fill='tozeroy',
            fillcolor='rgba(96, 165, 250, 0.1)'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Bar(
            x=df['Date'],
            y=df['momentum'],
            name='Momentum',
            marker_color='#f6e05e',
            opacity=0.6,
            marker_line_width=0
        ),
        secondary_y=True
    )

    fig.update_layout(
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color='#e2e8f0'), bgcolor='rgba(14,17,23,0.8)',
                    bordercolor='rgba(255,255,255,0.1)', borderwidth=1),
        hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
    )
    fig.update_yaxes(title_text="Sentiment", secondary_y=False,
                     showgrid=True, gridcolor='rgba(255,255,255,0.06)',
                     title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'))
    fig.update_yaxes(title_text="Momentum", secondary_y=True,
                     showgrid=False,
                     title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'))

    return fig


def create_volume_chart(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df['Date'],
            y=df['total_mentions'],
            name='Mentions',
            marker_color='#94a3b8',
            opacity=0.7,
            marker_line_width=0
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date'],
            y=df['Financial_Panic_Interaction'],
            name='Panic Index',
            line=dict(color='#fc8181', width=2.5),
            mode='lines+markers',
            marker=dict(size=5, color='#fc8181')
        ),
        secondary_y=True
    )

    fig.update_layout(
        height=400,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color='#e2e8f0'), bgcolor='rgba(14,17,23,0.8)',
                    bordercolor='rgba(255,255,255,0.1)', borderwidth=1),
        hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
    )
    fig.update_yaxes(title_text="Mentions", secondary_y=False,
                     showgrid=True, gridcolor='rgba(255,255,255,0.06)',
                     title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'))
    fig.update_yaxes(title_text="Panic Index", secondary_y=True,
                     showgrid=False,
                     title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'))

    return fig


def main():
    # Header with admin badge
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">🐻</div>
            <h1>THE BEAR PATROL</h1>
            <p style="color: #94a3b8;">Admin Analytics Dashboard</p>
            <span class="admin-badge">🔐 ADMIN ACCESS</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem;">👋</div>
            <div style="font-weight: 600; color: #e2e8f0;">Welcome, Admin</div>
            <div style="font-size: 0.7rem; color: #64748b;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.switch_page("app.py")

        st.markdown("---")

        uploaded_file = st.file_uploader("📁 Upload predictions CSV", type=['csv'])

        st.markdown("---")
        date_range = st.selectbox("📅 Time Frame", ["Last 30 Days", "Last 60 Days", "All Data"])

        st.markdown("---")
        show_models = st.multiselect(
            "🤖 Show Model Probabilities",
            ["RF", "SVM", "Voting", "TabNet"],
            default=["RF", "Voting", "SVM", "TabNet"]
        )

    # Load data
    df = load_data(uploaded_file)

    if date_range == "Last 30 Days":
        df_filtered = df.tail(30)
    elif date_range == "Last 60 Days":
        df_filtered = df.tail(60)
    else:
        df_filtered = df

    latest = df_filtered.iloc[-1]

    st.markdown("### 📉 Risk Analysis")
    fig_risk = create_risk_chart(df_filtered)
    st.plotly_chart(fig_risk, use_container_width=True)

    # Sentiment & Momentum
    st.markdown("## 💭 Sentiment & Momentum Analysis")
    fig_sentiment = create_sentiment_chart(df_filtered)
    st.plotly_chart(fig_sentiment, use_container_width=True)

    with st.expander("📊 Sentiment Insights & Analytics", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Sentiment", f"{latest['weighted_sentiment']:.3f}")
        with col2:
            st.metric("30d Avg Sentiment", f"{df_filtered['weighted_sentiment'].tail(30).mean():.3f}")
        with col3:
            st.metric("Sentiment Volatility", f"{df_filtered['weighted_sentiment'].tail(30).std():.3f}")
        with col4:
            st.metric("Current Momentum", f"{latest['momentum']:.3f}")

        st.markdown("""
        <div class="insight-box">
            <strong style="color: #f6e05e;">📈 AI Insight:</strong><br>
            Sentiment analysis shows {} trend over the past 30 days.
            Momentum indicators suggest {} market conditions.
        </div>
        """.format(
            "bullish" if df_filtered['weighted_sentiment'].tail(30).mean() > 0 else "bearish",
            "positive" if latest['momentum'] > 0 else "negative"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Social Activity
    st.markdown("## 📰 Social Media Activity")
    fig_volume = create_volume_chart(df_filtered)
    st.plotly_chart(fig_volume, use_container_width=True)

    with st.expander("📊 Social Media Analytics", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Mentions (30d)", f"{df_filtered['total_mentions'].tail(30).sum():.0f}")
        with col2:
            st.metric("Peak Panic Score", f"{df_filtered['Financial_Panic_Interaction'].max():.3f}")
        with col3:
            st.metric("Avg Daily Mentions", f"{df_filtered['total_mentions'].tail(30).mean():.1f}")

        correlation = df_filtered[['Predicted_Risk_Score', 'Financial_Panic_Interaction']].corr().iloc[0, 1]
        st.markdown(f"""
        <div class="insight-box">
            <strong style="color: #f6e05e;">📊 Correlation Analysis:</strong><br>
            Panic-Risk Correlation: {correlation:.3f}<br>
            {'⚠️ Strong correlation detected — social panic strongly predicts market risk' if abs(correlation) > 0.7 else '📈 Moderate correlation between social panic and market risk'}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Ensemble Model Confidence
    if show_models:
        st.markdown("## 🤖 Ensemble Model Confidence")

        model_data = []
        model_names = []

        if "RF" in show_models:
            model_data.append(df_filtered['Base_RF_Prob'].iloc[-1])
            model_names.append("Random Forest")
        if "SVM" in show_models:
            model_data.append(df_filtered['Base_SVM_Prob'].iloc[-1])
            model_names.append("SVM")
        if "Voting" in show_models:
            model_data.append(df_filtered['Base_Voting_Prob'].iloc[-1])
            model_names.append("Voting Ensemble")
        if "TabNet" in show_models:
            model_data.append(df_filtered['Base_TabNet_Prob'].iloc[-1])
            model_names.append("TabNet")

        bar_colors = ['#60a5fa', '#68d391', '#f6e05e', '#fc8181']
        fig_models = go.Figure(data=[
            go.Bar(
                x=model_names,
                y=model_data,
                marker_color=bar_colors[:len(model_data)],
                text=[f"{x:.1%}" for x in model_data],
                textposition='outside',
                textfont={'color': '#e2e8f0', 'size': 13},
                width=0.5
            )
        ])

        fig_models.update_layout(
            height=450,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Probability of Downturn",
            yaxis_range=[0, 1.1],
            yaxis_tickformat='.0%',
            margin=dict(l=40, r=40, t=40, b=40),
            showlegend=False,
            font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
            yaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'),
                       gridcolor='rgba(255,255,255,0.06)'),
            xaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8')),
            hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
        )

        st.plotly_chart(fig_models, use_container_width=True)

        with st.expander("📊 Model Performance Metrics", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ensemble Risk Score", f"{latest['Predicted_Risk_Score']:.1%}")
                st.metric("Model Consensus", f"{np.mean(model_data):.1%}")
                st.metric("Model Std Dev", f"{np.std(model_data):.3f}")
            with col2:
                st.metric("Highest Confidence", f"{max(model_data):.1%}")
                st.metric("Lowest Confidence", f"{min(model_data):.1%}")
                st.metric("Model Spread", f"{(max(model_data) - min(model_data)):.1%}")

        st.markdown("""
        <div class="insight-box">
            <strong style="color: #f6e05e;">🎯 Ensemble Decision:</strong><br>
            {} out of {} models predict increased risk.
            Recommended action: {}.
        </div>
        """.format(
            sum(1 for x in model_data if x > 0.5),
            len(model_data),
            "🚨 ACTIVATE BEAR PATROL" if latest['Crash_Warning_Flag'] == 1 else "✅ Monitor normally"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Advanced Analytics
    st.markdown("## 📊 Advanced Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Risk Score Distribution")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df_filtered['Predicted_Risk_Score'],
            nbinsx=20,
            marker_color='#60a5fa',
            opacity=0.8,
            marker_line_color='rgba(255,255,255,0.2)',
            marker_line_width=1
        ))
        fig_hist.update_layout(
            height=350,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Risk Score",
            yaxis_title="Frequency",
            font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
            xaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'),
                       tickformat='.0%', gridcolor='rgba(255,255,255,0.06)'),
            yaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'),
                       gridcolor='rgba(255,255,255,0.06)'),
            hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        st.markdown("### Warnings by Day of Week")
        warning_by_date = df_filtered.groupby(df_filtered['Date'].dt.dayofweek)['Crash_Warning_Flag'].sum()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        fig_bar = go.Figure(data=[
            go.Bar(
                x=days[:len(warning_by_date)],
                y=warning_by_date.values,
                marker_color='#fc8181',
                text=warning_by_date.values,
                textposition='outside',
                textfont={'color': '#e2e8f0', 'size': 13}
            )
        ])
        fig_bar.update_layout(
            height=350,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Day of Week",
            yaxis_title="Number of Warnings",
            font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
            xaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8')),
            yaxis=dict(title_font=dict(color='#94a3b8'), tickfont=dict(color='#94a3b8'),
                       gridcolor='rgba(255,255,255,0.06)'),
            hoverlabel=dict(bgcolor='#1e293b', font_color='#e2e8f0', font_size=12)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Export section
    st.markdown("---")
    st.markdown("## 📥 Export Data")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📊 Export Full Analytics (CSV)",
            data=csv,
            file_name=f"bear_patrol_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 0.7rem; padding: 1rem;">
        🐻 THE BEAR PATROL | Admin Analytics Dashboard | Shani &bull; Esther &bull; Matthew &bull; Desmond<br>
        🔐 Authorized access only | All actions are logged
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

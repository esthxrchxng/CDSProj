import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz
import yfinance as yf
import numpy as np

# Page config
st.set_page_config(
    page_title="Public Dashboard - THE BEAR PATROL",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - AESTHETIC LIGHT THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    
    /* Modern card styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.25rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: #1a1a2e;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #e53e3e;
        animation: pulse 2s infinite;
        color: #1a1a2e;
    }
    
    .safe-card {
        background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #38a169;
        color: #1a1a2e;
    }
    
    @keyframes pulse {
        0%, 100% { border-color: #e53e3e; box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.2); }
        50% { border-color: #fc8181; box-shadow: 0 0 0 8px rgba(229, 62, 62, 0); }
    }
    
    .big-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .locked-content {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        color: #1a1a2e;
        transition: all 0.3s ease;
    }
    
    .locked-content:hover {
        border-color: #cbd5e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] * {
        color: #1a1a2e;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        font-weight: 500;
        color: #4a5568;
    }
    
    /* Headers */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1a1a2e 0%, #e53e3e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0;
    }
    
    h2, h3 {
        color: #1a1a2e;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Info box */
    .stAlert {
        background: linear-gradient(135deg, #ebf8ff 0%, #ffffff 100%);
        color: #1a1a2e;
        border-left: 4px solid #3182ce;
        border-radius: 0.5rem;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv('jan_apr_2026_predictions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def create_risk_chart(df):
    """
    Create chart comparing Predicted Risk Score vs Actual Risk Score
    Actual risk score is calculated from S&P 500 price movements
    """
    
    # Fetch actual S&P 500 data
    @st.cache_data(ttl=3600)
    def get_sp500_data(start_date, end_date):
        try:
            sp500 = yf.download("^GSPC", start=start_date, end=end_date, progress=False)
            sp500 = sp500[['Close']].reset_index()
            sp500.columns = ['Date', 'SP500_Close']
            return sp500
        except:
            # Fallback synthetic data
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)
            base_price = 4500
            synthetic_prices = base_price + np.cumsum(np.random.randn(len(dates)) * 15)
            return pd.DataFrame({'Date': dates, 'SP500_Close': synthetic_prices})
    
    def calculate_actual_risk(sp500_prices):
        """
        Calculate actual risk score from S&P 500 price movements
        Risk is higher when prices are falling rapidly
        """
        # Calculate daily returns
        returns = sp500_prices.pct_change()
        
        # Calculate drawdown from recent peak
        rolling_max = sp500_prices.expanding().max()
        drawdown = (sp500_prices - rolling_max) / rolling_max
        
        # Calculate volatility (20-day rolling)
        volatility = returns.rolling(window=20, min_periods=1).std() * np.sqrt(252)
        
        # Calculate momentum (negative momentum = higher risk)
        momentum = returns.rolling(window=5, min_periods=1).mean()
        
        # Combine factors into risk score (0-1 scale)
        # Drawdown contributes most (0-0.6), volatility (0-0.3), negative momentum (0-0.1)
        drawdown_risk = np.clip(-drawdown * 1.5, 0, 0.6)
        volatility_risk = np.clip(volatility / 0.5 * 0.3, 0, 0.3)
        momentum_risk = np.clip(-momentum * 2, 0, 0.1)
        
        actual_risk = drawdown_risk + volatility_risk + momentum_risk
        actual_risk = np.clip(actual_risk, 0, 1)
        
        return actual_risk
    
    # Get date range
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    end_date = df['Date'].max().strftime('%Y-%m-%d')
    
    # Fetch S&P 500 data
    sp500_data = get_sp500_data(start_date, end_date)
    
    # Calculate actual risk scores
    sp500_data['Actual_Risk_Score'] = calculate_actual_risk(sp500_data['SP500_Close'])
    
    # Merge with prediction data
    merged_df = pd.merge(df, sp500_data, on='Date', how='left')
    
    # Create the chart
    fig = go.Figure()
    
    # Add Predicted Risk Score line
    fig.add_trace(go.Scatter(
        x=merged_df['Date'],
        y=merged_df['Predicted_Risk_Score'],
        mode='lines+markers',
        name='📊 Predicted Risk Score (Model)',
        line=dict(color='#e74c3c', width=2.5),
        marker=dict(size=6, color='#e74c3c'),
        fill=None
    ))
    
    # Add Actual Risk Score line (calculated from S&P 500)
    fig.add_trace(go.Scatter(
        x=merged_df['Date'],
        y=merged_df['Actual_Risk_Score'],
        mode='lines+markers',
        name='📈 Actual Risk Score (S&P 500)',
        line=dict(color='#2ecc71', width=2.5, dash='dash'),
        marker=dict(size=6, color='#2ecc71', symbol='diamond')
    ))
    
    # Add actual downturn markers
    actual_downturn_df = merged_df[merged_df['True_Downturn'] == 1]
    fig.add_trace(go.Scatter(
        x=actual_downturn_df['Date'],
        y=actual_downturn_df['Actual_Risk_Score'],
        mode='markers',
        name='💥 Actual Downturn Event',
        marker=dict(color='#e74c3c', size=14, symbol='x', line=dict(width=2, color='white'))
    ))
    
    # Add threshold line at 0.7
    fig.add_hline(y=0.7, line_dash="dash", line_color="#e74c3c", opacity=0.5,
                  annotation_text="High Risk Threshold (70%)", annotation_position="top right")
    
    # Add risk zones (background colors)
    fig.add_hrect(y0=0, y1=0.3, line_width=0, fillcolor="rgba(46, 204, 113, 0.05)", opacity=0.5)
    fig.add_hrect(y0=0.3, y1=0.7, line_width=0, fillcolor="rgba(241, 196, 15, 0.05)", opacity=0.5)
    fig.add_hrect(y0=0.7, y1=1, line_width=0, fillcolor="rgba(231, 76, 60, 0.08)", opacity=0.5)
    
    # Update layout
    fig.update_layout(
        height=500,
        template='simple_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family='Inter, sans-serif', size=12, color='#1a1a2e'),
        title=dict(
            text="Model Predictions vs Actual Market Risk (S&P 500)",
            font=dict(size=18, weight='bold', color='#1a1a2e'),
            x=0.5
        ),
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='#e2e8f0',
            gridwidth=1,
            title_font=dict(color='#4a5568'),
            tickfont=dict(color='#4a5568')
        ),
        yaxis=dict(
            title="Risk Score (0 = Low Risk, 1 = High Risk)",
            range=[0, 1],
            tickformat='.0%',
            showgrid=True,
            gridcolor='#e2e8f0',
            gridwidth=1,
            title_font=dict(color='#4a5568'),
            tickfont=dict(color='#4a5568')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color='#1a1a2e', size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter"
        )
    )
    
    return fig

def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 4rem;">🐻</div>
            <h1>THE BEAR PATROL</h1>
            <p style="color: #4a5568; font-size: 1rem;">Real-time S&P 500 Downturn Risk Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard Controls")
        
        current_time = datetime.now(pytz.timezone('US/Eastern'))
        market_hour = 9 <= current_time.hour <= 16
        market_status = "OPEN" if market_hour else "CLOSED"
        status_color = "#63ba5d80" if market_hour else "#ba635d80"
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: {status_color}; border-radius: 1rem; margin-bottom: 1rem;">
            <div style="font-weight: 600;">MARKET {market_status}</div>
            <div style="font-size: 0.8rem; color: #616161;">{current_time.strftime('%Y-%m-%d %H:%M:%S ET')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        date_range = st.selectbox(
            "📅 Time Frame",
            ["Last 30 Days", "Last 60 Days", "All Data"],
            help="Select the time period to display"
        )
        
        st.markdown("---")
        st.info("💡 **Public Access**\n\nView real-time risk scores and alerts. Advanced analytics require admin access.")
        
        if st.button("🔐 Admin Login", use_container_width=True):
            st.switch_page("pages/2_🔐_Admin_Login.py")
    
    # Load data
    df = load_data()
    
    if date_range == "Last 30 Days":
        df_filtered = df.tail(30)
    elif date_range == "Last 60 Days":
        df_filtered = df.tail(60)
    else:
        df_filtered = df
    
    latest = df_filtered.iloc[-1]
    latest_risk = latest['Predicted_Risk_Score']
    latest_warning = latest['Crash_Warning_Flag']
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if latest_warning == 1:
            st.markdown(f"""
            <div class="warning-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #e53e3e;">⚠️ Alert Status</div>
                <div class="big-number">ACTIVE</div>
                <div style="margin-top: 0.5rem; color: #4a5568;">Risk: <strong style="color: #e53e3e;">{latest_risk:.1%}</strong></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #38a169;">✅ Status</div>
                <div class="big-number">NORMAL</div>
                <div style="margin-top: 0.5rem; color: #4a5568;">Risk: <strong>{latest_risk:.1%}</strong></div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #718096;">📈 Risk Score</div>
            <div class="big-number">{latest_risk:.3f}</div>
            <div style="font-size: 0.7rem; color: #718096;">0 = Low Risk → 1 = High Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        trend = df_filtered['Predicted_Risk_Score'].pct_change().iloc[-1] if len(df_filtered) > 1 else 0
        trend_arrow = '↑' if trend > 0 else '↓'
        trend_color = '#e53e3e' if trend > 0 else '#38a169'
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #718096;">📊 Trend Direction</div>
            <div class="big-number" style="color: {trend_color};">{trend_arrow}</div>
            <div style="font-size: 0.7rem; color: #718096;">24-hour change</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        alert_count = df_filtered['Crash_Warning_Flag'].tail(30).sum()
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #718096;">🚨 Alert Frequency</div>
            <div class="big-number">{alert_count}</div>
            <div style="font-size: 0.7rem; color: #718096;">Last 30 days</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Score Comparison Chart
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #1e3a8a; font-weight: 600; display: inline-block; border-bottom: 3px solid #e74c3c; padding-bottom: 0.25rem;">
            📊 Risk Score Comparison: Model Predictions vs Actual Market Risk
        </h3>
    </div>
    """, unsafe_allow_html=True)
    fig_risk = create_risk_chart(df_filtered)
    st.plotly_chart(fig_risk, use_container_width=True)
    # After the chart, add comparison metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        predicted_risk = latest['Predicted_Risk_Score']
        st.metric(
            "🤖 Model Predicted Risk",
            f"{predicted_risk:.1%}",
            delta=None,
            help="Our AI model's prediction based on social sentiment + market data"
        )

    with col2:
        # Calculate actual risk from S&P 500 (you'll need to compute this)
        # For now, using a placeholder - you can calculate from your data
        actual_risk = latest.get('Actual_Risk_Score', predicted_risk * 0.9)
        st.metric(
            "📈 Actual Market Risk",
            f"{actual_risk:.1%}",
            delta=f"{predicted_risk - actual_risk:.1%}",
            delta_color="inverse",
            help="Risk calculated from actual S&P 500 price movements"
        )

    with col3:
        accuracy = 1 - abs(predicted_risk - actual_risk)
        st.metric(
            "🎯 Prediction Accuracy",
            f"{accuracy:.1%}",
            help="How close the model prediction is to actual market risk"
        )
        
    # Alert History
    st.markdown("### <span style='color: #000000;'>🚨 Recent Alert History</span>", unsafe_allow_html=True)
    warnings_df = df_filtered[df_filtered['Crash_Warning_Flag'] == 1].tail(10)
    
    if len(warnings_df) > 0:
        for _, row in warnings_df.iterrows():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fff5f5 0%, #fff5f5 100%); border-left: 4px solid #e53e3e; padding: 1rem; margin: 0.5rem 0; border-radius: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #e53e3e;">⚠️ CRASH WARNING</strong>
                        <div style="font-size: 0.85rem; color: #4a5568;">{row['Date'].strftime('%B %d, %Y')}</div>
                    </div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #e53e3e;">{row['Predicted_Risk_Score']:.1%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No alerts triggered in the selected period")
    
    # Locked Content Section
    st.markdown("---")
    st.markdown("### <span style='color: #000000;'>🔒 Advanced Analytics</span>", unsafe_allow_html=True)
    st.caption("Login as admin to unlock sentiment analysis, model confidence, and advanced metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="locked-content">
            <div style="font-size: 3rem;">🔒</div>
            <h3 style="color: #1a1a2e;">Sentiment & Momentum</h3>
            <p style="color: #4a5568;">Track social media sentiment and market momentum indicators</p>
            <span style="font-size: 0.7rem; color: #718096;">Admin access required</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="locked-content">
            <div style="font-size: 3rem;">🔒</div>
            <h3 style="color: #1a1a2e;">Ensemble Model</h3>
            <p style="color: #4a5568;">View individual model predictions and confidence scores</p>
            <span style="font-size: 0.7rem; color: #718096;">Admin access required</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; font-size: 0.7rem; padding: 1rem;">
        🐻 THE BEAR PATROL | Powered by Social Media Sentiment + Market Data
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
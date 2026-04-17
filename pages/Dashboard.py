import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(
    page_title="Public Dashboard - THE BEAR PATROL",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - DARK THEME
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* ── App background ── */
    .stApp {
        background: #0e1117 !important;
    }
    [data-testid="stAppViewContainer"] {
        background: #0e1117 !important;
    }
    [data-testid="stHeader"] {
        background: #0e1117 !important;
    }

    /* ── Default text ── */
    .stApp, .stApp p, .stApp li, .stApp span, .stApp label {
        color: #e2e8f0;
    }

    /* ── Selectbox / input widgets ── */
    [data-testid="stSelectbox"] > div > div {
        background: #1e293b !important;
        border-color: rgba(255,255,255,0.1) !important;
        color: #e2e8f0 !important;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: rgba(22, 28, 45, 0.95);
        backdrop-filter: blur(10px);
        padding: 1.25rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.07);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: #e2e8f0;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    }

    .warning-card {
        background: linear-gradient(135deg, #2d1515 0%, #1a1a2e 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #fc8181;
        animation: pulse 2s infinite;
        color: #e2e8f0;
    }

    .safe-card {
        background: linear-gradient(135deg, #0d2418 0%, #1a1a2e 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #68d391;
        color: #e2e8f0;
    }

    .pending-card {
        background: linear-gradient(135deg, #2d2410 0%, #1a1a2e 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #f6e05e;
        color: #e2e8f0;
    }

    .correct-card {
        background: linear-gradient(135deg, #0d2418 0%, #1a1a2e 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #68d391;
        color: #e2e8f0;
    }

    .incorrect-card {
        background: linear-gradient(135deg, #2d1515 0%, #1a1a2e 100%);
        padding: 1.25rem;
        border-radius: 1rem;
        border: 2px solid #fc8181;
        color: #e2e8f0;
    }

    @keyframes pulse {
        0%, 100% { border-color: #fc8181; box-shadow: 0 0 0 0 rgba(252,129,129,0.2); }
        50%       { border-color: #feb2b2; box-shadow: 0 0 0 8px rgba(252,129,129,0); }
    }

    .big-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #e2e8f0;
        -webkit-text-fill-color: #e2e8f0;
    }

    .locked-content {
        background: rgba(22, 28, 45, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    .locked-content:hover {
        border-color: rgba(255,255,255,0.15);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #111827 !important;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* ── Headers ── */
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

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        border-color: rgba(255,255,255,0.2);
    }

    /* ── Divider ── */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    }

    /* ── Streamlit default alert boxes ── */
    [data-testid="stAlert"] {
        background: rgba(22, 28, 45, 0.95) !important;
        color: #e2e8f0 !important;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_spx_data():
    """Load Bloomberg SPX data. Rows 0-5 are metadata; row 6 is the header."""
    df = pd.read_excel(
        'Raw Data/Financial Data/SPX Last Open val.xlsx',
        header=6
    )
    df = df[['Date', 'PX_LAST']].rename(columns={'PX_LAST': 'Close'})
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.dropna(subset=['Date', 'Close']).sort_values('Date').reset_index(drop=True)
    return df


@st.cache_data
def load_predictions():
    df = pd.read_csv('jan_apr_2026_predictions.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def compute_cutoff(pred_df, spx_df):
    """Return the last prediction date that has ≥30 trading days of SPX data after it."""
    cutoff = None
    for date in sorted(pred_df['Date']):
        future_days = int((spx_df['Date'] > date).sum())
        if future_days >= 30:
            cutoff = date
    return cutoff


def get_30day_window(selected_date, spx_df):
    """Return SPX rows from selected_date through the next 30 trading days."""
    selected_row = spx_df[spx_df['Date'] == selected_date]
    next_30 = spx_df[spx_df['Date'] > selected_date].head(30)
    return pd.concat([selected_row, next_30]).reset_index(drop=True)


def build_outcome(pred_row, is_verified):
    """Return (label, text_color, bg_color, border_color) for the verdict banner."""
    crash_flag = int(pred_row['Crash_Warning_Flag'].iloc[0]) if not pred_row.empty else 0
    if crash_flag == 1:
        if is_verified:
            true_downturn = pred_row['True_Downturn'].iloc[0]
            if pd.notna(true_downturn) and int(true_downturn) == 1:
                return ("⚠️ Model Predicted: DOWNTURN &nbsp;|&nbsp; Actual: DOWNTURN &nbsp;→&nbsp; ✅ CORRECT",
                        "#68d391", "#0d2418", "#68d391")
            else:
                return ("⚠️ Model Predicted: DOWNTURN &nbsp;|&nbsp; Actual: NO DOWNTURN &nbsp;→&nbsp; ❌ FALSE ALARM",
                        "#fc8181", "#2d1515", "#fc8181")
        else:
            return ("⚠️ Model Predicted: DOWNTURN &nbsp;|&nbsp; Actual: ⏳ Pending Verification",
                    "#f6e05e", "#2d2410", "#f6e05e")
    else:
        if is_verified:
            true_downturn = pred_row['True_Downturn'].iloc[0]
            if pd.notna(true_downturn) and int(true_downturn) == 1:
                return ("✅ Model Predicted: SAFE &nbsp;|&nbsp; Actual: DOWNTURN &nbsp;→&nbsp; ❌ MISSED",
                        "#fc8181", "#2d1515", "#fc8181")
            else:
                return ("✅ Model Predicted: SAFE &nbsp;|&nbsp; Actual: NO DOWNTURN &nbsp;→&nbsp; ✅ CORRECT",
                        "#68d391", "#0d2418", "#68d391")
        else:
            return ("✅ Model Predicted: SAFE &nbsp;|&nbsp; Actual: ⏳ Pending Verification",
                    "#f6e05e", "#2d2410", "#f6e05e")


def create_spx_chart(selected_date, spx_df):
    window = get_30day_window(selected_date, spx_df)

    if window.empty:
        return None

    reference_price = float(window.iloc[0]['Close'])
    threshold_price = reference_price * 0.97

    # Days after the selected date where price breached the -3% threshold
    future_window = window.iloc[1:]
    breach_days = future_window[future_window['Close'] < threshold_price]

    fig = go.Figure()

    # Shaded danger zone below threshold
    fig.add_hrect(
        y0=0, y1=threshold_price,
        fillcolor="rgba(252, 129, 129, 0.05)",
        line_width=0,
    )

    # SPX price line
    fig.add_trace(go.Scatter(
        x=window['Date'],
        y=window['Close'],
        mode='lines+markers',
        name='S&P 500 (PX_LAST)',
        line=dict(color='#60a5fa', width=2.5),
        marker=dict(size=5, color='#60a5fa'),
        hovertemplate='%{x|%b %d, %Y}<br>S&P 500: <b>%{y:,.2f}</b><extra></extra>'
    ))

    # Reference price (dotted)
    fig.add_hline(
        y=reference_price,
        line_dash='dot',
        line_color='#94a3b8',
        line_width=1.5,
        annotation_text=f'Reference: {reference_price:,.2f}',
        annotation_position='top left',
        annotation_font=dict(color='#94a3b8', size=11)
    )

    # -3% threshold (dashed red)
    fig.add_hline(
        y=threshold_price,
        line_dash='dash',
        line_color='#fc8181',
        line_width=1.5,
        annotation_text=f'-3% Threshold: {threshold_price:,.2f}',
        annotation_position='bottom right',
        annotation_font=dict(color='#fc8181', size=11)
    )

    # Selected date reference marker (purple diamond)
    fig.add_trace(go.Scatter(
        x=[window.iloc[0]['Date']],
        y=[reference_price],
        mode='markers',
        name='Selected Date',
        marker=dict(color='#c084fc', size=12, symbol='diamond',
                    line=dict(width=2, color='#0e1117')),
        hovertemplate='%{x|%b %d, %Y}<br>Reference Price: <b>%{y:,.2f}</b><extra></extra>'
    ))

    # Breach markers (red X)
    if not breach_days.empty:
        fig.add_trace(go.Scatter(
            x=breach_days['Date'],
            y=breach_days['Close'],
            mode='markers',
            name='3% Breach Day',
            marker=dict(color='#fc8181', size=13, symbol='x',
                        line=dict(width=2.5, color='#fc8181')),
            hovertemplate='%{x|%b %d, %Y}<br>Price: <b>%{y:,.2f}</b><br>Breached -3% threshold<extra></extra>'
        ))

    fig.update_layout(
        height=500,
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=50, b=80),
        font=dict(family='Inter, sans-serif', size=12, color='#e2e8f0'),
        title=dict(
            text=f"S&P 500 — 30 Trading Days from {selected_date.strftime('%b %d, %Y')}",
            font=dict(size=16, color='#e2e8f0'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.06)',
            gridwidth=1,
            title_font=dict(color='#94a3b8'),
            tickfont=dict(color='#94a3b8'),
            linecolor='rgba(255,255,255,0.1)',
        ),
        yaxis=dict(
            title='S&P 500 Index (PX_LAST)',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.06)',
            gridwidth=1,
            tickformat=',.0f',
            title_font=dict(color='#94a3b8'),
            tickfont=dict(color='#94a3b8'),
            linecolor='rgba(255,255,255,0.1)',
        ),
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.18,
            xanchor='center',
            x=0.5,
            font=dict(color='#e2e8f0', size=11),
            bgcolor='rgba(14,17,23,0.8)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor='#1e293b',
            font_size=12,
            font_family='Inter',
            font_color='#e2e8f0'
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
            <p style="color: #94a3b8; font-size: 1rem;">S&P 500 Downturn Risk Monitoring</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Load data
    spx_df = load_spx_data()
    pred_df = load_predictions()
    cutoff_date = compute_cutoff(pred_df, spx_df)

    # Available prediction dates (trading days only)
    available_dates = sorted(pred_df['Date'].dropna().unique())

    # Default selection: most recent verified date
    verified_dates = [d for d in available_dates if pd.Timestamp(d) <= cutoff_date] if cutoff_date else []
    default_date = verified_dates[-1] if verified_dates else available_dates[-1]
    default_idx = list(available_dates).index(default_date)

    # --- Date selector (main page) ---
    sel_col1, sel_col2, sel_col3 = st.columns([1, 2, 1])
    with sel_col2:
        st.markdown("#### 📅 Select a Prediction Date")
        selected_date = st.selectbox(
            "Select a prediction date to view the 30-day S&P 500 window:",
            options=available_dates,
            index=default_idx,
            format_func=lambda d: pd.Timestamp(d).strftime('%B %d, %Y'),
        )
        selected_date = pd.Timestamp(selected_date)

        is_verified = (cutoff_date is not None) and (selected_date <= cutoff_date)

        if is_verified:
            st.success("Full 30-day outcome verified for this date.")
        else:
            if cutoff_date:
                st.warning(f"Prediction only — 30-day window extends past available data (verified up to {cutoff_date.strftime('%b %d, %Y')}).")

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.info("💡 **Public Access**\n\nView risk predictions and S&P 500 outcomes. Advanced analytics require admin access.")

        if st.button("🔐 Admin Login", use_container_width=True):
            st.switch_page("pages/2_🔐_Admin_Login.py")

    # Get prediction row for selected date
    pred_row = pred_df[pred_df['Date'] == selected_date]

    if pred_row.empty:
        st.error(f"No prediction data available for {selected_date.strftime('%b %d, %Y')}. Please select another date.")
        st.stop()

    crash_flag = int(pred_row['Crash_Warning_Flag'].iloc[0])
    risk_score = float(pred_row['Predicted_Risk_Score'].iloc[0])

    # Determine actual outcome and model result
    if is_verified:
        true_downturn_val = pred_row['True_Downturn'].iloc[0]
        if pd.notna(true_downturn_val):
            actual_downturn = int(true_downturn_val)
            model_correct = (crash_flag == 1 and actual_downturn == 1) or \
                            (crash_flag == 0 and actual_downturn == 0)
        else:
            actual_downturn = None
            model_correct = None
    else:
        actual_downturn = None
        model_correct = None

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if crash_flag == 1:
            st.markdown(f"""
            <div class="warning-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #fc8181;">⚠️ Model Prediction</div>
                <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#fc8181; color:#fc8181;">DOWNTURN<br>WARNING</div>
                <div style="margin-top: 0.5rem; font-size:0.8rem; color: #94a3b8;">{selected_date.strftime('%b %d, %Y')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #68d391;">✅ Model Prediction</div>
                <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#68d391; color:#68d391;">SAFE</div>
                <div style="margin-top: 0.5rem; font-size:0.8rem; color: #94a3b8;">{selected_date.strftime('%b %d, %Y')}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #64748b;">📈 Risk Score</div>
            <div class="big-number">{risk_score:.3f}</div>
            <div style="font-size: 0.7rem; color: #64748b;">0 = Low Risk &nbsp;→&nbsp; 1 = High Risk</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top:0.25rem;">Threshold: &gt; 0.20 triggers warning</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if actual_downturn is not None:
            if actual_downturn == 1:
                st.markdown(f"""
                <div class="warning-card">
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #fc8181;">📉 Actual Outcome</div>
                    <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#fc8181; color:#fc8181;">DOWNTURN</div>
                    <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">≥3% drop occurred within 30 trading days</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="safe-card">
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #68d391;">📈 Actual Outcome</div>
                    <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#68d391; color:#68d391;">NO<br>DOWNTURN</div>
                    <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">No ≥3% drop within 30 trading days</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="pending-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #f6e05e;">⏳ Actual Outcome</div>
                <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#f6e05e; color:#f6e05e;">PENDING</div>
                <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">30-day window not yet complete</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        if model_correct is not None:
            if model_correct:
                st.markdown(f"""
                <div class="correct-card">
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #68d391;">🎯 Model Result</div>
                    <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#68d391; color:#68d391;">CORRECT</div>
                    <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">Prediction matched actual outcome</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="incorrect-card">
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #fc8181;">🎯 Model Result</div>
                    <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#fc8181; color:#fc8181;">INCORRECT</div>
                    <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">Prediction did not match outcome</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="pending-card">
                <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #f6e05e;">🎯 Model Result</div>
                <div class="big-number" style="font-size:1.6rem; -webkit-text-fill-color:#f6e05e; color:#f6e05e;">PENDING</div>
                <div style="font-size:0.8rem; color: #94a3b8; margin-top:0.5rem;">Awaiting full 30-day window</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Main chart
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <h3 style="color: #93c5fd; font-weight: 600; display: inline-block;
                   border-bottom: 3px solid #fc8181; padding-bottom: 0.25rem;">
            📊 S&P 500 Price — 30-Day Downturn Window
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # Check if SPX data exists for selected date
    spx_on_date = spx_df[spx_df['Date'] == selected_date]
    if spx_on_date.empty:
        st.warning(f"No S&P 500 price data found for {selected_date.strftime('%b %d, %Y')}. The chart cannot be displayed.")
    else:
        # Verdict banner
        outcome_label, text_color, bg_color, border_color = build_outcome(pred_row, is_verified)
        st.markdown(
            f"""<div style="background:{bg_color}; border:1.5px solid {border_color};
                border-radius:0.6rem; padding:0.65rem 1.2rem; text-align:center;
                font-size:0.95rem; font-weight:600; color:{text_color}; margin-bottom:0.5rem;">
                {outcome_label}
            </div>""",
            unsafe_allow_html=True
        )

        fig = create_spx_chart(selected_date, spx_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

        # Chart caption
        window = get_30day_window(selected_date, spx_df)
        ref_price = float(window.iloc[0]['Close']) if not window.empty else None
        if ref_price:
            available_days = len(window) - 1
            st.caption(
                f"Reference price on {selected_date.strftime('%b %d, %Y')}: **{ref_price:,.2f}**  |  "
                f"-3% threshold: **{ref_price * 0.97:,.2f}**  |  "
                f"Trading days shown: **{available_days}**/30"
                + ("  |  ⚠️ Partial window (data ends Apr 2, 2026)" if available_days < 30 else "")
            )

    # Locked Content Section
    st.markdown("---")
    st.markdown("### <span style='color: #e2e8f0;'>🔒 Advanced Analytics</span>", unsafe_allow_html=True)
    st.caption("Login as admin to unlock sentiment analysis, model confidence, and advanced metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="locked-content">
            <div style="font-size: 3rem;">🔒</div>
            <h3 style="color: #e2e8f0;">Sentiment &amp; Momentum</h3>
            <p style="color: #94a3b8;">Track social media sentiment and market momentum indicators</p>
            <span style="font-size: 0.7rem; color: #64748b;">Admin access required</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="locked-content">
            <div style="font-size: 3rem;">🔒</div>
            <h3 style="color: #e2e8f0;">Ensemble Model</h3>
            <p style="color: #94a3b8;">View individual model predictions and confidence scores</p>
            <span style="font-size: 0.7rem; color: #64748b;">Admin access required</span>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 0.7rem; padding: 1rem;">
        🐻 THE BEAR PATROL | S&P 500 Downturn Prediction Model
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

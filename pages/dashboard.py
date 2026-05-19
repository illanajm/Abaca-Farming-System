import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database import (
    session,
    Farmer,
    Farm,
    AbacaCultivation,
    PestManagement,
    SoilManagement
)
from analytics_engine import (
    descriptive_stats,
    frequency_table,
    correlation_analysis,
    detect_outliers,
    generate_insights
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

/* MAIN APP */
.stApp {
    background-color: #f4f6f9;
}

/* =========================
   SIDEBAR
   ========================= */
[data-testid="stSidebar"] {
    background: linear-gradient(
        white
    );
    width: 270px;
    border-right: 2px solid #ffffff20;
}

/* Hide default nav */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: black !important;
}

/* Sidebar buttons */
.stButton button {
    width: 100%;
    border-radius: 12px !important;
    background-color: #ffffff20 !important;
    color: white !important;
    border: 1px solid #ffffff30 !important;
    height: 45px;
    font-weight: 600;
}

.stButton > button {
    background-color: transparent !important;
    color: #006622 !important;
    border: 1px solid #006622 !important;
    border-radius: 8px !important;
    height: 32px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}

/* HOVER */
.stButton > button:hover {
    background-color: #006622 !important;
    color: white !important;
}

/* =========================
   LOGO AREA
   ========================= */
.logo-container {
    text-align: center;
    padding-top: 10px;
    padding-bottom: 20px;
}

.logo-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-top: 10px;
    text-align: center;
    top: -100px;
}

.logo-subtitle {
    color: #d9ffd9;
    font-size: 14px;
    text-align: center;
}

/* KPI CARD */
.kpi-card {
    background: white;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 128, 0, 0.25);
    padding: 18px;
    border-radius: 15px;
    color: #0b3d0b;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0, 128, 0, 0.15);
    margin-bottom: 10px;
}

.kpi-title {
    font-size: 14px;
    opacity: 0.9;
}

.kpi-value {
    font-size: 30px;
    font-weight: bold;
}

/* SECTION BOX */
.section-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}


/* HEADER */
.main-title {
    color: #006622;
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 0;
}

.sub-title {
    color: #666;
    margin-top: 0;
}

.welcome-top-right {
    position: absolute;
    top: -35px;
    right: 30px;
    font-size: 16px;
    color: #666;
    font-weight: 500;
    z-index: 999;
}

</style>
""", unsafe_allow_html=True)

# =========================
# AUTH CHECK
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("app.py")

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image("public/logos/abaca_logo.png", width=120)

    st.markdown("""
        <div class="logo-title">
            ABACA FARMING
        </div>

        <div class="logo-subtitle">
            Management System
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.page_link(
        "pages/dashboard.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/farmers.py",
        label="👨‍🌾 Farmers"
    )

    st.page_link(
        "pages/farms.py",
        label="🌱 Farms"
    )

    st.page_link(
        "pages/cultivation.py",
        label="🌾 Cultivation"
    )

    st.page_link(
        "pages/pest_management.py",
        label="🐛 Pest Management"
    )

    st.page_link(
        "pages/soil_management.py",
        label="🧪 Soil Management"
    )
    st.page_link("pages/reports.py", label="📊 Analytics & Reports")

    st.markdown("---")

# =========================
# DATABASE COUNTS (REAL DATA)
# =========================
total_farmers = session.query(Farmer).count()
total_farms = session.query(Farm).count()
total_cultivation = session.query(AbacaCultivation).count()
total_pests = session.query(PestManagement).count()
total_soil = session.query(SoilManagement).count()

col1, col2 = st.columns([8, 1.5])

with col2:
    with st.popover(f"Welcome back, {st.session_state.get('user', 'Farmer')}"):

        st.markdown("### Account")

        st.write(f"User: {st.session_state.get('user', 'Farmer')}")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.switch_page("app.py")

# =========================
# KPI CARD FUNCTION
# =========================
def kpi_card(title, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card("Farmers", total_farmers)

with col2:
    kpi_card("Farms", total_farms)

with col3:
    kpi_card("Cultivation", total_cultivation)

with col4:
    kpi_card("Pests", total_pests)

with col5:
    kpi_card("Soil Records", total_soil)

# =========================
# DATA FOR CHART + TABLE
# =========================
chart_df = pd.DataFrame({
    "Module": ["Farmers", "Farms", "Cultivation", "Pests", "Soil"],
    "Records": [total_farmers, total_farms, total_cultivation, total_pests, total_soil]
})

# =========================
# MAIN LAYOUT (LIKE IMAGE)
# =========================
left, right = st.columns([2, 1])

# =========================
# BAR CHART (LEFT)
# =========================
with left:

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Records",
        x=chart_df["Module"],
        y=chart_df["Records"],
        marker_color="#006622",
        width=0.2
    ))

    fig.update_layout(
        title="Abaca System Overview",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# TABLE (RIGHT)
# =========================
with right:

    st.markdown("""
    <div class="section-box">
        <h4>Module Summary</h4>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # PIE CHART
    # =========================
    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Pie(
        labels=chart_df["Module"],
        values=chart_df["Records"],
        hole=0.4,  # donut style
        textinfo="label+percent",
        insidetextorientation="radial",
        marker=dict(
            colors=["#006622", "#1f6f4a", "#468767", "#2e8b57", "#3cb371"]
        )
    )])

    # =========================
    # LAYOUT
    # =========================
    fig.update_layout(
        title="Module Distribution",
        template="plotly_white",
        height=360,
        margin=dict(t=50, b=20, l=20, r=20)
    )

    # =========================
    # DISPLAY
    # =========================
    st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHTS SECTION
# =========================
st.markdown("##System Insights")

highest = chart_df.loc[chart_df["Records"].idxmax()]
lowest = chart_df.loc[chart_df["Records"].idxmin()]
total = chart_df["Records"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="section-box">
        <h4>Highest Module</h4>
        <h2>{highest['Module']}</h2>
        <p>{highest['Records']} records</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="section-box">
        <h4>Lowest Module</h4>
        <h2>{lowest['Module']}</h2>
        <p>{lowest['Records']} records</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="section-box">
        <h4>Total Records</h4>
        <h2>{total}</h2>
        <p>All system modules combined</p>
    </div>
    """, unsafe_allow_html=True)
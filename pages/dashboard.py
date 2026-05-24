import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import func
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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Abaca Farming System",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: black;
}
.stApp {
    background-color: #f0f7f2;  /* clean dashboard gray */
}
/* =========================
   SIDEBAR
   ========================= */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #006622, #1f6f4a, #468767) !important;

    width: 270px;
    border-right: 2px solid #ffffff20;
}

/* Hide default nav */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
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

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 10px 10px rgba(0,0,0,0.06);
}

.metric-container {
    display: flex;
    align-items: center;
    gap: 18px;
}

.metric-icon {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background-color: #e8f5e9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 35px;
    color: #1b8f3a;
}

.metric-title {
    color: #777;
    font-size: 14px;
    margin-bottom: 5px;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #111;
}

.section-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}


</style>
""", unsafe_allow_html=True)

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

soil_quality_data = session.query(
    Farm.soil_quality,
    func.count(Farm.id).label("total")
).group_by(Farm.soil_quality).all()

soil_type_data = session.query(
    Farm.soil_type,
    func.count(Farm.id).label("total")
).group_by(Farm.soil_type).all()

overall_total_production = session.query(func.sum(Farm.average_yield)).scalar() or 0

total_cultivation_area = session.query(func.sum(AbacaCultivation.abaca_area)).scalar() or 0

total_farms_average_yield = overall_total_production / total_cultivation_area if total_cultivation_area > 0 else 0

total_barangays = session.query(
    func.count(func.distinct(Farmer.barangay))
).scalar() or 1   # avoid division by zero

production_per_barangay = total_farms_average_yield / total_barangays

production_by_barangay = session.query(
    Farmer.barangay,
    func.sum(Farm.average_yield).label("total_production")
).join(Farm, Farmer.id == Farm.farmer_id)\
 .group_by(Farmer.barangay)\
 .all()

total_cultivation = session.query(AbacaCultivation).count()


total_pests = session.query(PestManagement).count()

total_soil = session.query(SoilManagement).count()

farmers = session.query(Farmer.age).all()

irrigation_data = session.query(
    Farm.irrigation_source,
    func.count(Farm.farmer_id).label("total_farmers")
).group_by(Farm.irrigation_source).all()

production_by_year = session.query(
    AbacaCultivation.year_first_planted,
    func.sum(Farm.average_yield).label("total_production")
).join(Farm, AbacaCultivation.farm_id == Farm.id)\
 .group_by(AbacaCultivation.year_first_planted)\
 .order_by(AbacaCultivation.year_first_planted)\
 .all()

# ---------------- HEADER ----------------
col1, col2 = st.columns([9, 1])

with col1:
    st.markdown(
        "<h4 style='margin-bottom:0px;'>Dashboard</h4>",
        unsafe_allow_html=True
    )

with col2:

    with st.popover(f"👤 {st.session_state.get('user', 'Farmer')}"):

        st.markdown("### Account")

        st.write(f"User: {st.session_state.get('user', 'Farmer')}")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.switch_page("app.py")

st.write("")

# ---------------- TOP METRICS ----------------
m1, m2, m3, m4 = st.columns(4)

st.markdown("""
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-container">
            <div class="metric-icon">
                <i class="fas fa-users"></i>
            </div>
            <div>
                <div class="metric-title">Total Farmers</div>
                <div class="metric-value">{total_farmers}</div>
                Registered Farmers
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-container">
            <div class="metric-icon">
                <i class="fas fa-seedling"></i>
            </div>
            <div>
                <div class="metric-title">Total Area Cultivated</div>
                <div class="metric-value">{total_cultivation_area:,.1f}</div>
                Hectares
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-container">
            <div class="metric-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <div>
                <div class="metric-title">Average Yield</div>
                <div class="metric-value">{total_farms_average_yield:,.1f}</div>
                kg / year
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-container">
            <div class="metric-icon">
                <i class="fas fa-leaf"></i>
            </div>
            <div>
                <div class="metric-title">Total Production</div>
                <div class="metric-value">{overall_total_production:,.1f}</div>
                kg / year
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- CHART SECTION ----------------
left, middle, right = st.columns([1.2, 1.2, 1])

# ---------- PIE CHART ----------
with left:
    st.markdown("### Soil Quality Overview")

    df_soil = pd.DataFrame(soil_quality_data, columns=["Soil Quality", "Count"])

    # 🔥 convert to percentage
    df_soil["Percent"] = (df_soil["Count"] / df_soil["Count"].sum()) * 100

    fig = px.pie(
        df_soil,
        values="Percent",
        names="Soil Quality",
        color_discrete_sequence=[
            "#1F7A8C",  # Excellent - dark green
            "#0B6E4F",  # Good - ocean blue
            "#B22222",  # Average - brown
            "#C68642"   # Poor - red
        ]
    )

    fig.update_traces(textinfo="percent+label")

    fig.update_layout(height=350)

    st.plotly_chart(fig, use_container_width=True)

# ---------- DONUT CHART ----------
with middle:
    st.markdown("### Soil Type Distribution")

    df_soil_type = pd.DataFrame(soil_type_data, columns=["Soil Type", "Count"])

    # 🔥 convert to percentage
    df_soil_type["Percent"] = (df_soil_type["Count"] / df_soil_type["Count"].sum()) * 100

    fig2 = px.pie(
        df_soil_type,
        values="Percent",
        names="Soil Type",
        hole=0.4,
        color_discrete_sequence=[
            "#0B6E4F",  # dark green
            "#8B5E3C",  # brown
            "#1F7A8C"   # ocean blue
        ]
    )

    fig2.update_traces(textinfo="percent+label")

    fig2.update_layout(height=350)

    # center plant symbol
    fig2.add_annotation(
        text="🌱",
        x=0.5,
        y=0.5,
        font_size=40,
        showarrow=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------- IRRIGATION ----------
with right:
    st.markdown("### Irrigation Sources")

    df_irrigation = pd.DataFrame(
        irrigation_data,
        columns=["Irrigation Source", "Total Farmers"]
    )

    st.dataframe(
        df_irrigation,
        use_container_width=True,
        hide_index=True
    )

st.write("")

# ---------------- SECOND ROW ----------------
c1, c2, c3 = st.columns([1.2, 1.5, 1])

# ---------- TOP BARANGAYS ----------
with c1:
    st.markdown("### Top Producing Barangays")

    df_prod_barangay = pd.DataFrame(
        production_by_barangay,
        columns=["Barangay", "Total Production"]
    )

    st.dataframe(
        df_prod_barangay,
        use_container_width=True,
        hide_index=True
    )

# ---------- AGE DISTRIBUTION ----------
with c2:
    st.markdown("### Age Distribution of Farmers")

    age_groups = {
        "20-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0,
        "61 above": 0
    }

    for (age,) in farmers:
        if age is None:
            continue

        if 20 <= age <= 30:
            age_groups["20-30"] += 1
        elif 31 <= age <= 40:
            age_groups["31-40"] += 1
        elif 41 <= age <= 50:
            age_groups["41-50"] += 1
        elif 51 <= age <= 60:
            age_groups["51-60"] += 1
        elif age >= 61:
            age_groups["61 above"] += 1

    ages = pd.DataFrame({
        "Age Group": list(age_groups.keys()),
        "Farmers": list(age_groups.values())
    })

    fig3 = px.bar(
        ages,
        x="Age Group",
        y="Farmers",
        text="Farmers"
    )

    # BAR COLOR + WIDTH ADJUSTMENT
    fig3.update_traces(
        marker_color="#0B6E4F",  # dark green
        width=0.5               # bar width (0.3–0.8 good range)
    )

    fig3.update_layout(
        height=350,
        xaxis_title="Age Group",
        yaxis_title="Number of Farmers",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

with c3:
    st.markdown("### Production Trend (kg)")

    production = pd.DataFrame(
        production_by_year,
        columns=["Year", "Production"]
    )

    fig4 = px.line(
        production,
        x="Year",
        y="Production",
        markers=True
    )

    fig4.update_traces(
        line_color="#0B6E4F",
        marker_color="#0B6E4F"
    )

    fig4.update_layout(
        height=320,
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="",
        yaxis_title=""
    )

    st.plotly_chart(fig4, use_container_width=True)
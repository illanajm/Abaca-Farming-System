import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils.ui import hide_streamlit_ui
from utils.sidebar import render_sidebar
from utils.ui import apply_global_css
from utils.header import render_header
from analytics_engine import generate_analysis_engine
from report_engine.pdf_report import generate_pdf_report
from report_engine.excel_report import generate_excel_report

from database import (
    session,
    Farmer,
    Farm,
    AbacaCultivation,
    PestManagement,
    SoilManagement,
    SoilQuality,
    SoilType,
    IrrigationSource,
    EnvironmentalFactor,
    AccessToInputs,
    InputSource,
    Variety,
    PlantingMethod,
    PlantingDistance,
    IntercropCrops,
    PestType,
    PestImpact,
    ControlMethod,
    ControlFrequency,
    SoilTesting,
    TestingFrequency,
    SoilConservation,
    ConservationTechniques,
    SeasonalEffects
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from openpyxl import Workbook
from openpyxl.styles import Font

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Analytics & Reports",
    layout="wide"
)

hide_streamlit_ui()
render_sidebar() # Render custom sidebar with navigation links
apply_global_css() # Apply global CSS for consistent styling
render_header() # Render consistent header across pages

# =========================
# CUSTOM CSS (MODERN GREEN UI)
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
    font-family: 'Segoe UI', sans-serif;
}

/* TITLE */
.page-title {
    font-size: 38px;
    font-weight: 800;
    color: #0b3d0b;
}

.page-subtitle {
    font-size: 15px;
    color: #666;
}

/* GLASS KPI */
.metric-card {
    background: rgba(0, 128, 0, 0.12);
    border: 1px solid rgba(0, 128, 0, 0.25);
    box-shadow: 0 8px 25px rgba(0, 128, 0, 0.12);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #0b3d0b;
}

.metric-label {
    font-size: 13px;
    color: #1b5e20;
    font-weight: 600;
}

/* SECTION BOX */
.section-box {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# AUTH
# =========================
if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.switch_page("app.py")

# =========================
# HEADER
# =========================
st.markdown("""
<div class="page-title">Abaca Farming Analytics</div>
<div class="page-subtitle">Insights, trends, and downloadable reports</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =========================
# LOAD DATA
# =========================
farmers = session.query(Farmer).all()
farms = session.query(Farm).all()
cultivations = session.query(AbacaCultivation).all()
pests = session.query(PestManagement).all()

# =========================
# DATAFRAMES
# =========================
df_farmers = pd.DataFrame([{
    "farmer_id": f.id,
    "Farmer": f"{f.firstname} {f.middlename} {f.lastname}",
    "Age": f.age,
    "Barangay": f.barangay,
    "Years Farming": f.years_in_farming
} for f in farmers])

df_farms = pd.DataFrame([{
    "farm_id": f.id,
    "farmer_id": f.farmer_id,

    "Farmer": (
        f"{session.query(Farmer).filter_by(id=f.farmer_id).first().firstname} "
        f"{session.query(Farmer).filter_by(id=f.farmer_id).first().middlename} "
        f"{session.query(Farmer).filter_by(id=f.farmer_id).first().lastname}"
        if session.query(Farmer).filter_by(id=f.farmer_id).first()
        else None
    ),

    "Farm Area": f.farm_area,

    "Soil Type": (
        session.query(SoilType).filter_by(id=f.soil_type_id).first().description
        if session.query(SoilType).filter_by(id=f.soil_type_id).first()
        else None
    ),

    "Yield": f.average_yield
} for f in farms])

df_cultivation = pd.DataFrame([{
    "abaca_id": c.id,
    "farm_id": c.farm_id,
    "Variety": (
        session.query(Variety)
        .filter_by(id=c.variety_id)
        .first().description
        if session.query(Variety).filter_by(id=c.variety_id).first()
        else None
    )
} for c in cultivations])

df_pests = pd.DataFrame([{
    "abaca_id": p.abaca_id,
    "Pest Type": (
        session.query(PestType)
        .filter_by(id=p.pest_type_id)
        .first().description
        if session.query(PestType).filter_by(id=p.pest_type_id).first()
        else None
    )
} for p in pests])

filter_df = (
    df_farms[
        ["farm_id", "farmer_id", "Farmer"]
    ]
    .merge(
        df_farmers[
            ["farmer_id", "Barangay", "Age"]
        ],
        on="farmer_id",
        how="left"
    )
    .merge(
        df_cultivation[
            ["farm_id", "Variety"]
        ],
        on="farm_id",
        how="left"
    )
)

# =========================
# FILTERS
# =========================
st.markdown("### Filters")

# -------------------------
# Session State
# -------------------------
if "selected_farmer" not in st.session_state:
    st.session_state.selected_farmer = "All"

if "selected_barangay" not in st.session_state:
    st.session_state.selected_barangay = "All"

if "selected_variety" not in st.session_state:
    st.session_state.selected_variety = "All"

# -------------------------
# Age values
# -------------------------
min_age_default = 0
max_age_default = 150

# -------------------------
# Determine dropdown values
# -------------------------
available_farmers = sorted(
    df_farmers["Farmer"].dropna().unique()
)

available_barangays = sorted(
    df_farmers["Barangay"].dropna().unique()
)

available_varieties = sorted(
    df_cultivation["Variety"].dropna().unique()
)

disable_barangay = False
disable_age = False

# ======================================
# FARMER SELECTED
# ======================================
if st.session_state.selected_farmer != "All":

    disable_barangay = True
    disable_age = True

    farmer_info = filter_df[
        filter_df["Farmer"]
        == st.session_state.selected_farmer
    ]

    available_varieties = sorted(
        farmer_info["Variety"]
        .dropna()
        .unique()
    )

# ======================================
# BARANGAY SELECTED
# ======================================
elif st.session_state.selected_barangay != "All":

    barangay_df = filter_df[
        filter_df["Barangay"]
        == st.session_state.selected_barangay
    ]

    age_min = st.session_state.get("min_age", 0)
    age_max = st.session_state.get("max_age", 150)

    barangay_df = barangay_df[
        (barangay_df["Age"] >= age_min)
        &
        (barangay_df["Age"] <= age_max)
    ]

    available_farmers = sorted(
        barangay_df["Farmer"]
        .dropna()
        .unique()
    )

    available_varieties = sorted(
        barangay_df["Variety"]
        .dropna()
        .unique()
    )

# ======================================
# VARIETY SELECTED
# ======================================
elif st.session_state.selected_variety != "All":

    variety_df = filter_df[
        filter_df["Variety"]
        == st.session_state.selected_variety
    ]

    available_farmers = sorted(
        variety_df["Farmer"]
        .dropna()
        .unique()
    )

    available_barangays = sorted(
        variety_df["Barangay"]
        .dropna()
        .unique()
    )

# -------------------------
# UI
# -------------------------

f1, f2, f3, f4 = st.columns([2, 2, 2, 2])

with f1:

    selected_farmer = st.selectbox(
        "Farmer",
        ["All"] + list(available_farmers),
        key="selected_farmer"
    )

with f2:

    selected_barangay = st.selectbox(
        "Barangay",
        ["All"] + list(available_barangays),
        disabled=disable_barangay,
        key="selected_barangay"
    )

with f3:

    selected_variety = st.selectbox(
        "Variety",
        ["All"] + list(available_varieties),
        key="selected_variety"
    )

with f4:

    age_col1, age_col2 = st.columns(2)

    with age_col1:

        min_age = st.number_input(
            "Min Age",
            min_value=0,
            value=0,
            disabled=disable_age,
            key="min_age"
        )

    with age_col2:

        max_age = st.number_input(
            "Max Age",
            min_value=0,
            value=150,
            disabled=disable_age,
            key="max_age"
        )

# =========================
# FILTER LOGIC
# =========================
filtered_farmers = df_farmers.copy()

# AGE RANGE FILTER
filtered_farmers = filtered_farmers[
    (filtered_farmers["Age"] >= min_age) &
    (filtered_farmers["Age"] <= max_age)
]

if min_age > max_age:
    st.error("Min Age cannot be greater than Max Age")
    st.stop()

if selected_farmer != "All":
    filtered_farmers = filtered_farmers[filtered_farmers["Farmer"] == selected_farmer]

if selected_barangay != "All":
    filtered_farmers = filtered_farmers[filtered_farmers["Barangay"] == selected_barangay]

farmer_ids = filtered_farmers["farmer_id"].tolist() if not filtered_farmers.empty else []

filtered_farms = df_farms[df_farms["farmer_id"].isin(farmer_ids)]
farm_ids = filtered_farms["farm_id"].tolist() if not filtered_farms.empty else []

filtered_cultivation = df_cultivation[df_cultivation["farm_id"].isin(farm_ids)]

if selected_variety != "All":
    filtered_cultivation = filtered_cultivation[filtered_cultivation["Variety"] == selected_variety]

abaca_ids = filtered_cultivation["abaca_id"].tolist() if not filtered_cultivation.empty else []

filtered_pests = df_pests[df_pests["abaca_id"].isin(abaca_ids)]


# =========================
# KPI CARDS
# =========================
st.markdown("### Summary Metrics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_farmers)}</div>
        <div class="metric-label">Farmers</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_farms)}</div>
        <div class="metric-label">Farms</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    avg_yield = round(filtered_farms["Yield"].mean(), 2) if not filtered_farms.empty else 0

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_yield}</div>
        <div class="metric-label">Avg Yield</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_pests)}</div>
        <div class="metric-label">Pests</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CHARTS SECTION
# =========================
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-box"><h4> Age Distribution</h4></div>', unsafe_allow_html=True)

    if not filtered_farmers.empty:
        fig = px.histogram(
            filtered_farmers,
            x="Age",
            nbins=20,
            color_discrete_sequence=["#4cb817"]  # dark green
        )

        fig.update_traces(
            marker_line_width=0.1,   # border line
            marker_line_color="#06402B"  # darker green outline
        )

        fig.update_layout(
            bargap=0.1,  # controls bar width spacing (lower = thicker bars)
            plot_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-box"><h4> Soil Type</h4></div>', unsafe_allow_html=True)

    if not filtered_farms.empty:
        fig = px.pie(filtered_farms, names="Soil Type")
        st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-box"><h4> Yield vs Farm Area</h4></div>', unsafe_allow_html=True)

if not filtered_farms.empty:
    fig = px.scatter(
        filtered_farms,
        x="Farm Area",
        y="Yield",
        size="Yield",
        color="Soil Type"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-box"><h4> Pest Incidence</h4></div>', unsafe_allow_html=True)

if not filtered_pests.empty:
    pest_count = filtered_pests["Pest Type"].value_counts().reset_index()
    pest_count.columns = ["Pest", "Count"]

    fig = px.bar(pest_count, x="Pest", y="Count", color_discrete_sequence=["#4cb817"]  # dark green
        )
    fig.update_traces(
        width=0.5  # adjust bar width (0.3–0.8 best range)
    )
    st.plotly_chart(fig, use_container_width=True)


# =========================
# ANALYTICS ENGINE
# =========================

corr = None

if len(filtered_farms) >= 3:

    corr = filtered_farms["Farm Area"].corr(
        filtered_farms["Yield"]
    )

    if pd.isna(corr):
        corr = None

# Generate AI Analysis
ai_result = generate_analysis_engine(
    filtered_farmers,
    filtered_farms,
    filtered_pests,
    corr
)

# =========================
# AI GENERATED ANALYSIS
# =========================

st.markdown("---")

st.markdown("## AI Interpretation")

for item in ai_result["interpretation"]:

    st.info(item)

st.markdown("## AI Insights")


for item in ai_result["insights"]:

    st.success(item)

st.markdown("## AI Recommendations")

for item in ai_result["recommendations"]:

    st.warning(item)

# =========================
# DOWNLOAD REPORTS
# =========================

d1, d2 = st.columns(2)

with d1:

    pdf_file = generate_pdf_report(
        ai_result,
        filtered_farmers,
        filtered_farms,
        filtered_pests
    )

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_file,
        file_name="abaca_analytics_report.pdf",
        mime="application/pdf"
    )

with d2:

    excel_file = generate_excel_report(
        ai_result,
        filtered_farmers,
        filtered_farms,
        filtered_pests
    )

    st.download_button(
        label="📊 Download Excel Report",
        data=excel_file,
        file_name="abaca_analytics_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
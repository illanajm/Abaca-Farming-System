import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from database import (
    session,
    Farmer,
    Farm,
    AbacaCultivation,
    PestManagement
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from analytics_engine import (
    descriptive_stats,
    frequency_table,
    correlation_analysis,
    detect_outliers,
    generate_insights
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

/* BUTTON */
.stButton > button {
    background-color: #006622 !important;
    color: white !important;
    border-radius: 10px !important;
    height: 42px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background-color: #009933 !important;
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

[data-testid="stSidebarNav"] {
    display: none;
}

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
.logo-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-top: 10px;
    text-align: center;
}

.logo-subtitle {
    color: #d9ffd9;
    font-size: 14px;
    text-align: center;
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

    st.page_link("pages/dashboard.py", label="🏠 Dashboard")
    st.page_link("pages/farmers.py", label="👨‍🌾 Farmers")
    st.page_link("pages/farms.py", label="🌱 Farms")
    st.page_link("pages/cultivation.py", label="🌾 Cultivation")
    st.page_link("pages/pest_management.py", label="🐛 Pest Management")
    st.page_link("pages/soil_management.py", label="🧪 Soil Management")
    st.page_link("pages/reports.py", label="📊 Analytics & Reports")

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
    "Farmer": f"{f.firstname} {f.lastname}",
    "Age": f.age,
    "Barangay": f.barangay,
    "Years Farming": f.years_in_farming
} for f in farmers])

df_farms = pd.DataFrame([{
    "farm_id": f.id,
    "farmer_id": f.farmer_id,
    "Farm Area": f.farm_area,
    "Soil Type": f.soil_type,
    "Yield": f.average_yield
} for f in farms])

df_cultivation = pd.DataFrame([{
    "abaca_id": c.id,
    "farm_id": c.farm_id,
    "Variety": c.variety
} for c in cultivations])

df_pests = pd.DataFrame([{
    "abaca_id": p.abaca_id,
    "Pest Type": p.pest_type
} for p in pests])

# =========================
# FILTERS
# =========================
st.markdown("### Filters")

f1, f2, f3, f4 = st.columns([2, 2, 2, 2])

with f1:
    selected_farmer = st.selectbox("Farmer", ["All"] + df_farmers["Farmer"].dropna().unique().tolist())

with f2:
    selected_barangay = st.selectbox("Barangay", ["All"] + df_farmers["Barangay"].dropna().unique().tolist())

with f3:
    selected_variety = st.selectbox("Variety", ["All"] + df_cultivation["Variety"].dropna().unique().tolist())

with f4:
    age_col1, age_col2 = st.columns(2)

    with age_col1:
        min_age = st.number_input(
            "Min Age",
            min_value=0,
            value=0,
            step=1
        )

    with age_col2:
        max_age = st.number_input(
            "Max Age",
            min_value=0,
            value=150,
            step=1
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
        fig = px.histogram(filtered_farmers, x="Age", nbins=10)
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

    fig = px.bar(pest_count, x="Pest", y="Count")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# DOWNLOAD FUNCTIONS (UNCHANGED)
# =========================
corr = correlation_analysis(df_farms, "Farm Area", "Yield")

def generate_pdf(corr, df_farms, df_pests, df_farmers):


    avg_yield = round(filtered_farms["Yield"].mean(), 2) if not filtered_farms.empty else 0

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    elements = []

    from reportlab.platypus import Image
    from datetime import datetime
    import numpy as np

    # =========================
    # COVER PAGE (ENTERPRISE STYLE)
    # =========================
    elements.append(
        Paragraph(
            "<b>ABACA FARMING MANAGEMENT SYSTEM</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "📊 EXECUTIVE ANALYTICS REPORT",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"Generated Date: {datetime.now().strftime('%B %d, %Y')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # =========================
    # EXECUTIVE SUMMARY
    # =========================
    elements.append(Paragraph(" Executive Summary", styles["Heading2"]))

    avg_yield = round(filtered_farms["Yield"].mean(), 2) if not filtered_farms.empty else 0
    most_common_pest = filtered_pests["Pest Type"].mode()[0] if not filtered_pests.empty else "N/A"

    summary_text = f"""
    This report provides an overview of abaca farming operations including farmers, farms, cultivation patterns,
    and pest management activities.<br/><br/>

    • Total Farmers: <b>{len(filtered_farmers)}</b><br/>
    • Total Farms: <b>{len(filtered_farms)}</b><br/>
    • Average Yield: <b>{avg_yield}</b><br/>
    • Most Common Pest: <b>{most_common_pest}</b><br/><br/>

    The data suggests opportunities for improving soil quality management and strengthening pest control strategies
    to increase overall productivity.
    """

    elements.append(Paragraph(summary_text, styles["BodyText"]))
    elements.append(Spacer(1, 20))

    # =========================
    # KPI TABLE
    # =========================
    elements.append(Paragraph(" Key Performance Indicators", styles["Heading2"]))

    kpi_data = [
        ["Metric", "Value"],
        ["Farmers", len(filtered_farmers)],
        ["Farms", len(filtered_farms)],
        ["Average Yield", avg_yield],
        ["Pest Incidents", len(filtered_pests)]
    ]

    kpi_table = Table(kpi_data, colWidths=[250, 250])

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#006622")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(kpi_table)
    elements.append(Spacer(1, 20))

    # =========================
    # CHARTS SECTION
    # =========================
    elements.append(Paragraph(" Data Visualization", styles["Heading2"]))

    if not filtered_farms.empty:

        fig = px.scatter(
            filtered_farms,
            x="Farm Area",
            y="Yield",
            color="Soil Type",
            title="Farm Area vs Yield"
        )

        img_bytes = fig.to_image(format="png")

        img_buffer = BytesIO(img_bytes)

        chart = Image(img_buffer, width=480, height=300)

        elements.append(chart)

    elements.append(Spacer(1, 20))

    # =========================
    # FARMER TABLE (CLEAN)
    # =========================
    elements.append(Paragraph(" Farmer Demographics", styles["Heading2"]))

    if not filtered_farmers.empty:

        farmer_table = Table(
            [filtered_farmers.columns.tolist()] +
            filtered_farmers.astype(str).values.tolist()
        )

        farmer_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#009933")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
        ]))

        elements.append(farmer_table)

    elements.append(Spacer(1, 20))

    elements.append(Paragraph(" Advanced Statistical Analysis", styles["Heading2"]))

    if not filtered_farms.empty:

        farm_area = filtered_farms["Farm Area"]
        yield_data = filtered_farms["Yield"]

        def stats(x):
            return {
                "mean": round(x.mean(), 2),
                "median": round(x.median(), 2),
                "mode": x.mode()[0] if not x.mode().empty else 0,
                "std": round(x.std(), 2),
                "var": round(x.var(), 2),
                "min": round(x.min(), 2),
                "max": round(x.max(), 2),
                "range": round(x.max() - x.min(), 2),
                "cv": round((x.std() / x.mean()) * 100, 2) if x.mean() != 0 else 0
            }

        farm_stats = stats(farm_area)
        yield_stats = stats(yield_data)

        advanced_data = [
            ["Metric", "Farm Area", "Yield"],

            ["Mean", farm_stats["mean"], yield_stats["mean"]],
            ["Median", farm_stats["median"], yield_stats["median"]],
            ["Mode", farm_stats["mode"], yield_stats["mode"]],

            ["Std Deviation", farm_stats["std"], yield_stats["std"]],
            ["Variance", farm_stats["var"], yield_stats["var"]],

            ["Min", farm_stats["min"], yield_stats["min"]],
            ["Max", farm_stats["max"], yield_stats["max"]],

            ["Range", farm_stats["range"], yield_stats["range"]],
            ["Coefficient of Variation (%)", farm_stats["cv"], yield_stats["cv"]],
        ]

        adv_table = Table(advanced_data, colWidths=[180, 180, 180])

        adv_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#006622")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ]))

        elements.append(adv_table)

        # =========================
        # INTERPRETATION (AI-LIKE INSIGHT)
        # =========================

        elements.append(Spacer(1, 10))
        elements.append(Paragraph(" Interpretation", styles["Heading3"]))

        interpretation = ""

        if farm_stats["cv"] < 10:
            interpretation += "• Farm data is highly consistent (low variability).<br/>"
        elif farm_stats["cv"] < 30:
            interpretation += "• Farm data shows moderate variability.<br/>"
        else:
            interpretation += "• Farm data is highly variable (unstable farm sizes).<br/>"

        if yield_stats["mean"] > farm_stats["mean"]:
            interpretation += "• Yield performance is strong relative to farm size.<br/>"
        else:
            interpretation += "• Yield efficiency may need improvement.<br/>"

        if yield_stats["std"] > yield_stats["mean"] * 0.5:
            interpretation += "• Yield is unstable and inconsistent across farms.<br/>"

        elements.append(
            Paragraph(interpretation, styles["BodyText"])
        )

    else:
        elements.append(
            Paragraph("No sufficient data for advanced analysis.", styles["BodyText"])
        )

    elements.append(Spacer(1, 20))

    # =========================
    # INSIGHTS SECTION
    # =========================
    elements.append(Paragraph(" Insights & Recommendations", styles["Heading2"]))

    insights_list = []

    # =========================
    # MOST COMMON PEST
    # =========================
    if not df_pests.empty:
        most_common_pest = df_pests["Pest Type"].mode()[0]

        insights_list.append(
            f"Monitor '{most_common_pest}' as it is the most frequently occurring pest in the system."
        )

    # =========================
    # YIELD PERFORMANCE
    # =========================
    if not df_farms.empty:
        avg_yield = df_farms["Yield"].mean()
        std_yield = df_farms["Yield"].std()

        if std_yield > avg_yield * 0.3:
            insights_list.append(
                "Yield variation is high across farms. Standardize farming practices to improve consistency."
            )
        else:
            insights_list.append(
                "Yield levels are relatively stable across farms."
            )

    # =========================
    # FARM SIZE vs YIELD RELATIONSHIP
    # =========================
    if corr is not None:
        if corr > 0.6:
            insights_list.append(
                "Strong positive relationship between farm size and yield. Larger farms tend to be more productive."
            )
        elif corr > 0.3:
            insights_list.append(
                "Moderate relationship between farm size and yield."
            )
        else:
            insights_list.append(
                "Weak relationship between farm size and yield. Farm size is not a strong predictor of yield."
            )

    # =========================
    # SOIL / GENERAL RECOMMENDATION (DATA-BASED RULE)
    # =========================
    if not df_farms.empty:
        low_yield_ratio = (df_farms["Yield"] < df_farms["Yield"].mean()).mean()

        if low_yield_ratio > 0.5:
            insights_list.append(
                "More than half of farms are below average yield. Improve soil management and fertilizer practices."
            )

    # =========================
    # FINAL OUTPUT (HTML FORMAT FOR STREAMLIT)
    # =========================
    insights = "<br/>".join([f"• {i}" for i in insights_list])

    elements.append(Paragraph(insights, styles["BodyText"]))
    elements.append(Spacer(1, 20))

    # =========================
    # FOOTER
    # =========================
    elements.append(
        Paragraph(
            "Generated by Abaca Farming Management System © 2026",
            styles["Italic"]
        )
    )

    # =========================
    # BUILD PDF
    # =========================
    doc.build(elements)

    buffer.seek(0)
    return buffer


def generate_excel():
    output = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"

    ws.append(["Metric", "Value"])
    ws.append(["Farmers", len(filtered_farmers)])
    ws.append(["Farms", len(filtered_farms)])
    ws.append(["Avg Yield", avg_yield])
    ws.append(["Pests", len(filtered_pests)])

    wb.save(output)
    output.seek(0)
    return output

# =========================
# DOWNLOAD BUTTONS
# =========================
st.markdown("---")

d1, d2 = st.columns(2)

with d1:
    st.download_button(
        "Download PDF",
        data=generate_pdf(corr, filtered_farms, filtered_pests, filtered_farmers),
        file_name="abaca_report.pdf",
        mime="application/pdf"
    )

with d2:
    st.download_button(
        "Download Excel",
        data=generate_excel(),
        file_name="abaca_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
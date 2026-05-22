import streamlit as st
from database import session, Farm, AbacaCultivation, Farmer
from sqlalchemy import or_, func
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Cultivation",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
    font-family: 'Segoe UI', sans-serif;
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

/* SIDEBAR BUTTONS */
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

/* =========================
   PAGE TITLE
========================= */
.page-title {
    font-size: 37px;
    font-weight: 800;
    color: #006622;
    text-align: center;
}

.page-subtitle {
    font-size: 15px;
    color: #666;
}

/* =========================
   TABLE CONTAINER
========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border-radius: 20px !important;
    padding: 25px !important;
}

/* =========================
   SEARCH
========================= */
.search-wrapper {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.search-box {
    position: relative;
    width: 250px;
}

.search-box .search-icon {
    position: absolute;
    left: 12px;
    top: 11px;
    font-size: 14px;
    color: #888;
    z-index: 999;
    pointer-events: none;
}

.search-box input {
    width: 100% !important;
    height: 38px !important;
    padding-left: 35px !important;
    border-radius: 10px !important;
    border: 1px solid #d9d9d9 !important;
    font-size: 13px !important;
    background-color: white !important;
}

/* =========================
   TABLE HEADER
========================= */
.table-header {
    font-size: 15px;
    font-weight: 700;
    color: #333;
}

/* =========================
   ACTION BUTTONS
========================= */
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

div[data-testid="stFileUploader"] small {
    display: none !important;
}

div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInstructions"] {
    display: none !important;
}

/* Optional: remove extra spacing */
div[data-testid="stFileUploader"] section {
    padding: 0 !important;
    border: none !important;
    padding-top: 15px !important;
}

/* Tooltip on hover */
div[data-testid="stFileUploader"] button {
    background-color: #006622 !important;  /* GREEN */
    color: white !important;
}

/* Hover tooltip */
div[data-testid="stFileUploader"] button:hover::after {
    content: "Upload Excel file (.xlsx) — Max 200MB";
    position: absolute;
    top: -35px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #006622 !important;  /* GREEN */
    color: white;
    padding: 5px 10px;
    font-size: 11px;
    border-radius: 6px;
    white-space: nowrap;
    z-index: 9999;
}

</style>
""", unsafe_allow_html=True)

# =========================
# AUTH CHECK
# =========================
if not st.session_state.get("logged_in"):
    st.warning("Login first")
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

# =========================
# ADD CULTIVATION DIALOG
# =========================
@st.dialog("➕ Add Cultivation Record")
def add_cultivation_dialog():

    farmers = session.query(Farmer).all()

    farmer_map = {
        f.id: f"{f.firstname} {f.middlename[0] + '.' if f.middlename else ''} {f.lastname}"
        for f in farmers
    }
    farms = session.query(Farm).all()

    with st.form("add_cultivation_form"):

        farm = st.selectbox(
            "Farm",
            farms,
            format_func=lambda x: f"Farm #{x.id} - {farmer_map.get(x.farmer_id, 'Unknown Farmer')}"
        )

        year_first = st.number_input(
            "Year First Planted",
            1900,
            2100
        )

        abaca_area = st.number_input(
            "Abaca Area",
            0.0,
            format="%.2f"
        )

        variety = st.selectbox(
            "Variety",
            ["Tanggongon", "Tinawagan Pula", "Linawaan", "Inosa", "La Filipe", "Bongolanon", "Enusa"]
        )

        planting_distance = st.text_input("Planting Distance (meters)")
        planting_method = st.text_input("Planting Method")

        intercropping = st.selectbox(
            "Intercropping",
            ["Yes", "No"]
        )

        intercrop_crops = st.text_input("Intercrop Crops")

        submitted = st.form_submit_button("Save")

        if submitted:

            record = AbacaCultivation(
                farm_id=farm.id,
                year_first_planted=year_first,
                abaca_area=abaca_area,
                variety=variety,
                planting_distance=planting_distance,
                planting_method=planting_method,
                intercropping=intercropping,
                intercrop_crops=intercrop_crops
            )

            session.add(record)
            session.commit()

            st.success("Added successfully!")
            st.rerun()

# =========================
# VIEW DIALOG
# =========================
@st.dialog("👁 Cultivation Details")
def view_cultivation_dialog(record_id):

    record = session.query(
        AbacaCultivation
    ).filter_by(id=record_id).first()

    st.markdown("### Cultivation Information")

    st.write(f"**Variety:** {record.variety}")
    st.write(f"**Abaca Area:** {record.abaca_area}")
    st.write(f"**Planting Method:** {record.planting_method}")
    st.write(f"**Planting Distance (Meters):** {record.planting_distance}")
    st.write(f"**Intercropping:** {record.intercropping}")
    st.write(f"**Intercrop Crops:** {record.intercrop_crops}")
    st.write(f"**Year First Planted:** {record.year_first_planted}")

    st.markdown("---")

    if st.button("❌ Close"):
        st.rerun()

# =========================
# EDIT DIALOG
# =========================
@st.dialog("✏ Edit Cultivation")
def edit_cultivation_dialog(record_id):

    record = session.query(
        AbacaCultivation
    ).filter_by(id=record_id).first()

    with st.form("edit_form"):

        variety = st.selectbox(
            "Variety",
            ["Tanggongon", "Tinawagan Pula", "Linawaan", "Inosa", "La Filipe", "Bongolanon", "Enusa"],
            index=["Tanggongon", "Tinawagan Pula", "Linawaan", "Inosa", "La Filipe", "Bongolanon", "Enusa"].index(record.variety) if record.variety in ["Tanggongon", "Tinawagan Pula", "Linawaan", "Inosa", "La Filipe", "Bongolanon", "Enusa"] else 0
        )

        abaca_area = st.number_input(
            "Abaca Area",
            value=float(record.abaca_area)
        )

        planting_distance = st.text_input(
            "Planting Distance (meters)",
            value=record.planting_distance or ""
        )

        planting_method = st.text_input(
            "Planting Method",
            value=record.planting_method or ""
        )

        intercropping = st.text_input(
            "Intercropping",
            value=record.intercropping or ""
        )

        intercrop_crops = st.text_input(
            "Intercrop Crops",
            value=record.intercrop_crops or ""
        )

        update = st.form_submit_button("Update")

        if update:

            record.variety = variety
            record.abaca_area = abaca_area
            record.planting_distance = planting_distance
            record.planting_method = planting_method
            record.intercropping = intercropping
            record.intercrop_crops = intercrop_crops

            session.commit()

            st.success("Updated!")
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_cultivation_dialog(record_id):

    record = session.query(
        AbacaCultivation
    ).filter_by(id=record_id).first()

    st.warning(
        f"Delete '{record.variety}'?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancel"):
            st.rerun()

    with col2:
        if st.button("🗑 Yes Delete"):

            session.delete(record)
            session.commit()

            st.success("Deleted!")
            st.rerun()

# =========================
# HEADER
# =========================
col1, col2 = st.columns([8, 1.5])

with col1:

    st.markdown("""
    <div class="page-title">
        Abaca Cultivation
    </div>

    <div class="page-subtitle">
        Manage plantation records
    </div>
    """, unsafe_allow_html=True)

with col2:

    with st.popover(f"👤 {st.session_state.get('user', 'Farmer')}"):

        st.markdown("### Account")

        st.write(
            f"User: {st.session_state.get('user', 'Farmer')}"
        )

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.switch_page("app.py")

# =========================
# SEARCH + ADD
# =========================
search_col, action_col, upload_col = st.columns([0.8, 0.1, 0.1], gap="small")

with search_col:

    st.markdown("""
    <div class="search-wrapper">
        <div class="search-box">
    """, unsafe_allow_html=True)

    search = st.text_input(
        "",
        placeholder="Search cultivation...",
        label_visibility="collapsed"
    )

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

with action_col:
    st.markdown("")

    if st.button("Add Record"):
        add_cultivation_dialog()

with upload_col:

    uploaded_file = st.file_uploader(
        "",
        type=["xlsx"],
        label_visibility="collapsed",
        key="cultivation_upload"
    )

    # =========================
    # STEP 1: READ FILE ONLY
    # =========================
    if uploaded_file is not None:

        try:
            df = pd.read_excel(uploaded_file)

            # CLEAN HEADERS
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.replace("/", "_")
                .str.replace("-", "_")
            )

            # OPTIONAL rename if Excel uses First Name format
            rename_map = {
                "first_name": "firstname",
                "middle_name": "middlename",
                "last_name": "lastname",
            }

            df = df.rename(columns=rename_map)

            # REQUIRED COLUMNS
            required_columns = [
                "firstname",
                "lastname",
                "year_first_planted",
                "abaca_area",
                "variety",
                "planting_distance",
                "planting_method",
                "intercropping",
                "intercrop_crops"
            ]

            missing = [c for c in required_columns if c not in df.columns]

            if missing:
                st.error(f"Missing columns: {missing}")
                st.stop()

            st.session_state.cultivation_df = df
            st.success("File ready for import!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # =========================
    # STEP 2: IMPORT BUTTON
    # =========================
        if st.button("Import Cultivation", key="import_cultivation_btn"):

            df = st.session_state.cultivation_df

            inserted = 0
            skipped = 0
            total = len(df)

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():

                try:
                    status.text(f"Processing {i+1}/{total}...")

                    fname = str(row["firstname"]).strip()
                    lname = str(row["lastname"]).strip()

                    # =========================
                    # FIND FARMER (SAFE MATCH)
                    # =========================
                    farmer = session.query(Farmer).filter(
                        func.lower(Farmer.firstname) == fname.lower(),
                        func.lower(Farmer.lastname) == lname.lower()
                    ).first()

                    if not farmer:
                        skipped += 1
                        continue

                    # =========================
                    # FIND FARM (by farmer_id)
                    # =========================
                    farm = session.query(Farm).filter_by(
                        farmer_id=farmer.id
                    ).first()

                    if not farm:
                        skipped += 1
                        continue

                    # =========================
                    # CREATE CULTIVATION RECORD
                    # =========================
                    record = AbacaCultivation(
                        farm_id=farm.id,
                        year_first_planted=int(row["year_first_planted"] or 0),
                        abaca_area=float(row["abaca_area"] or 0),
                        variety=str(row["variety"] or ""),
                        planting_distance=str(row["planting_distance"] or ""),
                        planting_method=str(row["planting_method"] or ""),
                        intercropping=str(row["intercropping"] or ""),
                        intercrop_crops=str(row["intercrop_crops"] or "")
                    )

                    session.add(record)
                    inserted += 1

                except Exception as e:
                    skipped += 1
                    st.warning(f"Row {i+1} skipped: {e}")

                progress.progress((i + 1) / total)

            session.commit()

            st.success(f"Inserted: {inserted} | Skipped: {skipped}")

            # RESET
            del st.session_state["cultivation_df"]
            st.rerun()

# =========================
# FETCH DATA
# =========================
query = session.query(AbacaCultivation)

if search:

    search_term = f"%{search}%"

    query = query.filter(
        or_(
            AbacaCultivation.variety.ilike(search_term),
            AbacaCultivation.planting_method.ilike(search_term),
            AbacaCultivation.planting_distance.ilike(search_term),
            AbacaCultivation.intercropping.ilike(search_term),
            AbacaCultivation.intercrop_crops.ilike(search_term),
        )
    )

records = query.all()

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4 = st.columns(
        [3, 2, 2, 2, 2]
    )

    h0.markdown("<div class='table-header'>Variety</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Abaca Area</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Planting Method</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Year Planted</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not records:
        st.info("No cultivation records found.")

    for r in records:

        c0, c1, c2, c3, c4 = st.columns(
            [3, 2, 2, 2, 2]
        )

        c0.write(f"{r.variety}")
        c1.write(f"{r.abaca_area}")
        c2.write(f"{r.planting_method}")
        c3.write(f"{r.year_first_planted}")

        with c4:

            b1, b2, b3 = st.columns(3)

            with b1:

                st.markdown('<div class="view-btn">', unsafe_allow_html=True)

                if st.button("👁", key=f"view_{r.id}"):
                    view_cultivation_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b2:

                st.markdown('<div class="edit-btn">', unsafe_allow_html=True)

                if st.button("✏", key=f"edit_{r.id}"):
                    edit_cultivation_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b3:

                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)

                if st.button("🗑", key=f"delete_{r.id}"):
                    delete_cultivation_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from sqlalchemy import or_, func
from database import session, Farm, SoilManagement, Farmer
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Soil Management",
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
    background: linear-gradient(135deg, #006622, #1f6f4a, #468767) !important;th: 270px;
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

.search-box input {
    width: 100% !important;
    height: 38px !important;
    padding-left: 15px !important;
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

/* INPUTS */
input, textarea {
    border-radius: 10px !important;
}

/* DIALOG */
[data-testid="stDialog"] {
    border-radius: 20px !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 12px !important;
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
# ADD DIALOG
# =========================
@st.dialog("➕ Add Soil Record")
def add_soil_dialog():
    farmers = session.query(Farmer).all()

    farmer_map = {
        f.id: f"{f.firstname} {f.middlename[0] + '.' if f.middlename else ''} {f.lastname}"
        for f in farmers
    }
    farms = session.query(Farm).all()

    with st.form("add_soil_form"):

        farm = st.selectbox(
            "Farm",
            farms,
            format_func=lambda x: f"Farm #{x.id} - {farmer_map.get(x.farmer_id, 'Unknown Farmer')}"
        )

        soil_testing = st.text_input("Soil Testing")
        testing_frequency = st.text_input("Testing Frequency")
        fertility_improvement = st.text_input("Fertility Improvement")
        soil_conservation = st.text_input("Soil Conservation")
        conservation_techniques = st.text_input("Conservation Techniques")
        seasonal_effects = st.text_input("Seasonal Effects")

        submitted = st.form_submit_button("Save")

        if submitted:

            soil = SoilManagement(
                farm_id=farm.id,
                soil_testing=soil_testing,
                testing_frequency=testing_frequency,
                fertility_improvement=fertility_improvement,
                soil_conservation=soil_conservation,
                conservation_techniques=conservation_techniques,
                seasonal_effects=seasonal_effects
            )

            session.add(soil)
            session.commit()

            st.success("Added successfully!")
            st.rerun()

# =========================
# VIEW DIALOG
# =========================
@st.dialog("👁 Soil Details")
def view_soil_dialog(record_id):

    record = session.query(
        SoilManagement
    ).filter_by(id=record_id).first()

    st.markdown("### Soil Information")

    st.write(f"**Soil Testing:** {record.soil_testing}")
    st.write(f"**Testing Frequency:** {record.testing_frequency}")
    st.write(f"**Fertility Improvement:** {record.fertility_improvement}")
    st.write(f"**Soil Conservation:** {record.soil_conservation}")
    st.write(f"**Conservation Techniques:** {record.conservation_techniques}")
    st.write(f"**Seasonal Effects:** {record.seasonal_effects}")

    st.markdown("---")

    if st.button("❌ Close"):
        st.rerun()

# =========================
# EDIT DIALOG
# =========================
@st.dialog("✏ Edit Soil Record")
def edit_soil_dialog(record_id):

    record = session.query(
        SoilManagement
    ).filter_by(id=record_id).first()

    with st.form("edit_soil_form"):

        soil_testing = st.text_input(
            "Soil Testing",
            value=record.soil_testing
        )

        testing_frequency = st.text_input(
            "Testing Frequency",
            value=record.testing_frequency
        )

        fertility_improvement = st.text_input(
            "Fertility Improvement",
            value=record.fertility_improvement
        )

        soil_conservation = st.text_input(
            "Soil Conservation",
            value=record.soil_conservation
        )

        conservation_techniques = st.text_input(
            "Conservation Techniques",
            value=record.conservation_techniques
        )

        seasonal_effects = st.text_input(
            "Seasonal Effects",
            value=record.seasonal_effects
        )

        update = st.form_submit_button("Update")

        if update:

            record.soil_testing = soil_testing
            record.testing_frequency = testing_frequency
            record.fertility_improvement = fertility_improvement
            record.soil_conservation = soil_conservation
            record.conservation_techniques = conservation_techniques
            record.seasonal_effects = seasonal_effects

            session.commit()

            st.success("Updated successfully!")
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_soil_dialog(record_id):

    record = session.query(
        SoilManagement
    ).filter_by(id=record_id).first()

    st.warning(
        f"Delete '{record.soil_testing}'?"
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
        Soil Management
    </div>

    <div class="page-subtitle">
        Monitor soil quality and conservation
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
        placeholder="Search soil management...",
        label_visibility="collapsed"
    )

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

with action_col:

    st.markdown("")

    if st.button("Add Record"):
        add_soil_dialog()

with upload_col:

    uploaded_file = st.file_uploader(
        "",
        type=["xlsx"],
        label_visibility="collapsed",
        key="soil_management_upload"
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

            required_columns = [
                "first_name", "middle_name", "last_name",
                "soil_testing",
                "testing_frequency",
                "fertility_improvement",
                "soil_conservation",
                "conservation_techniques",
                "seasonal_effects"
            ]

            missing = [c for c in required_columns if c not in df.columns]

            if missing:
                st.error(f"Missing columns: {missing}")
                st.stop()

            st.session_state.soil_df = df
            st.success("File ready for import!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # =========================
    # STEP 2: IMPORT BUTTON
    # =========================
        if st.button("Import Soil Records", key="import_soil_btn"):

            df = st.session_state.soil_df

            inserted = 0
            skipped = 0
            total = len(df)

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():

                try:
                    status.text(f"Processing {i+1}/{total}...")

                    fname = str(row["first_name"]).strip().lower()
                    mname = str(row["middle_name"]).strip().lower()
                    lname = str(row["last_name"]).strip().lower()

                    # FIND FARMER
                    farmer = session.query(Farmer).filter(
                        func.lower(Farmer.firstname) == fname,
                        func.lower(Farmer.lastname) == lname
                    ).first()

                    if not farmer:
                        skipped += 1
                        continue

                    # FIND FARM (IMPORTANT: SoilManagement uses farm_id)
                    farm = session.query(Farm).filter_by(
                        farmer_id=farmer.id
                    ).first()

                    if not farm:
                        skipped += 1
                        continue

                    soil = SoilManagement(
                        farm_id=farm.id,
                        soil_testing=row["soil_testing"],
                        testing_frequency=row["testing_frequency"],
                        fertility_improvement=row["fertility_improvement"],
                        soil_conservation=row["soil_conservation"],
                        conservation_techniques=row["conservation_techniques"],
                        seasonal_effects=row["seasonal_effects"]
                    )

                    session.add(soil)
                    inserted += 1

                except Exception as e:
                    skipped += 1
                    st.warning(f"Row {i+1} skipped: {e}")

                progress.progress((i + 1) / total)

            session.commit()

            st.success(f"Inserted: {inserted} | Skipped: {skipped}")

            del st.session_state["soil_df"]
            st.rerun()

# =========================
# FETCH DATA
# =========================
query = session.query(SoilManagement)

if search:

    search_term = f"%{search}%"

    query = query.filter(
        or_(
            SoilManagement.soil_testing.ilike(search_term),
            SoilManagement.testing_frequency.ilike(search_term),
            SoilManagement.soil_conservation.ilike(search_term),
            SoilManagement.conservation_techniques.ilike(search_term),
            SoilManagement.seasonal_effects.ilike(search_term),
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

    h0.markdown(
        "<div class='table-header'>Soil Testing</div>",
        unsafe_allow_html=True
    )

    h1.markdown(
        "<div class='table-header'>Frequency</div>",
        unsafe_allow_html=True
    )

    h2.markdown(
        "<div class='table-header'>Conservation</div>",
        unsafe_allow_html=True
    )

    h3.markdown(
        "<div class='table-header'>Seasonal Effects</div>",
        unsafe_allow_html=True
    )

    h4.markdown(
        "<div class='table-header'>Actions</div>",
        unsafe_allow_html=True
    )

    st.divider()

    if not records:
        st.info("No soil records found.")

    for r in records:

        c0, c1, c2, c3, c4 = st.columns(
            [3, 2, 2, 2, 2]
        )

        c0.write(f"{r.soil_testing}")
        c1.write(f"{r.testing_frequency}")
        c2.write(f"{r.soil_conservation}")
        c3.write(f"{r.seasonal_effects}")

        with c4:

            b1, b2, b3 = st.columns(3)

            with b1:

                if st.button("👁", key=f"view_{r.id}"):
                    view_soil_dialog(r.id)

            with b2:

                if st.button("✏", key=f"edit_{r.id}"):
                    edit_soil_dialog(r.id)

            with b3:

                if st.button("🗑", key=f"delete_{r.id}"):
                    delete_soil_dialog(r.id)
import streamlit as st
from sqlalchemy import or_, func
from database import session, Farm, SoilManagement, Farmer, SoilTesting, TestingFrequency, SoilConservation, ConservationTechniques, SeasonalEffects
import pandas as pd
from utils.ui import hide_streamlit_ui
from utils.sidebar import render_sidebar
from utils.ui import apply_global_css
from utils.header import render_header
from auth import has_permission

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Soil Management",
    layout="wide"
)

hide_streamlit_ui()
render_sidebar() # Render custom sidebar with navigation links
apply_global_css() # Apply global CSS for consistent styling
render_header() # Render consistent header across pages

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
   PAGE TITLE
========================= */
.page-title {
    font-size: 37px;
    font-weight: 800;
    color: #006622;
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

def rf_select(label, model):
    options = session.query(model).all()

    mapping = {
        f"{o.code} - {o.description}": o.id
        for o in options
    }

    selected = st.selectbox(label, list(mapping.keys()))
    return mapping[selected]


def get_rf_id(model, value):
    if not value:
        return None

    obj = session.query(model).filter(
        model.description.ilike(str(value).strip())
    ).first()

    return obj.id if obj else None

# =========================
# ADD DIALOG
# =========================
@st.dialog("➕ Add Soil Record")
def add_soil_dialog():
    farmers = session.query(Farmer).all()
    farms = session.query(Farm).all()
    soil_testings = session.query(SoilTesting).all()
    testing_frequencies = session.query(TestingFrequency).all()
    soil_conservations = session.query(SoilConservation).all()
    conservation_techniques = session.query(ConservationTechniques).all()
    seasonal_effects = session.query(SeasonalEffects).all()

    farmer_map = {
        f.id: f"{f.firstname} {f.middlename[0] + '.' if f.middlename else ''} {f.lastname}"
        for f in farmers
    }

    with st.form("add_soil_form"):

        farm = st.selectbox(
            "Farm",
            farms,
            format_func=lambda x: f"Farm #{x.id} - {farmer_map.get(x.farmer_id, 'Unknown Farmer')}"
        )

        soil_testing = st.selectbox(
            "Soil Testing",
            soil_testings,
            format_func=lambda x: f"{x.description}"
        )

        testing_frequency = st.selectbox(
            "Testing Frequency",
            testing_frequencies,
            format_func=lambda x: f"{x.description}"
        )

        fertility_improvement = st.text_input("Fertility Improvement")

        soil_conservation = st.selectbox(
            "Soil Conservation",
            soil_conservations,
            format_func=lambda x: f"{x.description}"
        )
        
        conservation_technique = st.selectbox(
            "Conservation Techniques",
            conservation_techniques,
            format_func=lambda x: f"{x.description}"
        )

        seasonal_effect = st.selectbox(
            "Seasonal Effects",
            seasonal_effects,
            format_func=lambda x: f"{x.description}"
        )

        submitted = st.form_submit_button("Save")

        if submitted:

            soil = SoilManagement(
                farm_id=farm.id,
                soil_testing_id=soil_testing.id,
                testing_frequency_id=testing_frequency.id,
                fertility_improvement=fertility_improvement,
                soil_conservation_id=soil_conservation.id,
                conservation_techniques_id=conservation_technique.id,
                seasonal_effects_id=seasonal_effect.id
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

    soil_testing = session.query(SoilTesting).filter_by(
        id=record.soil_testing_id
    ).first()

    testing_frequency = session.query(TestingFrequency).filter_by(
        id=record.testing_frequency_id
    ).first()

    soil_conservation = session.query(SoilConservation).filter_by(
        id=record.soil_conservation_id
    ).first()

    conservation_technique = session.query(ConservationTechniques).filter_by(
        id=record.conservation_techniques_id
    ).first()

    seasonal_effect = session.query(SeasonalEffects).filter_by(
        id=record.seasonal_effects_id
    ).first()

    st.markdown("### Soil Information")

    st.write(f"**Soil Testing:** {soil_testing.description}")
    st.write(f"**Testing Frequency:** {testing_frequency.description}")
    st.write(f"**Fertility Improvement:** {record.fertility_improvement}")
    st.write(f"**Soil Conservation:** {soil_conservation.description}")
    st.write(f"**Conservation Techniques:** {conservation_technique.description}")
    st.write(f"**Seasonal Effects:** {seasonal_effect.description}")

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

    farmers = session.query(Farmer).all()
    farms = session.query(Farm).all()
    soil_testings = session.query(SoilTesting).all()
    testing_frequencies = session.query(TestingFrequency).all()
    soil_conservations = session.query(SoilConservation).all()
    conservation_techniques = session.query(ConservationTechniques).all()
    seasonal_effects = session.query(SeasonalEffects).all()

    selected_farm = session.get(
        Farm, record.farm_id
    )

    selected_soil_testing = session.get(
        SoilTesting, record.soil_testing_id
    )

    selected_testing_frequency = session.get(
        TestingFrequency, record.testing_frequency_id
    )

    selected_soil_conservation = session.get(
        SoilConservation, record.soil_conservation_id
    )

    selected_conservation_technique = session.get(
        ConservationTechniques, record.conservation_techniques_id
    )

    selected_seasonal_effect = session.get(
        SeasonalEffects, record.seasonal_effects_id
    )

    with st.form("edit_soil_form"):

        farm = st.selectbox(
            "Farm",
            farms,
            format_func=lambda x: (
                f"{session.get(Farmer, x.farmer_id).firstname} "
                f"{session.get(Farmer, x.farmer_id).middlename} "
                f"{session.get(Farmer, x.farmer_id).lastname} "
                f"(Farm #{x.id})"
            ),
            index=farms.index(selected_farm)
            if selected_farm in farms else 0
        )

        soil_testing = st.selectbox(
            "Soil Testing",
            soil_testings,
            format_func=lambda x: f"{x.description}",
            index=soil_testings.index(selected_soil_testing)
            if selected_soil_testing in soil_testings else 0
        )

        testing_frequency = st.selectbox(
            "Testing Frequency",
            testing_frequencies,
            format_func=lambda x: f"{x.description}",
            index=testing_frequencies.index(selected_testing_frequency)
            if selected_testing_frequency in testing_frequencies else 0
        )

        fertility_improvement = st.text_input(
            "Fertility Improvement",
            value=record.fertility_improvement
        )

        soil_conservation = st.selectbox(
            "Soil Conservation",
            soil_conservations,
            format_func=lambda x: f"{x.description}",
            index=soil_conservations.index(selected_soil_conservation)
            if selected_soil_conservation in soil_conservations else 0
        )

        conservation_technique = st.selectbox(
            "Conservation Techniques",
            conservation_techniques,
            format_func=lambda x: f"{x.description}",
            index=conservation_techniques.index(selected_conservation_technique)
            if selected_conservation_technique in conservation_techniques else 0
        )

        seasonal_effect = st.selectbox(
            "Seasonal Effects",
            seasonal_effects,
            format_func=lambda x: f"{x.description}",
            index=seasonal_effects.index(selected_seasonal_effect)
            if selected_seasonal_effect in seasonal_effects else 0
        )

        update = st.form_submit_button("Update")

        if update:
            record.farm_id = farm.id
            record.soil_testing_id = soil_testing.id
            record.testing_frequency_id = testing_frequency.id
            record.fertility_improvement = fertility_improvement
            record.soil_conservation_id = soil_conservation.id
            record.conservation_techniques_id = conservation_technique.id
            record.seasonal_effects_id = seasonal_effect.id

            session.commit()

            st.success("Updated successfully!")
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_soil_dialog(record_id):

    record = session.get(SoilManagement, record_id)

    farm = session.get(Farm, record.farm_id)
    farmer = session.get(Farmer, farm.farmer_id)
    soil_testing = session.get(SoilTesting, record.soil_testing_id)

    st.warning(
        f"Delete soil management record for "
        f"{farmer.firstname} {farmer.lastname} "
        f"({soil_testing.description})?"
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

                    # =========================
                    # LOOKUPS
                    # =========================
                    soil_testing_id = get_rf_id(SoilTesting, row["soil_testing"])
                    testing_frequency_id = get_rf_id(TestingFrequency, row["testing_frequency"])
                    soil_conservation_id = get_rf_id(SoilConservation, row["soil_conservation"])
                    conservation_techniques_id = get_rf_id(ConservationTechniques, row["conservation_techniques"])
                    seasonal_effects_id = get_rf_id(SeasonalEffects, row["seasonal_effects"])

                    # =========================
                    # SKIP IF REQUIRED LOOKUPS FAIL
                    # =========================
                    if (
                        soil_testing_id is None
                        or testing_frequency_id is None
                        or soil_conservation_id is None
                        or conservation_techniques_id is None
                        or seasonal_effects_id is None
                    ):
                        skipped += 1
                        continue

                    soil = SoilManagement(
                        farm_id=farm.id,
                        soil_testing_id=soil_testing_id,
                        testing_frequency_id=testing_frequency_id,
                        fertility_improvement=str(row["fertility_improvement"] or ""),
                        soil_conservation_id=soil_conservation_id,
                        conservation_techniques_id=conservation_techniques_id,
                        seasonal_effects_id=seasonal_effects_id
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
# PAGINATION
# =========================
ROWS_PER_PAGE = 10

total_rows = len(records)
total_pages = max((total_rows - 1) // ROWS_PER_PAGE + 1, 1)

if "soil_page" not in st.session_state:
    st.session_state.soil_page = 1

# Keep current page valid
if st.session_state.soil_page > total_pages:
    st.session_state.soil_page = total_pages

if st.session_state.soil_page < 1:
    st.session_state.soil_page = 1

start_idx = (st.session_state.soil_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

paginated_soils = records[start_idx:end_idx]

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5, h6 = st.columns(
        [1, 3, 3, 2, 2, 2, 2]
    )

    h0.markdown("<div class='table-header'>#</div>", unsafe_allow_html=True)

    h1.markdown(
        "<div class='table-header'>Farmer</div>",
        unsafe_allow_html=True
    )

    h2.markdown(
        "<div class='table-header'>Soil Testing</div>",
        unsafe_allow_html=True
    )

    h3.markdown(
        "<div class='table-header'>Frequency</div>",
        unsafe_allow_html=True
    )

    h4.markdown(
        "<div class='table-header'>Conservation</div>",
        unsafe_allow_html=True
    )

    h5.markdown(
        "<div class='table-header'>Seasonal Effects</div>",
        unsafe_allow_html=True
    )

    h6.markdown(
        "<div class='table-header'>Actions</div>",
        unsafe_allow_html=True
    )

    st.divider()

    if not records:
        st.info("No soil records found.")

    for i, r in enumerate(paginated_soils, start=start_idx + 1):

        farm = session.query(Farm).filter_by(
            id=r.farm_id
        ).first()

        farmer = session.query(Farmer).filter_by(
            id=farm.farmer_id
        ).first()

        soil_testing = session.query(SoilTesting).filter_by(
            id=r.soil_testing_id
        ).first()

        testing_frequency = session.query(TestingFrequency).filter_by(
            id=r.testing_frequency_id
        ).first()

        soil_conservation = session.query(SoilConservation).filter_by(
            id=r.soil_conservation_id
        ).first()

        conservation_technique = session.query(ConservationTechniques).filter_by(
            id=r.conservation_techniques_id
        ).first()

        seasonal_effect = session.query(SeasonalEffects).filter_by(
            id=r.seasonal_effects_id
        ).first()

        c0, c1, c2, c3, c4, c5, c6 = st.columns(
            [1, 3, 3, 2, 2, 2, 2]
        )

        c0.write(i)
        c1.write(
            f"{farmer.firstname} "
            f"{farmer.middlename[0] + '.' if farmer.middlename else ''} "
            f"{farmer.lastname}"
        )
        c2.write(f"{soil_testing.description}")
        c3.write(f"{testing_frequency.description}")
        c4.write(f"{soil_conservation.description}")
        c5.write(f"{seasonal_effect.description}")

        with c6:

            b1, b2, b3 = st.columns(3)

            with b1:

                if st.button("👁", key=f"view_{r.id}"):
                    view_soil_dialog(r.id)

            with b2:

                if st.button("✏", key=f"edit_{r.id}"):
                    edit_soil_dialog(r.id)

            with b3:
                if has_permission("delete"):
                    if st.button("🗑", key=f"delete_{r.id}"):
                        delete_soil_dialog(r.id)

# =========================
# PAGINATION CONTROLS
# =========================
if total_rows > 0:

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns([.04, .08, .9])

    with p1:
        if st.button(
            "⬅",
            disabled=st.session_state.soil_page == 1,
            use_container_width=False
        ):
            st.session_state.soil_page -= 1
            st.rerun()

    with p2:
        st.markdown(
            f"""
            <div style="
                font-size:12px;
                color:gray;
                text-align:left;
                padding-top:6px;
            ">
                Page <b>{st.session_state.soil_page}</b> / {total_pages}
                &nbsp;|&nbsp;
                {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        if st.button(
            "➡",
            disabled=st.session_state.soil_page == total_pages,
            use_container_width=False
        ):
            st.session_state.soil_page += 1
            st.rerun()
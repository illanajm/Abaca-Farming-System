import streamlit as st
import pandas as pd
from sqlalchemy import or_, func, cast, String
from datetime import datetime
from database import session, Farmer, Farm, SoilQuality, SoilType, IrrigationSource, EnvironmentalFactor, AccessToInputs, InputSource
from auth import is_admin, has_permission
from utils.ui import hide_streamlit_ui
from utils.sidebar import render_sidebar
from utils.ui import apply_global_css
from utils.header import render_header

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Farms",
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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")
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
# ADD FARM DIALOG
# =========================
@st.dialog("➕ Add Farm")
def add_farm_dialog():

    farmers = session.query(Farmer).all()
    soil_qualities = session.query(SoilQuality).all()
    soil_types = session.query(SoilType).all()
    irrigation_sources = session.query(IrrigationSource).all()
    environmental_factors = session.query(EnvironmentalFactor).all()
    access_to_inputs = session.query(AccessToInputs).all()
    input_sources = session.query(InputSource).all()

    with st.form("add_farm_form"):

        farmer = st.selectbox(
            "Farmer",
            farmers,
            format_func=lambda x: f"{x.firstname} {x.middlename[0] + '.' if x.middlename else ''} {x.lastname}"
        )

        farm_area = st.number_input(
            "Farm Area (ha)",
            min_value=0.0
        )

        soil_quality = st.selectbox(
            "Soil Quality",
            soil_qualities,
            format_func=lambda x: f"{x.description}"
        )

        soil_type = st.selectbox(
            "Soil Type",
            soil_types,
            format_func=lambda x: f"{x.description}"
        )

        irrigation_source = st.selectbox(
            "Irrigation Source",
            irrigation_sources,
            format_func=lambda x: f"{x.description}"
        )

        environmental_factors = st.selectbox(
            "Environment Factors",
            environmental_factors,
            format_func=lambda x: f"{x.description}"
        )

        access_to_inputs = st.selectbox(
            "Access to Inputs",
            access_to_inputs,
            format_func=lambda x: f"{x.description}"
        )
        
        input_source = st.selectbox(
            "Input Source",
            input_sources,
            format_func=lambda x: f"{x.description}"
        )

        average_yield = st.number_input(
            "Average Yield (kg/year)",
            min_value=0.0
        )

        submitted = st.form_submit_button("Save")

        if submitted:

            farm = Farm(
                farmer_id=farmer.id,
                farm_area=farm_area,
                soil_quality_id=soil_quality.id,
                soil_type_id=soil_type.id,
                irrigation_source_id=irrigation_source.id,
                environmental_factor_id=environmental_factors.id,
                access_to_inputs_id=access_to_inputs.id,
                input_source_id=input_source.id,
                average_yield=average_yield
            )

            session.add(farm)
            session.commit()

            st.success("Farm added!")
            st.rerun()

# =========================
# EDIT FARM DIALOG
# =========================
@st.dialog("✏ Edit Farm")
def edit_farm_dialog(farm_id):

    farm = session.get(Farm, farm_id)

    # LOAD OPTIONS
    farmers = session.query(Farmer).all()
    soil_qualities = session.query(SoilQuality).all()
    soil_types = session.query(SoilType).all()
    irrigation_sources = session.query(IrrigationSource).all()
    environmental_factors = session.query(EnvironmentalFactor).all()
    access_to_inputs = session.query(AccessToInputs).all()
    input_sources = session.query(InputSource).all()

    selected_farmer = session.get(
        Farmer, farm.farmer_id
    )

    selected_soil_quality = session.get(
        SoilQuality, farm.soil_quality_id
    )

    selected_soil_type = session.get(
        SoilType, farm.soil_type_id
    )

    selected_irrigation_source = session.get(
        IrrigationSource, farm.irrigation_source_id
    )

    selected_environmental_factor = session.get(
        EnvironmentalFactor, farm.environmental_factor_id
    )

    selected_access_to_inputs = session.get(
        AccessToInputs, farm.access_to_inputs_id
    )

    selected_input_source = session.get(
        InputSource, farm.input_source_id
    )

    with st.form("edit_farm_form"):

        farmer = st.selectbox(
            "Farmer",
            farmers,
            format_func=lambda x: f"{x.firstname} {x.middlename} {x.lastname}",
            index=farmers.index(selected_farmer)
            if selected_farmer in farmers else 0
        )

        farm_area = st.number_input(
            "Farm Area (ha)",
            value=float(farm.farm_area or 0)
        )

        soil_quality = st.selectbox(
            "Soil Quality",
            soil_qualities,
            format_func=lambda x: f"{x.description}",
            index=soil_qualities.index(selected_soil_quality)
            if selected_soil_quality in soil_qualities else 0
        )

        soil_type = st.selectbox(
            "Soil Type",
            soil_types,
            format_func=lambda x: f"{x.description}",
            index=soil_types.index(selected_soil_type)
            if selected_soil_type in soil_types else 0
        )

        irrigation_source = st.selectbox(
            "Irrigation Source",
            irrigation_sources,
            format_func=lambda x: f"{x.description}",
            index=irrigation_sources.index(selected_irrigation_source)
            if selected_irrigation_source in irrigation_sources else 0
        )

        environmental_factor = st.selectbox(
            "Environmental Factor",
            environmental_factors,
            format_func=lambda x: f"{x.description}",
            index=environmental_factors.index(selected_environmental_factor)
            if selected_environmental_factor in environmental_factors else 0
        )

        access_to_input = st.selectbox(
            "Access to Inputs",
            access_to_inputs,
            format_func=lambda x: f"{x.description}",
            index=access_to_inputs.index(selected_access_to_inputs)
            if selected_access_to_inputs in access_to_inputs else 0
        )

        input_source = st.selectbox(
            "Input Source",
            input_sources,
            format_func=lambda x: f"{x.description}",
            index=input_sources.index(selected_input_source)
            if selected_input_source in input_sources else 0
        )

        average_yield = st.number_input(
            "Average Yield (kg/year)",
            value=float(farm.average_yield or 0)
        )

        update = st.form_submit_button("Update")

        if update:
            farm.farmer_id = farmer.id
            farm.farm_area = farm_area
            farm.soil_quality_id = soil_quality.id
            farm.soil_type_id = soil_type.id
            farm.irrigation_source_id = irrigation_source.id
            farm.environmental_factor_id = environmental_factor.id
            farm.access_to_inputs_id = access_to_input.id
            farm.input_source_id = input_source.id
            farm.average_yield = average_yield

            session.commit()

            st.success("Updated successfully!")
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_farm_dialog(farm_id):

    farm = session.query(Farm).get(farm_id)

    if not farm:
        st.error("Farm not found.")
        return

    st.warning(
        "Are you sure you want to delete this farm?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancel"):
            st.rerun()

    with col2:
        if st.button("🗑 Yes, Delete"):

            session.delete(farm)
            session.commit()

            st.success("Farm deleted!")
            st.rerun()

# =========================
# VIEW FARM DIALOG
# =========================
@st.dialog("👁 Farm Details")
def view_farm_dialog(farm_id):

    farm = session.query(Farm).get(farm_id)

    farmer = session.query(Farmer).filter_by(
        id=farm.farmer_id
    ).first()

    soil_quality = session.query(SoilQuality).filter_by(
        id=farm.soil_quality_id
    ).first()

    soil_type = session.query(SoilType).filter_by(
        id=farm.soil_type_id
    ).first()

    irrigation_source = session.query(IrrigationSource).filter_by(
        id=farm.irrigation_source_id
    ).first()

    environmental_factors = session.query(EnvironmentalFactor).filter_by(
        id=farm.environmental_factor_id
    ).first()

    access_to_inputs = session.query(AccessToInputs).filter_by(
        id=farm.access_to_inputs_id
    ).first()

    input_source = session.query(InputSource).filter_by(
        id=farm.input_source_id
    ).first()


    st.markdown("### Farm Information")

    st.write(
        f"**Farmer:** "
        f"{farmer.firstname} {farmer.middlename[0] + '.' if farmer.middlename else ''} {farmer.lastname}"
    )

    st.write(f"**Farm Area:** {farm.farm_area}")
    st.write(f"**Soil Quality:** {soil_quality.description if soil_quality else 'N/A'}")
    st.write(f"**Soil Type:** {soil_type.description if soil_type else 'N/A'}")
    st.write(f"**Irrigation Source:** {irrigation_source.description if irrigation_source else 'N/A'}")
    st.write(f"**Environmental Factors:** {environmental_factors.description if environmental_factors else 'N/A'}")
    st.write(f"**Access to Inputs:** {access_to_inputs.description if access_to_inputs else 'N/A'}")
    st.write(f"**Input Source:** {input_source.description if input_source else 'N/A'}")
    st.write(f"**Average Yield:** {farm.average_yield}")

    st.markdown("---")

    if st.button("❌ Close"):
        st.rerun()

# =========================
# HEADER
# =========================
col1, col2 = st.columns([8, 1.5])

with col1:

    st.markdown("""
    <div class="page-title">
        Farms Management
    </div>

    <div class="page-subtitle">
        Manage all registered farms
    </div>
    """, unsafe_allow_html=True)

# =========================
# TABLE ACTIONS
# =========================
search_col, action_col, upload_col = st.columns([0.8, 0.1, 0.1], gap="small")

with search_col:

    st.markdown("""
    <div class="search-wrapper">
        <div class="search-box">
    """, unsafe_allow_html=True)

    search = st.text_input(
        "",
        placeholder="Search farm...",
        label_visibility="collapsed"
    )

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

with action_col:
    st.markdown("")

    if st.button("Add Farm"):
        add_farm_dialog()

with upload_col:

    uploaded_file = st.file_uploader(
        "",
        type=["xlsx"],
        label_visibility="collapsed",
        key="farm_upload"
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

            rename_map = {
                "first_name": "firstname",
                "middle_name": "middlename",
                "last_name": "lastname",
            }

            df = df.rename(columns=rename_map)

            required_columns = [
                "firstname", "lastname",
                "farm_area",
                "soil_quality",
                "soil_type",
                "irrigation_source",
                "environmental_factors",
                "access_to_inputs",
                "input_source",
                "average_yield"
            ]

            missing = [c for c in required_columns if c not in df.columns]

            if missing:
                st.error(f"Missing columns: {missing}")
                st.stop()

            st.session_state.farm_df = df
            st.success("File ready for import!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # =========================
    # STEP 2: IMPORT BUTTON
    # =========================
        if st.button("Import Farms", key="import_farms_btn"):

            df = st.session_state.farm_df

            inserted = 0
            skipped = 0
            total = len(df)

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():

                try:
                    status.text(f"Processing {i+1}/{total}...")

                    # SAFE CLEANING
                    fname = str(row["firstname"]).strip()
                    lname = str(row["lastname"]).strip()

                    # FARMER LOOKUP (SAFE)
                    farmer = session.query(Farmer).filter(
                        func.lower(Farmer.firstname) == fname.lower(),
                        func.lower(Farmer.lastname) == lname.lower()
                    ).first()

                    if not farmer:
                        skipped += 1
                        continue

                    # =========================
                    # LOOKUPS
                    # =========================
                    soil_quality_id = get_rf_id(SoilQuality, row["soil_quality"])
                    soil_type_id = get_rf_id(SoilType, row["soil_type"])
                    irrigation_source_id = get_rf_id(IrrigationSource, row["irrigation_source"])
                    environmental_factor_id = get_rf_id(EnvironmentalFactor, row["environmental_factors"])
                    access_to_inputs_id = get_rf_id(AccessToInputs, row["access_to_inputs"])
                    input_source_id = get_rf_id(InputSource, row["input_source"])

                    # =========================
                    # SKIP IF REQUIRED LOOKUPS FAIL
                    # =========================
                    if (
                        soil_quality_id is None
                        or soil_type_id is None
                        or irrigation_source_id is None
                        or environmental_factor_id is None
                        or access_to_inputs_id is None
                        or input_source_id is None
                    ):
                        skipped += 1
                        continue

                    farm = Farm(
                        farmer_id=farmer.id,
                        farm_area=float(row["farm_area"] or 0),
                        soil_quality_id=soil_quality_id,
                        soil_type_id=soil_type_id,
                        irrigation_source_id=irrigation_source_id,
                        environmental_factor_id=environmental_factor_id,
                        access_to_inputs_id=access_to_inputs_id,
                        input_source_id=input_source_id,
                        average_yield=float(row["average_yield"] or 0)
                    )

                    session.add(farm)
                    inserted += 1

                except Exception as e:
                    skipped += 1
                    st.warning(f"Row {i+1} skipped: {e}")

                progress.progress((i + 1) / total)

            session.commit()

            st.success(f"Inserted: {inserted} | Skipped: {skipped}")

            # RESET (IMPORTANT)
            del st.session_state["farm_df"]

            st.rerun()

# =========================
# FETCH DATA
# =========================
query = session.query(Farm)

if search:

    search_term = f"%{search}%"

    query = (
        query
        .join(Farmer, Farmer.id == Farm.farmer_id)
        .join(SoilQuality, SoilQuality.id == Farm.soil_quality_id)
        .join(SoilType, SoilType.id == Farm.soil_type_id)
        .join(IrrigationSource, IrrigationSource.id == Farm.irrigation_source_id)
        .join(EnvironmentalFactor, EnvironmentalFactor.id == Farm.environmental_factor_id)
        .join(AccessToInputs, AccessToInputs.id == Farm.access_to_inputs_id)
        .join(InputSource, InputSource.id == Farm.input_source_id)
        .filter(
            or_(
                Farmer.firstname.ilike(search_term),
                Farmer.lastname.ilike(search_term),

                SoilQuality.code.ilike(search_term),
                SoilQuality.description.ilike(search_term),

                SoilType.code.ilike(search_term),
                SoilType.description.ilike(search_term),

                IrrigationSource.code.ilike(search_term),
                IrrigationSource.description.ilike(search_term),

                EnvironmentalFactor.code.ilike(search_term),
                EnvironmentalFactor.description.ilike(search_term),

                AccessToInputs.code.ilike(search_term),
                AccessToInputs.description.ilike(search_term),

                InputSource.code.ilike(search_term),
                InputSource.description.ilike(search_term),

                cast(Farm.farm_area, String).ilike(search_term),
                cast(Farm.average_yield, String).ilike(search_term),
            )
        )
    )

farms = query.all()

# =========================
# PAGINATION
# =========================
ROWS_PER_PAGE = 10

total_rows = len(farms)
total_pages = max((total_rows - 1) // ROWS_PER_PAGE + 1, 1)

if "farm_page" not in st.session_state:
    st.session_state.farm_page = 1

# Keep current page valid
if st.session_state.farm_page > total_pages:
    st.session_state.farm_page = total_pages

if st.session_state.farm_page < 1:
    st.session_state.farm_page = 1

start_idx = (st.session_state.farm_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

paginated_farms = farms[start_idx:end_idx]

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5, h6 = st.columns(
    [1, 3, 2, 2, 2, 2, 2]
)

    h0.markdown("<div class='table-header'>#</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Farmer</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Farm Area (ha)</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Soil Type</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Soil Quality</div>", unsafe_allow_html=True)
    h5.markdown("<div class='table-header'>Average Yield (kg/year)</div>", unsafe_allow_html=True)
    h6.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not farms:
        st.info("No farms found.")

    for i, farm in enumerate(paginated_farms, start=start_idx + 1):

        farmer = session.query(Farmer).filter_by(
            id=farm.farmer_id
        ).first()

        soil_type = session.query(SoilType).filter_by(
            id=farm.soil_type_id
        ).first()

        soil_quality = session.query(SoilQuality).filter_by(
            id=farm.soil_quality_id
        ).first()

        c0, c1, c2, c3, c4, c5, c6 = st.columns(
            [1, 3, 2, 2, 2, 2, 2]
        )

        c0.write(i)

        c1.write(
            f"{farmer.firstname} "
            f"{farmer.middlename[0] + '.' if farmer.middlename else ''} "
            f"{farmer.lastname}"
        )

        c2.write(f"{farm.farm_area}")
        c3.write(f"{soil_type.description}")
        c4.write(f"{soil_quality.description}")
        c5.write(f"{farm.average_yield}")

        with c6:

            b1, b2, b3 = st.columns(3)

            with b1:
                st.markdown(
                    '<div class="view-btn">',
                    unsafe_allow_html=True
                )

                if st.button(
                    "👁",
                    key=f"view_{farm.id}"
                ):
                    view_farm_dialog(farm.id)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with b2:
                st.markdown(
                    '<div class="edit-btn">',
                    unsafe_allow_html=True
                )

                if st.button(
                    "✏",
                    key=f"edit_{farm.id}"
                ):
                    edit_farm_dialog(farm.id)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

            with b3:
                if has_permission("delete"):

                    st.markdown(
                        '<div class="delete-btn">',
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "🗑",
                        key=f"delete_{farm.id}"
                    ):
                        delete_farm_dialog(farm.id)

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

# =========================
# PAGINATION CONTROLS
# =========================
if total_rows > 0:

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns([.04, .08, .9])

    with p1:
        if st.button(
            "⬅",
            disabled=st.session_state.farm_page == 1,
            use_container_width=False
        ):
            st.session_state.farm_page -= 1
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
                Page <b>{st.session_state.farm_page}</b> / {total_pages}
                &nbsp;|&nbsp;
                {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        if st.button(
            "➡",
            disabled=st.session_state.farm_page == total_pages,
            use_container_width=False
        ):
            st.session_state.farm_page += 1
            st.rerun()

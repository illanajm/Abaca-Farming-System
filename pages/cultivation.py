import streamlit as st
from database import session, Farm, AbacaCultivation, Farmer, Variety, PlantingDistance, PlantingMethod, IntercropCrops
from sqlalchemy import or_, func
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
    page_title="Cultivation",
    layout="wide"
)

hide_streamlit_ui()
render_sidebar()
apply_global_css()
render_header()

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
# ADD CULTIVATION DIALOG
# =========================
@st.dialog("➕ Add Cultivation Record")
def add_cultivation_dialog():

    farmers = session.query(Farmer).all()
    varieties = session.query(Variety).all()
    planting_distances = session.query(PlantingDistance).all()
    planting_methods = session.query(PlantingMethod).all()
    intercrops_crops = session.query(IntercropCrops).all()

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
            varieties,
            format_func=lambda x: f"{x.description}"
        )

        planting_distance = st.selectbox(
            "Planting Distance (meters)",
            planting_distances,
            format_func=lambda x: f"{x.description}"
        )

        planting_method = st.selectbox(
            "Planting Method",
            planting_methods,
            format_func=lambda x: f"{x.description}"
        )

        intercropping = st.selectbox(
            "Intercropping",
            ["Yes", "No"]
        )

        intercrop_crops = st.selectbox(
            "Intercrop Crops",
            intercrops_crops,
            format_func=lambda x: f"{x.description}"
        )

        submitted = st.form_submit_button("Save")

        if submitted:

            record = AbacaCultivation(
                farm_id=farm.id,
                year_first_planted=year_first,
                abaca_area=abaca_area,
                variety_id=variety.id,
                planting_distance_id=planting_distance.id,
                planting_method_id=planting_method.id,
                intercropping=intercropping,
                intercrop_crops_id=intercrop_crops.id
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

    variety = session.query(Variety).filter_by(id=record.variety_id).first()
    planting_method = session.query(PlantingMethod).filter_by(id=record.planting_method_id).first()
    planting_distance = session.query(PlantingDistance).filter_by(id=record.planting_distance_id).first()
    intercrop_crops = session.query(IntercropCrops).filter_by(id=record.intercrop_crops_id).first()

    st.markdown("### Cultivation Information")

    st.write(f"**Variety:** {variety.description if variety else 'N/A'}")
    st.write(f"**Abaca Area:** {record.abaca_area}")
    st.write(f"**Planting Method:** {planting_method.description if planting_method else 'N/A'}")
    st.write(f"**Planting Distance (Meters):** {planting_distance.description if planting_distance else 'N/A'}")
    st.write(f"**Intercropping:** {record.intercropping}")
    st.write(f"**Intercrop Crops:** {intercrop_crops.description if intercrop_crops else 'N/A'}")
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

    record = session.get(AbacaCultivation, record_id)

    farmers = session.query(Farmer).all()
    farms = session.query(Farm).all()
    varieties = session.query(Variety).all()
    planting_distances = session.query(PlantingDistance).all()
    planting_methods = session.query(PlantingMethod).all()
    intercrops_crops = session.query(IntercropCrops).all()


    selected_farm = session.get(
        Farm, record.farm_id
    )

    selected_variety = session.get(
        Variety, record.variety_id
    )

    selected_planting_distance = session.get(
        PlantingDistance, record.planting_distance_id
    )

    selected_planting_method = session.get(
        PlantingMethod, record.planting_method_id
    )

    selected_intercrop_crops = session.get(
        IntercropCrops, record.intercrop_crops_id
    )

    with st.form("edit_form"):

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

        variety = st.selectbox(
            "Variety",
            varieties,
            format_func=lambda x: f"{x.description}",
            index=varieties.index(selected_variety)
            if selected_variety in varieties else 0
        )

        year_first = st.number_input(
            "Year First Planted",
            1900,
            2100,
            value=record.year_first_planted
        )

        abaca_area = st.number_input(
            "Abaca Area",
            value=float(record.abaca_area)
        )

        planting_distance = st.selectbox(
            "Planting Distance (meters)",
            planting_distances,
            format_func=lambda x: f"{x.description}",
            index=planting_distances.index(selected_planting_distance)
            if selected_planting_distance in planting_distances else 0
        )

        planting_method = st.selectbox(
            "Planting Method",
            planting_methods,
            format_func=lambda x: f"{x.description}",
            index=planting_methods.index(selected_planting_method)
            if selected_planting_method in planting_methods else 0
        )

        intercropping = st.selectbox(
            "Intercropping",
            ["Yes", "No"],
            index=["Yes", "No"].index(record.intercropping or "No")
        )

        intercrop_crops = st.selectbox(
            "Intercrop Crops",
            intercrops_crops,
            format_func=lambda x: f"{x.description}",
            index=intercrops_crops.index(selected_intercrop_crops)
            if selected_intercrop_crops in intercrops_crops else 0
        )

        update = st.form_submit_button("Update")

        if update:
            record.farm_id = farm.id
            record.variety_id = variety.id
            record.abaca_area = abaca_area
            record.year_first_planted = year_first
            record.planting_distance_id = planting_distance.id
            record.planting_method_id = planting_method.id
            record.intercropping = intercropping
            record.intercrop_crops_id = intercrop_crops.id

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
                    # LOOKUPS
                    # =========================
                    variety_id = get_rf_id(Variety, row["variety"])
                    planting_distance_id = get_rf_id(PlantingDistance, row["planting_distance"])
                    planting_method_id = get_rf_id(PlantingMethod, row["planting_method"])
                    intercrop_crops_id = get_rf_id(IntercropCrops, row["intercrop_crops"])
                    
                    # =========================
                    # SKIP IF REQUIRED LOOKUPS FAIL
                    # =========================
                    if (
                        variety_id is None
                        or planting_distance_id is None
                        or planting_method_id is None
                        or intercrop_crops_id is None
                    ):
                        skipped += 1
                        continue

                    # =========================
                    # CREATE CULTIVATION RECORD
                    # =========================
                    record = AbacaCultivation(
                        farm_id=farm.id,
                        year_first_planted=int(row["year_first_planted"] or 0),
                        abaca_area=float(row["abaca_area"] or 0),
                        variety_id=variety_id,
                        planting_distance_id=planting_distance_id,
                        planting_method_id=planting_method_id,
                        intercropping=str(row["intercropping"] or ""),
                        intercrop_crops_id=intercrop_crops_id
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
# PAGINATION
# =========================
ROWS_PER_PAGE = 10

total_rows = len(records)
total_pages = max((total_rows - 1) // ROWS_PER_PAGE + 1, 1)

if "cultivation_page" not in st.session_state:
    st.session_state.cultivation_page = 1

# Keep current page valid
if st.session_state.cultivation_page > total_pages:
    st.session_state.cultivation_page = total_pages

if st.session_state.cultivation_page < 1:
    st.session_state.cultivation_page = 1

start_idx = (st.session_state.cultivation_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

paginated_records = records[start_idx:end_idx]

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5, h6 = st.columns(
        [1, 3, 3, 2, 2, 2, 2]
    )

    h0.markdown("<div class='table-header'>#</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Farmer</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Variety</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Abaca Area</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Planting Method</div>", unsafe_allow_html=True)
    h5.markdown("<div class='table-header'>Year Planted</div>", unsafe_allow_html=True)
    h6.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not records:
        st.info("No cultivation records found.")

    for i, r in enumerate(
        paginated_records,
        start=1
    ):
        farm = session.query(Farm).filter_by(id=r.farm_id).first()
        farmer = session.query(Farmer).filter_by(id=farm.farmer_id).first()
        variety = session.query(Variety).filter_by(id=r.variety_id).first()
        planting_method = session.query(PlantingMethod).filter_by(id=r.planting_method_id).first()

        c0, c1, c2, c3, c4, c5, c6 = st.columns(
            [1, 3, 3, 2, 2, 2, 2]
        )

        c0.write(i)
        c1.write(
            f"{farmer.firstname} "
            f"{farmer.middlename[0] + '.' if farmer.middlename else ''} "
            f"{farmer.lastname}"
        )
        c2.write(f"{variety.description if variety else 'N/A'}")
        c3.write(f"{r.abaca_area}")
        c4.write(f"{planting_method.description if planting_method else 'N/A'}")
        c5.write(f"{r.year_first_planted}")

        with c6:

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
                if has_permission("delete"):
                    st.markdown('<div class="delete-btn">', unsafe_allow_html=True)

                    if st.button("🗑", key=f"delete_{r.id}"):
                        delete_cultivation_dialog(r.id)

                    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# PAGINATION CONTROLS
# =========================
if total_rows > 0:

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns([.04, .08, .9])

    with p1:
        if st.button(
            "⬅",
            disabled=st.session_state.cultivation_page == 1,
            use_container_width=False
        ):
            st.session_state.cultivation_page -= 1
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
                Page <b>{st.session_state.cultivation_page}</b> / {total_pages}
                &nbsp;|&nbsp;
                {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        if st.button(
            "➡",
            disabled=st.session_state.cultivation_page == total_pages,
            use_container_width=False
        ):
            st.session_state.cultivation_page += 1
            st.rerun()

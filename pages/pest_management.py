import streamlit as st
from sqlalchemy import or_, func
from database import session, AbacaCultivation, PestManagement, Farm, Farmer, Variety, PestType, PestImpact, ControlMethod, ControlFrequency
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
    page_title="Pest Management",
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
    padding-top: 1px !important;
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
# FLASH SUCCESS MESSAGE
# =========================
if "success_message" in st.session_state:
    st.success(st.session_state.pop("success_message"))


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
@st.dialog("➕ Add Pest Record")
def add_pest_dialog():
    farms = session.query(Farm).all()
    farmers = session.query(Farmer).all()
    cultivations = session.query(AbacaCultivation).all()
    varieties = session.query(Variety).all()
    pest_types = session.query(PestType).all()
    pest_impacts = session.query(PestImpact).all()
    control_methods = session.query(ControlMethod).all()
    control_frequencies = session.query(ControlFrequency).all()

    # Farm map
    farm_map = {f.id: f for f in farms}

    # Farmer map
    farmer_map = {
        f.id: f"{f.firstname} {f.middlename[0] + '.' if f.middlename else ''} {f.lastname}"
        for f in farmers
    }

    variety_map = {
        v.id: v.description  # or v.name if that's your field
        for v in varieties
    }

    cultivation_map = {}

    for c in cultivations:
        farm = farm_map.get(c.farm_id)

        if farm:
            farmer_name = farmer_map.get(farm.farmer_id, "Unknown Farmer")
        else:
            farmer_name = "Unknown Farmer"

        variety_desc = variety_map.get(c.variety_id, "Unknown Variety")

        cultivation_map[c.id] = (
            f"{variety_desc} | Farm #{c.farm_id} | {farmer_name}"
        )

    with st.form("add_pest_form"):

        abaca = st.selectbox(
            "Cultivation",
            cultivations,
            format_func=lambda x: cultivation_map.get(x.id, "Unknown")
        )

        pest_type = st.selectbox(
            "Pest Type",
            pest_types,
            format_func=lambda x: f"{x.description}" 
        )

        pest_impact = st.selectbox(
            "Pest Impact",
            pest_impacts,
            format_func=lambda x: f"{x.description}" 
        )

        control_method = st.selectbox(
            "Control Method",
            control_methods,
            format_func=lambda x: f"{x.description}" 
        )

        control_frequency = st.selectbox(
            "Control Frequency",
            control_frequencies,
            format_func=lambda x: f"{x.description}" 
        )

        submit = st.form_submit_button("Save")

        if submit:

            pest = PestManagement(
                abaca_id=abaca.id,
                pest_type_id=pest_type.id,
                pest_impact_id=pest_impact.id,
                control_method_id=control_method.id,
                control_frequency_id=control_frequency.id
            )

            session.add(pest)
            session.commit()

            st.session_state.success_message = "Pest record added successfully!"
            st.rerun()

# =========================
# VIEW DIALOG
# =========================
@st.dialog("👁 Pest Details")
def view_pest_dialog(record_id):

    record = session.query(PestManagement).filter_by(
        id=record_id
    ).first()

    pest_type = session.query(PestType).filter_by(id=record.pest_type_id).first()
    pest_impact = session.query(PestImpact).filter_by(id=record.pest_impact_id).first()
    control_method = session.query(ControlMethod).filter_by(id=record.control_method_id).first()
    control_frequency = session.query(ControlFrequency).filter_by(id=record.control_frequency_id).first()

    st.markdown("### Pest Information")

    st.write(f"**Pest Type:** {pest_type.description if pest_type else 'Unknown'}")
    st.write(f"**Pest Impact:** {pest_impact.description if pest_impact else 'Unknown'}")
    st.write(f"**Control Method:** {control_method.description if control_method else 'Unknown'}")
    st.write(f"**Control Frequency:** {control_frequency.description if control_frequency else 'Unknown'}")

    st.markdown("---")

    if st.button("❌ Close"):
        st.rerun()

# =========================
# EDIT DIALOG
# =========================
@st.dialog("✏ Edit Pest Record")
def edit_pest_dialog(record_id):

    record = session.get(PestManagement, record_id)

    farmers = session.query(Farmer).all()
    farms = session.query(Farm).all()
    cultivations = session.query(AbacaCultivation).all()
    pest_types = session.query(PestType).all()
    pest_impacts = session.query(PestImpact).all()
    control_methods = session.query(ControlMethod).all()
    control_frequencies = session.query(ControlFrequency).all()

    selected_cultivation = session.get(
        AbacaCultivation, record.abaca_id
    )

    selected_pest_type = session.get(
        PestType, record.pest_type_id
    )

    selected_pest_impact = session.get(
        PestImpact, record.pest_impact_id
    )

    selected_control_method = session.get(
        ControlMethod, record.control_method_id
    )

    selected_control_frequency = session.get(
        ControlFrequency, record.control_frequency_id
    )

    farmer_map = {
        f.id: f
        for f in farmers
    }

    farm_map = {
        f.id: f
        for f in farms
    }

    cultivation_labels = {}

    for cultivation in cultivations:

        farm = farm_map.get(
            cultivation.farm_id
        )

        if not farm:

            cultivation_labels[cultivation.id] = (
                f"Cultivation #{cultivation.id}"
            )

            continue


        farmer = farmer_map.get(
            farm.farmer_id
        )

        if not farmer:

            cultivation_labels[cultivation.id] = (
                f"Farm #{farm.id}"
            )

            continue


        fullname = (
            f"{farmer.firstname} "
            f"{farmer.middlename or ''} "
            f"{farmer.lastname}"
        ).strip()


        cultivation_labels[cultivation.id] = (
            f"{fullname}"
            f" | Farm #{farm.id}"
            f" | Cultivation #{cultivation.id}"
        )

    with st.form("edit_pest_form"):

        cultivation = st.selectbox(
            "Abaca Cultivation",
            cultivations,
            format_func=lambda x: cultivation_labels.get(
                x.id,
                f"Cultivation #{x.id}"
            ),
            index=(
                cultivations.index(selected_cultivation)
                if selected_cultivation in cultivations
                else 0
            )
        )

        pest_type = st.selectbox(
            "Pest Type",
            pest_types,
            format_func=lambda x: f"{x.description}",
            index=pest_types.index(selected_pest_type)
            if selected_pest_type in pest_types else 0
        )

        pest_impact = st.selectbox(
            "Pest Impact",
            pest_impacts,
            format_func=lambda x: f"{x.description}",
            index=pest_impacts.index(selected_pest_impact)
            if selected_pest_impact in pest_impacts else 0
        )

        control_method = st.selectbox(
            "Control Method",
            control_methods,
            format_func=lambda x: f"{x.description}",
            index=control_methods.index(selected_control_method)
            if selected_control_method in control_methods else 0
        )

        control_frequency = st.selectbox(
            "Control Frequency",
            control_frequencies,
            format_func=lambda x: f"{x.description}",
            index=control_frequencies.index(selected_control_frequency)
            if selected_control_frequency in control_frequencies else 0
        )

        update = st.form_submit_button("Update")

        if update:

            record.abaca_id = cultivation.id
            record.pest_type_id = pest_type.id
            record.pest_impact_id = pest_impact.id
            record.control_method_id = control_method.id
            record.control_frequency_id = control_frequency.id

            session.commit()

            st.session_state.success_message = "Pest record updated successfully!"
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_pest_dialog(record_id):

    record = session.get(PestManagement, record_id)

    abaca = session.get(AbacaCultivation, record.abaca_id)
    farm = session.get(Farm, abaca.farm_id)
    farmer = session.get(Farmer, farm.farmer_id)
    pest_type = session.get(PestType, record.pest_type_id)

    st.warning(
        f"Delete pest management record for "
        f"{farmer.firstname} {farmer.lastname} "
        f"({pest_type.description})?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancel"):
            st.rerun()

    with col2:
        if st.button("🗑 Yes Delete"):

            session.delete(record)
            session.commit()

            st.session_state.success_message = "Pest record deleted!"
            st.rerun()

# =========================
# HEADER
# =========================
col1, col2 = st.columns([8, 1.5])

with col1:

    st.markdown("""
    <div class="page-title">
        Pest Management
    </div>

    <div class="page-subtitle">
        Monitor and control pest activity
    </div>
    """, unsafe_allow_html=True)


# =========================
# SEARCH + ADD
# =========================
search_col, action_col, upload_col = st.columns([0.8, 0.1, 0.1], gap="small")

with search_col:

    search = st.text_input(
        "",
        placeholder="Search pest...",
        label_visibility="collapsed"
    )

with action_col:

    if st.button("Add Record"):
        add_pest_dialog()

with upload_col:

    uploaded_file = st.file_uploader(
        "",
        type=["xlsx"],
        label_visibility="collapsed",
        key="pest_management_upload"
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

            # OPTIONAL rename (if Excel uses full names)
            rename_map = {
                "first_name": "firstname",
                "middle_name": "middlename",
                "last_name": "lastname",
            }

            df = df.rename(columns=rename_map)

            # REQUIRED COLUMNS
            required_columns = [
                "firstname",
                "middlename",
                "lastname",
                "pest_type",
                "pest_impact",
                "control_method",
                "control_frequency"
            ]

            missing = [c for c in required_columns if c not in df.columns]

            if missing:
                st.error(f"Missing columns: {missing}")
                st.stop()

            st.session_state.pest_df = df
            st.success("File ready for import!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

    # =========================
    # STEP 2: IMPORT BUTTON
    # =========================
        if st.button("Import Pest Records", key="import_pest_btn"):

            df = st.session_state.pest_df

            inserted = 0
            skipped = 0
            total = len(df)

            progress = st.progress(0)
            status = st.empty()

            for i, row in df.iterrows():

                try:
                    status.text(f"Processing {i+1}/{total}...")

                    fname = str(row["firstname"]).strip()
                    mname = str(row["middlename"]).strip()
                    lname = str(row["lastname"]).strip()

                    # =========================
                    # FIND FARMER
                    # =========================
                    farmer = session.query(Farmer).filter(
                        func.lower(Farmer.firstname) == fname.lower(),
                        func.lower(Farmer.middlename) == mname.lower(),
                        func.lower(Farmer.lastname) == lname.lower()
                    ).first()

                    if not farmer:
                        skipped += 1
                        continue

                    # =========================
                    # FIND FARM
                    # =========================
                    farm = session.query(Farm).filter_by(
                        farmer_id=farmer.id
                    ).first()

                    if not farm:
                        skipped += 1
                        continue

                    # =========================
                    # FIND CULTIVATION
                    # =========================
                    cultivation = session.query(AbacaCultivation).filter_by(
                        farm_id=farm.id
                    ).first()

                    if not cultivation:
                        skipped += 1
                        continue

                    # =========================
                    # LOOKUPS
                    # =========================
                    pest_types = [
                        p.strip()
                        for p in str(row["pest_type"]).split(",")
                        if p.strip()
                    ]
                    pest_impact_id = get_rf_id(PestImpact, row["pest_impact"])
                    control_method_id = get_rf_id(ControlMethod, row["control_method"])
                    control_frequency_id = get_rf_id(ControlFrequency, row["control_frequency"])

                    # =========================
                    # SKIP IF REQUIRED LOOKUPS FAIL
                    # =========================
                    if (
                        pest_impact_id is None
                        or control_method_id is None
                        or control_frequency_id is None
                    ):
                        skipped += 1
                        continue

                    # Create one record per pest type
                    for pest_name in pest_types:

                        pest_type_id = get_rf_id(PestType, pest_name)

                        if pest_type_id is None:
                            continue

                        pest = PestManagement(
                            abaca_id=cultivation.id,
                            pest_type_id=pest_type_id,
                            pest_impact_id=pest_impact_id,
                            control_method_id=control_method_id,
                            control_frequency_id=control_frequency_id
                        )

                        session.add(pest)
                        inserted += 1

                except Exception as e:
                    skipped += 1
                    st.warning(f"Row {i+1} skipped: {e}")

                progress.progress((i + 1) / total)

            session.commit()

            st.success(f"Inserted: {inserted} | Skipped: {skipped}")

            # RESET
            del st.session_state["pest_df"]
            st.rerun()

# =========================
# FETCH DATA
# =========================
query = session.query(PestManagement)

if search:

    search_term = f"%{search}%"

    query = (
        query
        .join(PestType, PestType.id == PestManagement.pest_type_id)
        .join(PestImpact, PestImpact.id == PestManagement.pest_impact_id)
        .join(ControlMethod, ControlMethod.id == PestManagement.control_method_id)
        .join(ControlFrequency, ControlFrequency.id == PestManagement.control_frequency_id)
        .filter(
            or_(
                PestType.code.ilike(search_term),
                PestType.description.ilike(search_term),

                PestImpact.code.ilike(search_term),
                PestImpact.description.ilike(search_term),

                ControlMethod.code.ilike(search_term),
                ControlMethod.description.ilike(search_term),

                ControlFrequency.code.ilike(search_term),
                ControlFrequency.description.ilike(search_term),
            )
        )
    )

records = query.all()

# =========================
# PAGINATION
# =========================
ROWS_PER_PAGE = 10

total_rows = len(records)
total_pages = max((total_rows - 1) // ROWS_PER_PAGE + 1, 1)

if "pest_page" not in st.session_state:
    st.session_state.pest_page = 1

# Keep current page valid
if st.session_state.pest_page > total_pages:
    st.session_state.pest_page = total_pages

if st.session_state.pest_page < 1:
    st.session_state.pest_page = 1

start_idx = (st.session_state.pest_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

paginated_pests = records[start_idx:end_idx]

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5, h6 = st.columns(
        [1, 3, 3, 3, 3, 2, 2]
    )

    h0.markdown("<div class='table-header'>#</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Famer</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Pest Type</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Impact</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Control Method</div>", unsafe_allow_html=True)
    h5.markdown("<div class='table-header'>Frequency</div>", unsafe_allow_html=True)
    h6.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not records:
        st.info("No pest records found.")

    for i, r in enumerate(paginated_pests, start=start_idx + 1):

        cultivation = session.query(AbacaCultivation).filter_by(
            id=r.abaca_id
        ).first()

        farm = session.query(Farm).filter_by(
            id=cultivation.farm_id
        ).first()

        farmer = session.query(Farmer).filter_by(
            id=farm.farmer_id
        ).first()

        pest_type = session.query(PestType).filter_by(
            id=r.pest_type_id
        ).first()

        pest_impact = session.query(PestImpact).filter_by(
            id=r.pest_impact_id
        ).first()

        control_method = session.query(ControlMethod).filter_by(
            id=r.control_method_id
        ).first()

        control_frequency = session.query(ControlFrequency).filter_by(
            id=r.control_frequency_id
        ).first()

        c0, c1, c2, c3, c4, c5, c6 = st.columns(
            [1, 3, 3, 3, 3, 2, 2]
        )

        c0.write(i)
        c1.write(
            f"{farmer.firstname} "
            f"{farmer.middlename[0] + '.' if farmer.middlename else ''} "
            f"{farmer.lastname}"
        )
        c2.write(pest_type.description)
        c3.write(pest_impact.description)
        c4.write(control_method.description)
        c5.write(control_frequency.description)

        with c6:

            b1, b2, b3 = st.columns(
                [1, 1, 1],
                gap="small"
            )

            with b1:

                st.markdown('<div class="view-btn">', unsafe_allow_html=True)

                if st.button("👁", key=f"view_{r.id}"):
                    view_pest_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b2:

                st.markdown('<div class="edit-btn">', unsafe_allow_html=True)

                if st.button("✏", key=f"edit_{r.id}"):
                    edit_pest_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b3:
                if has_permission("delete"):
                    st.markdown('<div class="delete-btn">', unsafe_allow_html=True)

                    if st.button("🗑", key=f"delete_{r.id}"):
                        delete_pest_dialog(r.id)

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
            disabled=st.session_state.pest_page == 1,
            use_container_width=False
        ):
            st.session_state.pest_page -= 1
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
                Page <b>{st.session_state.pest_page}</b> / {total_pages}
                &nbsp;|&nbsp;
                {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        if st.button(
            "➡",
            disabled=st.session_state.pest_page == total_pages,
            use_container_width=False
        ):
            st.session_state.pest_page += 1
            st.rerun()
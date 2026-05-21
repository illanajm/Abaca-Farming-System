import streamlit as st
from sqlalchemy import or_
from database import session, AbacaCultivation, PestManagement, Farm, Farmer

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Pest Management",
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
@st.dialog("➕ Add Pest Record")
def add_pest_dialog():
    farms = session.query(Farm).all()
    farmers = session.query(Farmer).all()

    farm_map = {
        f.id: f for f in farms
    }

    farmer_map = {
        f.id: f"{f.firstname} {f.middlename[0] + '.' if f.middlename else ''} {f.lastname}"
        for f in farmers
    }

    cultivations = session.query(AbacaCultivation).all()

    with st.form("add_pest_form"):

        abaca = st.selectbox(
            "Cultivation",
            cultivations,
            format_func=lambda x: (
                f"{x.variety} | "
                f"Farm #{x.farm_id} | "
                f"{farmer_map.get(farm_map.get(x.farm_id).farmer_id) if farm_map.get(x.farm_id) else 'Unknown Farmer'}"
            )
        )

        pest_type = st.text_input("Pest Type")
        pest_impact = st.text_input("Pest Impact")
        control_method = st.text_input("Control Method")
        control_frequency = st.text_input("Control Frequency")

        submit = st.form_submit_button("Save")

        if submit:

            pest = PestManagement(
                abaca_id=abaca.id,
                pest_type=pest_type,
                pest_impact=pest_impact,
                control_method=control_method,
                control_frequency=control_frequency
            )

            session.add(pest)
            session.commit()

            st.success("Added successfully!")
            st.rerun()

# =========================
# VIEW DIALOG
# =========================
@st.dialog("👁 Pest Details")
def view_pest_dialog(record_id):

    record = session.query(PestManagement).filter_by(
        id=record_id
    ).first()

    st.markdown("### Pest Information")

    st.write(f"**Pest Type:** {record.pest_type}")
    st.write(f"**Pest Impact:** {record.pest_impact}")
    st.write(f"**Control Method:** {record.control_method}")
    st.write(f"**Control Frequency:** {record.control_frequency}")

    st.markdown("---")

    if st.button("❌ Close"):
        st.rerun()

# =========================
# EDIT DIALOG
# =========================
@st.dialog("✏ Edit Pest Record")
def edit_pest_dialog(record_id):

    record = session.query(PestManagement).filter_by(
        id=record_id
    ).first()

    with st.form("edit_pest_form"):

        pest_type = st.text_input(
            "Pest Type",
            value=record.pest_type
        )

        pest_impact = st.text_input(
            "Pest Impact",
            value=record.pest_impact
        )

        control_method = st.text_input(
            "Control Method",
            value=record.control_method
        )

        control_frequency = st.text_input(
            "Control Frequency",
            value=record.control_frequency
        )

        update = st.form_submit_button("Update")

        if update:

            record.pest_type = pest_type
            record.pest_impact = pest_impact
            record.control_method = control_method
            record.control_frequency = control_frequency

            session.commit()

            st.success("Updated!")
            st.rerun()

# =========================
# DELETE DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_pest_dialog(record_id):

    record = session.query(PestManagement).filter_by(
        id=record_id
    ).first()

    st.warning(
        f"Delete '{record.pest_type}'?"
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
        Pest Management
    </div>

    <div class="page-subtitle">
        Monitor and control pest activity
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
search_col, action_col = st.columns([1, 0.2], gap="large")

with search_col:

    search = st.text_input(
        "",
        placeholder="Search pest...",
        label_visibility="collapsed"
    )

with action_col:

    if st.button("Add Record"):
        add_pest_dialog()

# =========================
# FETCH DATA
# =========================
query = session.query(PestManagement)

if search:

    search_term = f"%{search}%"

    query = query.filter(
        or_(
            PestManagement.pest_type.ilike(search_term),
            PestManagement.pest_impact.ilike(search_term),
            PestManagement.control_method.ilike(search_term),
            PestManagement.control_frequency.ilike(search_term),
        )
    )

records = query.all()

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4 = st.columns(
        [3, 3, 3, 2, 2]
    )

    h0.markdown("<div class='table-header'>Pest Type</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Impact</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Control Method</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Frequency</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not records:
        st.info("No pest records found.")

    for r in records:

        c0, c1, c2, c3, c4 = st.columns(
            [3, 3, 3, 2, 2]
        )

        c0.write(r.pest_type)
        c1.write(r.pest_impact)
        c2.write(r.control_method)
        c3.write(r.control_frequency)

        with c4:

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

                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)

                if st.button("🗑", key=f"delete_{r.id}"):
                    delete_pest_dialog(r.id)

                st.markdown('</div>', unsafe_allow_html=True)
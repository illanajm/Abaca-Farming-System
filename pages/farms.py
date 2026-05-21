import streamlit as st
from database import session, Farmer, Farm

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Farms",
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
# ADD FARM DIALOG
# =========================
@st.dialog("➕ Add Farm")
def add_farm_dialog():

    farmers = session.query(Farmer).all()

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
            ["Poor", "Average", "Good", "Excellent"]
        )

        soil_type = st.selectbox(
            "Soil Type",
            ["Sandy", "Clay", "Silty", "Peaty", "Chalky", "Loam"]
        )

        irrigation_source = st.selectbox(
            "Irrigation Source",
            ["River", "Deep Well", "Rainfed", "Irrigation System", "Water Pump", "Water Trucking", "Saline Irrigation", "None"]
        )

        environmental_factors = st.selectbox(
            "Environmental Factors",
            ["Drought", "Flooding", "Pests", "Diseases", "Frost", "Heatwaves", "Typhoon", "Wind Exposure", "Soil Fertility", "Climate Change", "None"]
        )

        access_to_inputs = st.selectbox(
            "Access to Inputs",
            ["Accessible", "Limited", "None"]
        )

        input_source = st.selectbox(
            "Input Source",
            ["Local Market", "Cooperative", "Government Program", "Private Supplier", "Own Production", "Neighboring Farmers", "Loan/Credit", "Local Suppliers"]
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
                soil_quality=soil_quality,
                soil_type=soil_type,
                irrigation_source=irrigation_source,
                environmental_factors=environmental_factors,
                access_to_inputs=access_to_inputs,
                input_source=input_source,
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

    farm = session.query(Farm).get(farm_id)

    with st.form("edit_farm_form"):

        farm_area = st.number_input(
            "Farm Area (ha)",
            value=float(farm.farm_area or 0)
        )

        soil_quality = st.selectbox(
            "Soil Quality",
            ["Poor", "Average", "Good", "Excellent"],
            index=["Poor", "Average", "Good", "Excellent"].index(farm.soil_quality) if farm.soil_quality in ["Poor", "Average", "Good", "Excellent"] else 0
        )

        soil_type = st.selectbox(
            "Soil Type",
            ["Sandy", "Clay", "Silty", "Peaty", "Chalky", "Loam"],
            index=["Sandy", "Clay", "Silty", "Peaty", "Chalky", "Loam"].index(farm.soil_type) if farm.soil_type in ["Sandy", "Clay", "Silty", "Peaty", "Chalky", "Loam"] else 0
        )

        irrigation_source = st.selectbox(
            "Irrigation Source",
            ["River", "Deep Well", "Rainfed", "Irrigation System", "Water Pump", "Water Trucking", "Saline Irrigation", "None"],
            index=["River", "Deep Well", "Rainfed", "Irrigation System", "Water Pump", "Water Trucking", "Saline Irrigation", "None"].index(farm.irrigation_source) if farm.irrigation_source in ["River", "Deep Well", "Rainfed", "Irrigation System", "Water Pump", "Water Trucking", "Saline Irrigation", "None"] else 0
        )

        environmental_factors = st.selectbox(
            "Environmental Factors",
            ["Drought", "Flooding", "Pests", "Diseases", "Frost", "Heatwaves", "Typhoon", "Wind Exposure", "Soil Fertility", "Climate Change", "None"],
            index=["Drought", "Flooding", "Pests", "Diseases", "Frost", "Heatwaves", "Typhoon", "Wind Exposure", "Soil Fertility", "Climate Change", "None"].index(farm.environmental_factors) if farm.environmental_factors in ["Drought", "Flooding", "Pests", "Diseases", "Frost", "Heatwaves", "Typhoon", "Wind Exposure", "Soil Fertility", "Climate Change", "None"] else 0
        )

        access_to_inputs = st.selectbox(
            "Access to Inputs",
            ["Accessible", "Limited", "None"],
            index=["Accessible", "Limited", "None"].index(farm.access_to_inputs) if farm.access_to_inputs in ["Accessible", "Limited", "None"] else 0
        )

        input_source = st.selectbox(
            "Input Source",
            ["Local Market", "Cooperative", "Government Program", "Private Supplier", "Own Production", "Neighboring Farmers", "Loan/Credit", "Local Suppliers"],
            index=["Local Market", "Cooperative", "Government Program", "Private Supplier", "Own Production", "Neighboring Farmers", "Loan/Credit", "Local Suppliers"].index(farm.input_source) if farm.input_source in ["Local Market", "Cooperative", "Government Program", "Private Supplier", "Own Production", "Neighboring Farmers", "Loan/Credit", "Local Suppliers"] else 0
        )

        average_yield = st.number_input(
            "Average Yield (kg/year)",
            value=float(farm.average_yield or 0)
        )

        update = st.form_submit_button("Update")

        if update:

            farm.farm_area = farm_area
            farm.soil_quality = soil_quality
            farm.soil_type = soil_type
            farm.irrigation_source = irrigation_source
            farm.environmental_factors = environmental_factors
            farm.access_to_inputs = access_to_inputs
            farm.input_source = input_source
            farm.average_yield = average_yield
            session.commit()

            st.success("Updated!")
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

    st.markdown("### Farm Information")

    st.write(
        f"**Farmer:** "
        f"{farmer.firstname} {farmer.middlename[0] + '.' if farmer.middlename else ''} {farmer.lastname}"
    )

    st.write(f"**Farm Area:** {farm.farm_area}")
    st.write(f"**Soil Quality:** {farm.soil_quality}")
    st.write(f"**Soil Type:** {farm.soil_type}")
    st.write(f"**Irrigation Source:** {farm.irrigation_source}")
    st.write(f"**Environmental Factors:** {farm.environmental_factors}")
    st.write(f"**Access to Inputs:** {farm.access_to_inputs}")
    st.write(f"**Input Source:** {farm.input_source}")
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
# TABLE ACTIONS
# =========================
search_col, action_col = st.columns([1, 0.2], gap="large")

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

# =========================
# FETCH DATA
# =========================
query = session.query(Farm)

if search:

    search_term = f"%{search}%"

    query = query.join(
        Farmer,
        Farmer.id == Farm.farmer_id
    ).filter(
        or_(
            Farmer.firstname.ilike(search_term),
            Farmer.lastname.ilike(search_term),

            cast(Farm.farm_area, String).ilike(search_term),
            Farm.soil_quality.ilike(search_term),
            Farm.soil_type.ilike(search_term),
            Farm.irrigation_source.ilike(search_term),
            Farm.environmental_factors.ilike(search_term),
            Farm.access_to_inputs.ilike(search_term),
            Farm.input_source.ilike(search_term),
            cast(Farm.average_yield, String).ilike(search_term),
        )
    )

farms = query.all()

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5 = st.columns(
        [3, 2, 2, 2, 2, 2]
    )

    h0.markdown("<div class='table-header'>Farmer</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Farm Area (ha)</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Soil Type</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Soil Quality</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Average Yield (kg/year)</div>", unsafe_allow_html=True)
    h5.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not farms:
        st.info("No farms found.")

    for farm in farms:

        farmer = session.query(Farmer).filter_by(
            id=farm.farmer_id
        ).first()

        c0, c1, c2, c3, c4, c5 = st.columns(
            [3, 2, 2, 2, 2, 2]
        )

        c0.write(
            f"{farmer.firstname} {farmer.middlename[0] + '.' if farmer.middlename else ''} {farmer.lastname}"
        )

        c1.write(f"{farm.farm_area}")
        c2.write(f"{farm.soil_type}")
        c3.write(f"{farm.soil_quality}")
        c4.write(f"{farm.average_yield}")

        with c5:

            b1, b2, b3 = st.columns(3)

            with b1:
                st.markdown('<div class="view-btn">', unsafe_allow_html=True)

                if st.button("👁", key=f"view_{farm.id}"):
                    view_farm_dialog(farm.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b2:
                st.markdown('<div class="edit-btn">', unsafe_allow_html=True)

                if st.button("✏", key=f"edit_{farm.id}"):
                    edit_farm_dialog(farm.id)

                st.markdown('</div>', unsafe_allow_html=True)

            with b3:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)

                if st.button("🗑", key=f"delete_{farm.id}"):
                    delete_farm_dialog(farm.id)

                st.markdown('</div>', unsafe_allow_html=True)

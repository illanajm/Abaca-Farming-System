import streamlit as st
from sqlalchemy import or_, func, cast, String
from database import session, Farmer
from datetime import date

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Farmers",
    layout="wide"
)

# =========================
# AUTH CHECK
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("app.py")

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
    background: linear-gradient(
        white
    );
    width: 270px;
    border-right: 2px solid #ffffff20;
}

/* Hide default nav */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Sidebar text */
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

/* =========================
   LOGO AREA
   ========================= */
.logo-container {
    text-align: center;
    padding-top: 10px;
    padding-bottom: 20px;
}

.logo-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-top: 10px;
    text-align: center;
    top: -100px;
}

.logo-subtitle {
    color: #d9ffd9;
    font-size: 14px;
    text-align: center;
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

/* PAGE TITLE */
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

/* TABLE CONTAINER */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border-radius: 20px !important;
    padding: 25px !important;
}

/* SEARCH CONTAINER */
.search-wrapper {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

/* SEARCH INPUT AREA */
.search-box {
    position: relative;
    width: 250px;
}

/* SEARCH ICON */
.search-box .search-icon {
    position: absolute;
    left: 12px;
    top: 11px;
    font-size: 14px;
    color: #888;
    z-index: 999;
    pointer-events: none;
}

/* INPUT */
.search-box input {
    width: 100% !important;
    height: 38px !important;
    padding-left: 35px !important;
    border-radius: 10px !important;
    border: 1px solid #d9d9d9 !important;
    font-size: 13px !important;
    background-color: white !important;
}

.table-header {
    font-size: 17px;
    font-weight: 700;
    color: #333;
    # text-align: center;
}

.welcome-top-right {
    position: absolute;
    top: -35px;
    right: 30px;
    font-size: 16px;
    color: #666;
    font-weight: 500;
    z-index: 999;
}

</style>
""", unsafe_allow_html=True)

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

    st.page_link(
        "pages/dashboard.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/farmers.py",
        label="👨‍🌾 Farmers"
    )

    st.page_link(
        "pages/farms.py",
        label="🌱 Farms"
    )

    st.page_link(
        "pages/cultivation.py",
        label="🌾 Cultivation"
    )

    st.page_link(
        "pages/pest_management.py",
        label="🐛 Pest Management"
    )

    st.page_link(
        "pages/soil_management.py",
        label="🧪 Soil Management"
    )
    st.page_link("pages/reports.py", label="📊 Analytics & Reports")

    st.markdown("---")

# =========================
# CALCULATE AGE FUNCTION
# =========================
def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )


# =========================
# ADD FARMER DIALOG
# =========================
@st.dialog("➕ Add New Farmer")
def add_farmer_dialog():

    with st.form("add_farmer_form"):

        firstname = st.text_input("First Name")
        middlename = st.text_input("Middle Name")
        lastname = st.text_input("Last Name")

        sex = st.selectbox(
            "Sex",
            ["Male", "Female", "Other"]
        )

        # =========================
        # BIRTHDATE INPUT
        # =========================
        birthdate = st.date_input(
            "Birthdate",
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        # =========================
        # REALTIME AGE
        # =========================
        age = calculate_age(birthdate)

        civil_status = st.selectbox(
            "Civil Status",
            ["Single", "Married", "Divorced", "Widowed", "Common-law"]
        )

        city_municipality = st.text_input(
            "City/Municipality"
        )

        barangay = st.text_input(
            "Barangay"
        )

        years_in_farming = st.number_input(
            "Years in Farming",
            0
        )

        farming_break = st.number_input(
            "Farming Break",
            0
        )

        break_year_start = st.number_input(
            "Break Year Start",
            0
        )

        break_year_end = st.number_input(
            "Break Year End",
            0
        )
        
        reason_for_break = st.text_area(
            "Reason for Break",
            height=150,
            placeholder="Describe the reason for farming break..."
        )

        submitted = st.form_submit_button(
            "Save"
        )

        if submitted:

            farmer = Farmer(
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                sex=sex,
                birthdate=str(birthdate),  # Store as string in DB
                age=age,               # auto-calculated age
                civil_status=civil_status,
                city_municipality=city_municipality,
                barangay=barangay,
                years_in_farming=years_in_farming,
                farming_break=farming_break,
                break_year_start=break_year_start,
                break_year_end=break_year_end,
                reason_for_break=reason_for_break
            )

            session.add(farmer)
            session.commit()

            st.success("Farmer added!")
            st.rerun()

# =========================
# CALCULATE AGE FUNCTION
# =========================
def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

# =========================
# EDIT FARMER DIALOG
# =========================
@st.dialog("✏ Edit Farmer")
def edit_farmer_dialog(farmer_id):

    farmer = session.query(Farmer).filter_by(
        id=farmer_id
    ).first()

    if not farmer:
        st.error("Farmer not found")
        return

    with st.form("edit_farmer_form"):

        firstname = st.text_input(
            "First Name",
            value=farmer.firstname
        )

        middlename = st.text_input(
            "Middle Name",
            value=farmer.middlename
        )

        lastname = st.text_input(
            "Last Name",
            value=farmer.lastname
        )

        sex = st.selectbox(
            "Sex",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(
                farmer.sex
            )
        )
        birthdate = st.date_input(
            "Birthdate",
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            value=date.fromisoformat(farmer.birthdate)
        )

        age = calculate_age(birthdate)

        civil_status = st.selectbox(
            "Civil Status",
            ["Single", "Married", "Divorced", "Widowed", "Common-law"],
            index=["Single", "Married", "Divorced", "Widowed", "Common-law"].index(
                farmer.civil_status
            )
        )

        city_municipality = st.text_input(
            "City/Municipality",
            value=farmer.city_municipality
        )

        barangay = st.text_input(
            "Barangay",
            value=farmer.barangay
        )

        years_in_farming = st.number_input(
            "Years in Farming",
            0,
            value=farmer.years_in_farming
        )

        farming_break = st.number_input(
            "Farming Break",
            0,
            value=farmer.farming_break
        )

        break_year_start = st.number_input(
            "Break Year Start",
            0,
            value=farmer.break_year_start
        )

        break_year_end = st.number_input(
            "Break Year End",
            0,
            value=farmer.break_year_end
        )

        reason_for_break = st.text_area(
            "Reason for Break",
            value=farmer.reason_for_break,
            height=150,
            placeholder="Describe the reason for farming break..."
        )

        submitted = st.form_submit_button(
            "Update"
        )

        if submitted:

            farmer.firstname = firstname
            farmer.middlename = middlename
            farmer.lastname = lastname
            farmer.sex = sex
            farmer.birthdate = str(birthdate)
            farmer.age = age
            farmer.civil_status = civil_status
            farmer.city_municipality = city_municipality
            farmer.barangay = barangay
            farmer.years_in_farming = years_in_farming
            farmer.farming_break = farming_break
            farmer.break_year_start = break_year_start
            farmer.break_year_end = break_year_end
            farmer.reason_for_break = reason_for_break

            session.commit()

            st.success("Updated!")
            st.rerun()

# =========================
# DELETE FARMER DIALOG
# =========================
@st.dialog("⚠️ Confirm Delete")
def delete_farmer_dialog(farmer_id):

    farmer = session.query(Farmer).filter_by(id=farmer_id).first()

    if not farmer:
        st.error("Farmer not found.")
        return

    st.warning(
        f"Are you sure you want to delete **{farmer.firstname} {farmer.lastname}**?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancel"):
            st.rerun()

    with col2:
        if st.button("🗑 Yes, Delete"):
            session.delete(farmer)
            session.commit()
            st.success("Farmer deleted!")
            st.rerun()

# =========================
# VIEW FARMER DIALOG
# =========================
@st.dialog("👁 Farmer Details")
def view_farmer_dialog(farmer_id):

    farmer = session.query(Farmer).filter_by(id=farmer_id).first()

    if not farmer:
        st.error("Farmer not found.")
        return

    st.markdown("### Personal Information")

    st.write(f"**Name:** {farmer.firstname} {farmer.middlename} {farmer.lastname}")
    st.write(f"**Sex:** {farmer.sex}")
    st.write(f"**Birthdate:** {farmer.birthdate}")
    st.write(f"**Age:** {farmer.age}")
    st.write(f"**Civil Status:** {farmer.civil_status}")

    st.markdown("### Location")
    st.write(f"**Address:** {farmer.barangay}, {farmer.city_municipality}")

    st.markdown("### Farming Information")
    st.write(f"**Years in Farming:** {farmer.years_in_farming}")
    st.write(f"**Farming Break:** {farmer.farming_break}")
    st.write(f"**Break Year:** {farmer.break_year_start} - {farmer.break_year_end}")
    st.write(f"**Reason for Break:** {farmer.reason_for_break}")

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
        Farmer's Record List
    </div>

    <div class="page-subtitle">
        Manage all registered farmers
    </div>
    """, unsafe_allow_html=True)

with col2:

    with st.popover(f"Welcome back, {st.session_state.get('user', 'Farmer')}"):

        st.markdown("### Account")

        st.write(f"User: {st.session_state.get('user', 'Farmer')}")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.pop("user", None)
            st.switch_page("app.py")

# =========================
# TABLE HEADER ACTIONS
# =========================
search_col, age_col, action_col = st.columns([1.2, 0.8, 0.3], gap="small")

with search_col:
    search = st.text_input(
        "",
        placeholder="Search farmer...",
        label_visibility="collapsed"
    )

with age_col:
    a1, a2 = st.columns(2)

    with a1:
        min_age = st.number_input(
            "Min",
            min_value=0,
            value=0,
            step=1,
            label_visibility="collapsed"
        )

    with a2:
        max_age = st.number_input(
            "Max",
            min_value=0,
            value=150,
            step=1,
            label_visibility="collapsed"
        )

    if min_age > max_age:
        st.error("Min Age cannot be greater than Max Age")
        st.stop()

with action_col:
    if st.button("➕ Add Farmer"):
        add_farmer_dialog()

# =========================
# FETCH DATA
# =========================
query = session.query(Farmer)

# AGE RANGE FILTER (add this BEFORE search filter or inside it)
query = query.filter(Farmer.age >= min_age, Farmer.age <= max_age)

if search:

    search_term = f"%{search}%"

    # FULL NAME COMBINATIONS
    fullname1 = func.concat(
        Farmer.firstname,
        " ",
        Farmer.lastname
    )

    fullname2 = func.concat(
        Farmer.firstname,
        " ",
        Farmer.middlename,
        " ",
        Farmer.lastname
    )

    fullname3 = func.concat(
        Farmer.lastname,
        " ",
        Farmer.firstname
    )

    fullname4 = func.concat(
        Farmer.firstname,
        " ",
        Farmer.middlename
    )

    fullname5 = func.concat(
        Farmer.middlename,
        " ",
        Farmer.lastname
    )

    query = query.filter(
        or_(

            # NAME SEARCH
            Farmer.firstname.ilike(search_term),
            Farmer.middlename.ilike(search_term),
            Farmer.lastname.ilike(search_term),

            fullname1.ilike(search_term),
            fullname2.ilike(search_term),
            fullname3.ilike(search_term),
            fullname4.ilike(search_term),
            fullname5.ilike(search_term),

            # OTHER DATA
            Farmer.sex.ilike(search_term),
            Farmer.civil_status.ilike(search_term),
            Farmer.city_municipality.ilike(search_term),
            Farmer.barangay.ilike(search_term),
            Farmer.reason_for_break.ilike(search_term),

            cast(Farmer.age, String).ilike(search_term),
            cast(Farmer.years_in_farming, String).ilike(search_term),
            cast(Farmer.farming_break, String).ilike(search_term),
            cast(Farmer.break_year_start, String).ilike(search_term),
            cast(Farmer.break_year_end, String).ilike(search_term),
        )
    )

farmers = query.all()

# =========================
# TABLE
# =========================
with st.container(border=True):

    h0, h1, h2, h3, h4, h5, h6, h7 = st.columns(
        [1, 3, 2, 2, 2, 2, 2, 2]
    )

    h0.markdown("<div class='table-header'>#</div>", unsafe_allow_html=True)
    h1.markdown("<div class='table-header'>Name</div>", unsafe_allow_html=True)
    h2.markdown("<div class='table-header'>Sex</div>", unsafe_allow_html=True)
    h3.markdown("<div class='table-header'>Birthdate</div>", unsafe_allow_html=True)
    h4.markdown("<div class='table-header'>Age</div>", unsafe_allow_html=True)
    h5.markdown("<div class='table-header'>Civil Status</div>", unsafe_allow_html=True)
    h6.markdown("<div class='table-header'>Address</div>", unsafe_allow_html=True)
    h7.markdown("<div class='table-header'>Actions</div>", unsafe_allow_html=True)

    st.divider()

    if not farmers:
        st.info("No farmers found.")

    for index, farmer in enumerate(
        farmers,
        start=1
    ):

        c0, c1, c2, c3, c4, c5, c6, c7 = st.columns(
            [1, 3, 2, 2, 2, 2, 2, 2]
        )

        c0.markdown(f"**{index}**")

        c1.write(
            f"{farmer.firstname} {farmer.middlename[0] + '.' if farmer.middlename else ''} {farmer.lastname}"
        )

        c2.write(
            f"{farmer.sex}"
        )

        c3.write(
            f"{farmer.birthdate}"
        )

        c4.write(
            f"{farmer.age}"
        )

        c5.write(
            f"{farmer.civil_status}"
        )

        c6.write(
            f"{farmer.city_municipality} "
            f"{farmer.barangay}"
        )

        with c7:

            b1, b2, b3 = st.columns(3)

            with b1:

                if st.button("👁", key=f"view_{farmer.id}"):
                    view_farmer_dialog(farmer.id)

            with b2:

                if st.button(
                    "✏",
                    key=f"edit_{farmer.id}"
                ):

                    edit_farmer_dialog(
                        farmer.id
                    )

            with b3:

                if st.button("🗑", key=f"del_{farmer.id}"):
                    delete_farmer_dialog(farmer.id)


# =========================
# VIEW FARMER
# =========================
if st.session_state.get("open_view"):

    farmer = session.query(Farmer).filter_by(
        id=st.session_state.view_id
    ).first()

    if farmer:

        st.subheader(
            "👁 Farmer Details"
        )

        st.write(
            f"Name: "
            f"{farmer.firstname} "
            f"{farmer.lastname}"
        )

        st.write(
            f"Middle Name: "
            f"{farmer.middlename}"
        )

        st.write(
            f"Sex: {farmer.sex}"
        )

        st.write(
            f"Age: {farmer.age}"
        )

        st.write(
            f"Civil Status: "
            f"{farmer.civil_status}"
        )

        st.write(
            f"Location: "
            f"{farmer.barangay}, "
            f"{farmer.city_municipality}"
        )

        st.write(
            f"Years in Farming: "
            f"{farmer.years_in_farming}"
        )

        st.write(
            f"Farming Break: "
            f"{farmer.farming_break}"
        )

        st.write(
            f"Break Years: "
            f"{farmer.break_year_start} "
            f"- "
            f"{farmer.break_year_end}"
        )

        st.write(
            f"Reason for Break: "
            f"{farmer.reason_for_break}"
        )

        if st.button("Close"):

            st.session_state.open_view = False
            st.rerun()
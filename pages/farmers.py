import streamlit as st
from sqlalchemy import or_, func, cast, String
from database import session, Farmer
from datetime import date, datetime
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
    page_title="Farmers",
    layout="wide"
)

hide_streamlit_ui()
render_sidebar() # Render custom sidebar with navigation links
apply_global_css() # Apply global CSS for consistent styling
render_header() # Render consistent header across pages

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

/* PAGE TITLE */
.page-title {
    font-size: 37px;
    font-weight: 800;
    color: #006622;
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
            max_value = date(date.today().year, 12, 31)
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
            max_value = date(date.today().year, 12, 31),
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
    birthdate = datetime.strptime(farmer.birthdate, "%Y-%m-%d")

    if not farmer:
        st.error("Farmer not found.")
        return

    st.markdown("### Personal Information")

    st.write(f"**Name:** {farmer.firstname} {farmer.middlename} {farmer.lastname}")
    st.write(f"**Sex:** {farmer.sex}")
    st.write(f"**Birthdate:** {birthdate.strftime('%B %d, %Y')}")
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

# =========================
# TABLE HEADER ACTIONS
# =========================
search_col, age_col, add_col, upload_col = st.columns(
    [3, 4.4, 0.9, 0.8],
    vertical_alignment="center"
)

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

with add_col:
    if st.button("➕ Add Farmer"):
        add_farmer_dialog()

with upload_col:
    uploaded_file = st.file_uploader("", type=["xlsx"], label_visibility="collapsed", key="farmer_upload")

    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file)

        # =========================
        # CLEAN HEADERS
        # =========================
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("/", "_")
            .str.replace("-", "_")
        )

        # =========================
        # MAP NAMES
        # =========================
        rename_map = {
            "first_name": "firstname",
            "middle_name": "middlename",
            "last_name": "lastname",
        }

        df = df.rename(columns=rename_map)

        required_columns = [
            "firstname", "middlename", "lastname",
            "sex", "birthdate", "civil_status",
            "city_municipality", "barangay",
            "years_in_farming", "farming_break",
            "break_year_start", "break_year_end",
            "reason_for_break"
        ]

        missing = [c for c in required_columns if c not in df.columns]

        if missing:
            st.error(f"Missing columns: {missing}")
            st.stop()

        
        existing_farmers = session.query(Farmer).all()

        farmers_map = {
            (
                f.firstname.strip().lower(),
                f.middlename.strip().lower(),
                f.lastname.strip().lower()
            ): f
            for f in existing_farmers
        }


        if st.button("Import Farmers"):

            inserted = 0
            skipped = 0
            total = len(df)

            for i, row in df.iterrows():

                try:
                    firstname = str(row["firstname"]).strip()
                    middlename = str(row["middlename"]).strip()
                    lastname = str(row["lastname"]).strip()

                    key = (
                        firstname.lower(),
                        middlename.lower(),
                        lastname.lower()
                    )

                    birthdate = pd.to_datetime(row["birthdate"], errors="coerce")

                    if pd.isna(birthdate):
                        skipped += 1
                        continue

                    birthdate = birthdate.date()
                    age = calculate_age(birthdate)

                    def safe_int(val):
                        try:
                            return int(val)
                        except:
                            return 0

                    # =========================
                    # IF EXISTS → UPDATE
                    # =========================
                    if key in farmers_map:

                        farmer = farmers_map[key]

                        farmer.sex = str(row["sex"]).strip()
                        farmer.birthdate = str(birthdate)
                        farmer.age = age
                        farmer.civil_status = str(row["civil_status"]).strip()
                        farmer.city_municipality = str(row["city_municipality"]).strip()
                        farmer.barangay = str(row["barangay"]).strip()
                        farmer.years_in_farming = safe_int(row["years_in_farming"])
                        farmer.farming_break = safe_int(row["farming_break"])
                        farmer.break_year_start = safe_int(row["break_year_start"])
                        farmer.break_year_end = safe_int(row["break_year_end"])
                        farmer.reason_for_break = str(row["reason_for_break"] or "")

                        updated += 1

                    # =========================
                    # ELSE → INSERT NEW
                    # =========================
                    else:

                        farmer = Farmer(
                            firstname=firstname,
                            middlename=middlename,
                            lastname=lastname,
                            sex=str(row["sex"]).strip(),
                            birthdate=str(birthdate),
                            age=age,
                            civil_status=str(row["civil_status"]).strip(),
                            city_municipality=str(row["city_municipality"]).strip(),
                            barangay=str(row["barangay"]).strip(),
                            years_in_farming=safe_int(row["years_in_farming"]),
                            farming_break=safe_int(row["farming_break"]),
                            break_year_start=safe_int(row["break_year_start"]),
                            break_year_end=safe_int(row["break_year_end"]),
                            reason_for_break=str(row["reason_for_break"] or "")
                        )

                        session.add(farmer)

                        # also add to map so duplicates inside Excel update properly
                        farmers_map[key] = farmer

                        inserted += 1

                except Exception as e:
                    skipped += 1
                    st.warning(f"Row {i+1} error: {e}")

            # IMPORTANT: COMMIT OUTSIDE LOOP
            session.commit()

            st.success(f"Inserted: {inserted} | Skipped: {skipped}")
            st.rerun()

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
# PAGINATION
# =========================
ROWS_PER_PAGE = 10

total_rows = len(farmers)
total_pages = max((total_rows - 1) // ROWS_PER_PAGE + 1, 1)

if "farmer_page" not in st.session_state:
    st.session_state.farmer_page = 1

# Keep current page valid
if st.session_state.farmer_page > total_pages:
    st.session_state.farmer_page = total_pages

if st.session_state.farmer_page < 1:
    st.session_state.farmer_page = 1

start_idx = (st.session_state.farmer_page - 1) * ROWS_PER_PAGE
end_idx = start_idx + ROWS_PER_PAGE

paginated_farmers = farmers[start_idx:end_idx]

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
        paginated_farmers,
        start=start_idx + 1
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

        c3.write(datetime.strptime(farmer.birthdate, "%Y-%m-%d").strftime("%B %d, %Y"))

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
                if has_permission("delete"):
                    if st.button("🗑", key=f"del_{farmer.id}"):
                        delete_farmer_dialog(farmer.id)

# =========================
# PAGINATION CONTROLS
# =========================
if total_rows > 0:

    st.markdown("<br>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns([.04, .08, .9])

    with p1:
        if st.button(
            "⬅",
            disabled=st.session_state.farmer_page == 1,
            use_container_width=False
        ):
            st.session_state.farmer_page -= 1
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
                Page <b>{st.session_state.farmer_page}</b> / {total_pages}
                &nbsp;|&nbsp;
                {start_idx + 1}-{min(end_idx, total_rows)} of {total_rows}
            </div>
            """,
            unsafe_allow_html=True
        )

    with p3:
        if st.button(
            "➡",
            disabled=st.session_state.farmer_page == total_pages,
            use_container_width=False
        ):
            st.session_state.farmer_page += 1
            st.rerun()


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
import streamlit as st
from datetime import date
from database import User, session

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Abaca Farming System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# GLOBAL STYLE
# =========================
st.markdown("""
<style>

/* Hide Sidebar */
[data-testid="stSidebar"] {
    display: none;
}

/* Page background */
.stApp {
    background-color: #f2f2f2;
}

/* Center content */
.block-container {
    max-width: 1200px;
    padding-top: 10rem;
}

/* =========================
   MAIN CARD (IMPORTANT FIX)
   ========================= */
div[data-testid="stHorizontalBlock"] {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,1);
    background: white;
}

/* LEFT COLUMN (GREEN) */
div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
    background-color: white;
    padding: 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

/* RIGHT COLUMN (WHITE) */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    background: linear-gradient(135deg, #006622, #1f6f4a, #468767) !important;
    padding: 60px !important;
    color: white !important;
    box-shadow: 0 10px 25px rgba(0, 102, 34, 0.25) !important;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* BUTTONS */
.stButton button,
.stFormSubmitButton button {
    background-color: #009933 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    height: 45px;

    border: 2px solid white !important;  /* ✅ white outline */
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #007a29 !important;
}

/* LABELS */
label {
    color: white !important;
    font-weight: 500 !important;
}

/* LEFT SIDE TEXT */
.left-title {
    color: green;
    text-align: center;
    margin-top: 20px;
    font-size: 22px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# AGE FUNCTION
# =========================
def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

# =========================
# DATABASE FUNCTIONS
# =========================
def register_user(data):
    try:
        existing = session.query(User).filter_by(username=data["username"]).first()

        if existing:
            return False

        user = User(**data)
        session.add(user)
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        st.error(f"Database error: {e}")
        return False


def login_user(username, password):
    return session.query(User).filter_by(
        username=username,
        password=password
    ).first()

# =========================
# LOGIN PAGE
# =========================
if st.session_state.page == "login":

    left, right = st.columns([1, 1])

    # =========================
    # LEFT PANEL (GREEN)
    # =========================
    with left:

        st.image("public/logos/abaca_logo.png", width=500)

        st.markdown("""
            <div class="left-title">
                ABACA FARMING SYSTEM
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # RIGHT PANEL (WHITE - LOGIN)
    # =========================
    with right:

        st.subheader("Logins")

        with st.form("login_form"):

            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")


            login_btn = st.form_submit_button(
                "Sign In",
                use_container_width=True
            )

            register_btn = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if login_btn:
                user = login_user(username, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user.firstname

                    st.success(f"Welcome {user.firstname}")

                    st.switch_page("pages/dashboard.py")
                else:
                    st.error("Invalid credentials")

            if register_btn:
                st.session_state.page = "register"
                st.rerun()

# =========================
# REGISTER PAGE
# =========================
else:

    left, right = st.columns([1, 1])

    # LEFT PANEL (GREEN)
    with left:

        st.image("public/logos/abaca_logo.png", width=500)

        st.markdown("""
            <div class="left-title">
                ABACA FARMING SYSTEM
            </div>
        """, unsafe_allow_html=True)

    # RIGHT PANEL (WHITE - REGISTER)
    with right:

        st.subheader("Create Account")

        with st.form("register_form"):

            firstname = st.text_input("First Name")
            middlename = st.text_input("Middle Name")
            lastname = st.text_input("Last Name")

            username_reg = st.text_input("Username")

            password_reg = st.text_input(
                "Password",
                type="password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )

            create_btn = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            back_btn = st.form_submit_button(
                "Back to Login",
                use_container_width=True
            )

            # =========================
            # CREATE ACCOUNT
            # =========================
            if create_btn:

                if password_reg != confirm:
                    st.error("Passwords do not match")

                elif (
                    not firstname or
                    not lastname or
                    not username_reg or
                    not password_reg
                ):
                    st.error("Please fill all required fields")

                else:

                    data = {
                        "firstname": firstname,
                        "middlename": middlename,
                        "lastname": lastname,
                        "username": username_reg,
                        "password": password_reg
                    }

                    if register_user(data):

                        st.success(
                            "Account created successfully!"
                        )

                        st.session_state.page = "login"
                        st.rerun()

                    else:
                        st.error("Username already exists")

            # =========================
            # BACK BUTTON
            # =========================
            if back_btn:
                st.session_state.page = "login"
                st.rerun()
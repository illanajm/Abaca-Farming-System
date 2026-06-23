import streamlit as st
import bcrypt
from datetime import date
from database import User, session, UserRole
from utils.ui import hide_streamlit_ui
from auth import load_permissions

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Abaca Farming System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_ui()

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

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def login_user(username, password):
    user = (
        session.query(User, UserRole)
        .join(UserRole, User.role_id == UserRole.id)
        .filter(User.username == username)
        .first()
    )

    if not user:
        return None

    db_user, role = user

    if not check_password(password, db_user.password):
        return None

    return {
        "user": db_user,
        "role": role
    }

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

            if login_btn:
                result = login_user(username, password)

                if result:
                    db_user = result["user"]
                    role = result["role"]

                    st.session_state.logged_in = True
                    st.session_state["user_id"] = db_user.id
                    st.session_state["user"] = db_user.username

                    st.session_state["role_id"] = role.id
                    st.session_state["role_name"] = role.code

                    load_permissions()

                    st.success(f"Welcome {db_user.firstname}")

                    st.switch_page("pages/dashboard.py")
                else:
                    st.error("Invalid credentials")
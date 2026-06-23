import streamlit as st
from auth import has_permission

def logout():
    st.session_state.clear()
    st.switch_page("app.py")  # adjust if needed

def render_sidebar():

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

        role_name = st.session_state.get("role_name", "Guest")
        user = st.session_state.get("user", "Guest")

        st.page_link("pages/dashboard.py", label="🏠 Dashboard")
        st.page_link("pages/farmers.py", label="👨‍🌾 Farmers")
        st.page_link("pages/farms.py", label="🌱 Farms")
        st.page_link("pages/cultivation.py", label="🌾 Cultivation")
        st.page_link("pages/pest_management.py", label="🐛 Pest Management")
        st.page_link("pages/soil_management.py", label="🧪 Soil Management")
        st.page_link("pages/reports.py", label="📊 Analytics & Reports")

        if role_name == "Admin":
            st.page_link("pages/users.py", label="👥 User Management")

        if has_permission("manage_references"):
            st.page_link("pages/references.py", label="📚 Reference Data")

        st.markdown("---")

        # Push profile section to bottom
        st.markdown("<div style='height:120px'></div>", unsafe_allow_html=True)

        # Clickable settings/logout
        with st.popover("⚙️ Account"):
            st.markdown(f"""
            <div style="text-align:center;">
                <div style="
                    width:70px;
                    height:70px;
                    border-radius:50%;
                    background:#16a34a;
                    color:white;
                    font-size:28px;
                    font-weight:bold;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    margin:auto;">
                    {user[0].upper()}
                </div>
                <h4>{user}</h4>
                <p>{role_name}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Logout", use_container_width=True):
                st.session_state.clear()
                st.switch_page("app.py")
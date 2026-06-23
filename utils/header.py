import streamlit as st

def render_header():

    user = st.session_state.get("user", "Guest")
    role = st.session_state.get("role", "encoder")

    role_colors = {
        "admin": "#e74c3c",
        "staff": "#3498db",
        "encoder": "#2ecc71"
    }

    color = role_colors.get(role, "#777")

    st.markdown(f"""
    <style>

    .header-box {{
        background: white;
        padding: 12px 18px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }}

    .title {{
        font-size: 18px;
        font-weight: 800;
        color: #0b6e4f;
    }}

    .right {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 10px;
    }}

    .role-badge {{
        background: {color};
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }}

    .avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #0b6e4f;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }}

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER ROW (MAIN AREA ONLY)
    # =========================
    col1, = st.columns([3])
    with col1:
        inner1, inner2 = st.columns([5, 1])

        with inner1:
            st.markdown(f"""
            <div class="header-box">
                <div class="right">
                    <div class="avatar">{user[0].upper() if user else "U"}</div>
                    <span>{user}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
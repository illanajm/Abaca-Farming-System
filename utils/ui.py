import streamlit as st

def hide_streamlit_ui():
    st.markdown("""
    <style>

    /* Hide top toolbar (3 dots menu) */
    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Hide header */
    [data-testid="stHeader"] {
        display: none !important;
    }

    /* Hide main menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Remove extra top spacing */
    .block-container {
        padding-top: 1rem !important;
    }

    /* Hide default toolbar */
    [data-testid="stToolbar"] {
        display: none;
    }
    /* Hide default decoration */
    [data-testid="stDecoration"] {
        display: none;
    }
    /* Hide default status widget */
    [data-testid="stStatusWidget"] {
        display: none;
    }

    </style>
    """, unsafe_allow_html=True)


def apply_global_css():
    st.markdown("""
    <style>

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

            /* Sidebar buttons */
        .stButton button {
            width: 100%;
            border-radius: 12px !important;
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

        [data-testid="stPopover"] button {
            background: #16a34a !important;
            color: white !important;
            width: 250px;
        }
    </style>
    """, unsafe_allow_html=True)


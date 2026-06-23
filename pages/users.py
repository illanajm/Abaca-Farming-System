import streamlit as st
import pandas as pd
import bcrypt

from database import session, User, UserRole, Permission, RolePermission
from auth import is_admin
from utils.ui import hide_streamlit_ui, apply_global_css
from utils.sidebar import render_sidebar
from utils.header import render_header

# =========================
# ACCESS CONTROL
# =========================
if not is_admin():
    st.error("Access Denied: Admins only")
    st.stop()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="User Management", layout="wide")

hide_streamlit_ui()
render_sidebar()
apply_global_css()
render_header()

st.title("User Management")

# =========================
# PASSWORD HASH
# =========================
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# =========================
# LOAD DATA
# =========================
users = session.query(User).all()
roles = session.query(UserRole).all()
permissions = session.query(Permission).all()

role_map = {r.code: r.id for r in roles}
perm_map = {p.code: p.id for p in permissions}

# =========================
# USERS TABLE
# =========================
st.subheader("Existing Users")

df = pd.DataFrame([
    {
        "No": i + 1,
        "Username": u.username,
        "Role": session.query(UserRole).filter_by(id=u.role_id).first().code
    }
    for i, u in enumerate(users)
])

st.dataframe(df, use_container_width=True, hide_index=True)

# =========================
# ADD USER
# =========================
st.divider()
st.subheader("Add New User")

with st.form("add_user_form"):

    firstname = st.text_input("First Name")
    middlename = st.text_input("Middle Name (Optional)")
    lastname = st.text_input("Last Name")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role_code = st.selectbox("Role", list(role_map.keys()))

    submit = st.form_submit_button("Create User")

    if submit:
        if not username or not password:
            st.warning("Please fill all required fields")

        elif session.query(User).filter_by(username=username).first():
            st.error("Username already exists")

        else:
            new_user = User(
                firstname=firstname,
                middlename=middlename,
                lastname=lastname,
                username=username,
                password=hash_password(password),
                role_id=role_map[role_code]
            )

            session.add(new_user)
            session.commit()

            st.success("User created successfully")
            st.rerun()

# =========================
# UPDATE USER ROLE
# =========================
st.divider()
st.subheader("Update User Role")

user_map = {u.username: u.id for u in users}

selected_user = st.selectbox("Select User", list(user_map.keys()))
new_role = st.selectbox("New Role", list(role_map.keys()))

if st.button("Update Role"):
    user = session.query(User).filter_by(id=user_map[selected_user]).first()

    if user:
        user.role_id = role_map[new_role]
        session.commit()
        st.success("Role updated successfully")
        st.rerun()

# =========================
# DELETE USER
# =========================
st.divider()
st.subheader("Delete User")

delete_user = st.selectbox("Select User to Delete", list(user_map.keys()), key="delete")

if st.button("Delete User"):
    user = session.query(User).filter_by(id=user_map[delete_user]).first()

    if user:
        session.delete(user)
        session.commit()
        st.success("User deleted successfully")
        st.rerun()

# =========================
# ROLE → PERMISSION MANAGEMENT
# =========================
st.divider()
st.subheader("Role Permissions Management")

selected_role = st.selectbox("Select Role", list(role_map.keys()))
selected_role_id = role_map[selected_role]

# existing permissions
existing_perms = session.query(RolePermission.permission_id)\
    .filter(RolePermission.role_id == selected_role_id)\
    .all()

existing_perm_ids = [p[0] for p in existing_perms]
existing_perm_codes = [
    p.code for p in permissions if p.id in existing_perm_ids
]

selected_permissions = st.multiselect(
    "Assign Permissions",
    list(perm_map.keys()),
    default=existing_perm_codes
)

if st.button("Save Permissions"):

    # delete old permissions
    session.query(RolePermission).filter_by(role_id=selected_role_id).delete()

    # insert new permissions
    for perm_code in selected_permissions:
        session.add(RolePermission(
            role_id=selected_role_id,
            permission_id=perm_map[perm_code]
        ))

    session.commit()

    st.success("Permissions updated successfully")
    st.rerun()
import streamlit as st
from database import session, Permission, RolePermission


def load_permissions():
    role_id = st.session_state.get("role_id")

    if not role_id:
        st.session_state["permissions"] = []
        return

    perms = (
        session.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .filter(RolePermission.role_id == role_id)
        .all()
    )

    permissions = [p[0] for p in perms]

    st.session_state["permissions"] = permissions

def has_permission(permission_code: str):
    permissions = st.session_state.get("permissions")

    if not permissions:
        return False

    return permission_code in permissions


def is_admin():
    return st.session_state.get("role_name") == "Admin"


def is_staff():
    return st.session_state.get("role_name") == "Staff"


def is_encoder():
    return st.session_state.get("role_name") == "Encoder"


def can_delete():
    return has_permission("delete")


def can_manage_users():
    return has_permission("manage_users")


def can_manage_references():
    return has_permission("manage_references")
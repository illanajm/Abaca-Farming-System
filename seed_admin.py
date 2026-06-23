from database import session
from database import User, UserRole, Permission, RolePermission
from pages.users import hash_password

def seed_roles():
    roles = [
        ("Admin", "Full system access"),
        ("Staff", "Can manage records and limited actions"),
        ("Encoder", "Data entry only")
    ]

    for code, desc in roles:
        existing = session.query(UserRole).filter_by(code=code).first()
        if not existing:
            session.add(UserRole(code=code, description=desc))

    session.commit()


def seed_permissions():
    perms = [
        ("manage_users", "Create, update, delete users"),
        ("delete", "Delete records and entries"),
        ("manage_references", "Manage master/reference data")
    ]

    for code, desc in perms:
        existing = session.query(Permission).filter_by(code=code).first()
        if not existing:
            session.add(Permission(code=code, description=desc))

    session.commit()

    session.commit()


def seed_role_permissions():
    role_map = {
        "Admin": ["manage_users", "delete", "manage_references"],
        "Staff": ["delete", "manage_references"],
        "Encoder": []
    }

    for role_code, permissions in role_map.items():
        role = session.query(UserRole).filter_by(code=role_code).first()

        if not role:
            continue

        for perm_code in permissions:
            perm = session.query(Permission).filter_by(code=perm_code).first()

            if not perm:
                continue

            existing = session.query(RolePermission).filter_by(
                role_id=role.id,
                permission_id=perm.id
            ).first()

            if not existing:
                session.add(RolePermission(
                    role_id=role.id,
                    permission_id=perm.id
                ))

    session.commit()


def create_admin():
    existing = session.query(User).filter_by(username="superadmin").first()

    if existing:
        print("Admin already exists")
        return

    admin_user = User(
        firstname="Super",
        middlename="",
        lastname="Admin",
        username="superadmin",
        password=hash_password("admin123"),
        role_id=1  # Assuming the Admin role has ID 1
    )

    session.add(admin_user)
    session.commit()
    print("Admin created successfully!")

if __name__ == "__main__":
    seed_roles()
    seed_permissions()
    seed_role_permissions()
    create_admin()
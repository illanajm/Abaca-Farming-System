from database import session, User

try:
    test_user = User(
        firstname="Test",
        lastname="User",
        username="test123",
        password="1234"
    )

    session.add(test_user)
    session.commit()

    print("Inserted successfully")

except Exception as e:
    session.rollback()
    print("Error:", e)
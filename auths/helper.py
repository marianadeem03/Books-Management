from auths.models import User


def CreateUser(email, password, username, role):
    try:
        add_user = User(
            email=email,
            password=password,
            username=username,
            role=role,
        )
        add_user.set_password(password)
        add_user.save()
        return add_user
    except Exception:
        return None

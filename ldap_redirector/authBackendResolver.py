from auth_backends import instagram_backend
def get_auth_backend(name):
    if name == "instagram":
        return instagram_backend
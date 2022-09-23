from .auth_backends import instagram_backend
def get_auth_backend(name, chrome_binary_path, chrome_version):
    if name == "instagram":
        return instagram_backend.InstagramBackend(chrome_binary_path, chrome_version)
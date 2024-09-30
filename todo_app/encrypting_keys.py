from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_key(key):
    fernet = Fernet(settings.FERNET_KEY)
    return fernet.encrypt(key.encode()).decode()

def decrypt_key(key):
    fernet = Fernet(settings.FERNET_KEY)
    return fernet.decrypt(key.encode()).decode()
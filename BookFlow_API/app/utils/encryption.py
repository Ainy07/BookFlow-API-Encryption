from builtins import isinstance, str
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

def get_cipher():
    key = settings.AES_SECRET_KEY
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def encrypt_data(data: str) -> str:
    cipher = get_cipher()
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()

def decrypt_data(encrypted_data: str) -> str:
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()

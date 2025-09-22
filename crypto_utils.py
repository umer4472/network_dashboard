from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

# Load key from .env
SECRET_KEY = os.getenv("ENCRYPTION_KEY")

if not SECRET_KEY:
    raise ValueError("ENCRYPTION_KEY is missing from .env file")

# No need to .encode() if the key is already stored correctly
fernet = Fernet(SECRET_KEY)

def encrypt_value(value: str) -> str:
    """Encrypt a plain string value"""
    return fernet.encrypt(value.encode()).decode()

def decrypt_value(token: str) -> str:
    """Decrypt an encrypted string value"""
    return fernet.decrypt(token.encode()).decode()

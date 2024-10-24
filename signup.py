import bcrypt
import os
from utils import generate_key_pair

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one number.")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter.")

def sign_up(username, password):
    validate_password(password)
    
    public_key_pem, private_key_pem = generate_key_pair()

    password_hash = hash_password(password)

    with open("public_keys.txt", "a") as pub_file:
        pub_file.write(f"USERNAME:{username}\nPASSWORD_HASH:{password_hash.decode('utf-8')}\n{public_key_pem.decode('utf-8')}\n\n")

    if not os.path.exists("keys"):
        os.makedirs("keys")
    
    with open(f"keys/{username}_private_key.pem", "wb") as priv_file:
        priv_file.write(private_key_pem)
    
    os.chmod(f"keys/{username}_private_key.pem", 0o600)

    print(f"User {username} signed up successfully. Private key stored in 'keys/{username}_private_key.pem'.")

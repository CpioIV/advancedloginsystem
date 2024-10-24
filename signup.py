import os
from utils import generate_key_pair

def sign_up(username):
    public_key_pem, private_key_pem = generate_key_pair()

    with open("public_keys.txt", "a") as pub_file:
        pub_file.write(f"USERNAME:{username}\n{public_key_pem.decode('utf-8')}\n\n")

    if not os.path.exists("keys"):
        os.makedirs("keys")
    
    with open(f"keys/{username}_private_key.pem", "wb") as priv_file:
        priv_file.write(private_key_pem)

    print(f"User {username} signed up successfully. Private key stored in 'keys/{username}_private_key.pem'.")

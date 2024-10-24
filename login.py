import os
from utils import load_private_key, sign_challenge, verify_signature

def get_public_key_from_file(username):
    try:
        with open("public_keys.txt", "r") as pub_file:
            lines = pub_file.readlines()
            public_key_pem = []
            capturing = False

            for line in lines:
                if line.strip().startswith(f"USERNAME:{username}"):
                    capturing = True  # Found the user
                elif capturing and line.startswith("-----BEGIN PUBLIC KEY-----"):
                    public_key_pem.append(line)
                elif capturing and line.startswith("-----END PUBLIC KEY-----"):
                    public_key_pem.append(line)
                    break
                elif capturing:
                    public_key_pem.append(line)

            if public_key_pem:
                return "".join(public_key_pem).encode('utf-8')
            else:
                return None
    except FileNotFoundError:
        print("Public keys file not found.")
        return None


def login(username):
    challenge = os.urandom(32)
    
    private_key = load_private_key(f"keys/{username}_private_key.pem")
    signature = sign_challenge(challenge, private_key)

    public_key_pem = get_public_key_from_file(username)
    print(f"Retrieved public key for {username}: {public_key_pem}")

    if not public_key_pem:
        print(f"Error: Public key for {username} not found!")
        return

    if verify_signature(public_key_pem, signature, challenge):
        print(f"User {username} authenticated successfully.")
    else:
        print(f"Authentication failed for user {username}.")

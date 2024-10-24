import bcrypt
import os
import time
from utils import verify_signature, sign_challenge, load_private_key

failed_attempts = {}

def check_password(stored_password_hash, input_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password_hash.encode('utf-8'))

def get_public_key_and_password_hash_from_file(username):
    try:
        with open("public_keys.txt", "r") as pub_file:
            lines = pub_file.readlines()
            public_key_pem = []
            stored_password_hash = None
            capturing = False

            for line in lines:
                if line.strip().startswith(f"USERNAME:{username}"):
                    capturing = True  # Found the user
                elif capturing and line.startswith("PASSWORD_HASH:"):
                    stored_password_hash = line.split(":")[1].strip()
                elif capturing and line.startswith("-----BEGIN PUBLIC KEY-----"):
                    public_key_pem.append(line)
                elif capturing and line.startswith("-----END PUBLIC KEY-----"):
                    public_key_pem.append(line)
                    break
                elif capturing:
                    public_key_pem.append(line)

            if public_key_pem and stored_password_hash:
                return "".join(public_key_pem).encode('utf-8'), stored_password_hash
            else:
                return None, None
    except FileNotFoundError:
        print("Public keys file not found.")
        return None, None

def rate_limit(username):
    global failed_attempts
    attempts = failed_attempts.get(username, {'count': 0, 'last_attempt': time.time()})
    
    if attempts['count'] >= 3 and (time.time() - attempts['last_attempt'] < 5):
        print("Too many failed attempts. Please wait before trying again.")
        return False
    
    return True

def log_failed_attempt(username):
    global failed_attempts
    attempts = failed_attempts.get(username, {'count': 0, 'last_attempt': time.time()})
    attempts['count'] += 1
    attempts['last_attempt'] = time.time()
    failed_attempts[username] = attempts

def login(username, password):
    if not rate_limit(username):
        return

    public_key_pem, stored_password_hash = get_public_key_and_password_hash_from_file(username)
    
    if not public_key_pem or not stored_password_hash:
        print(f"Error: User {username} not found!")
        return

    if not check_password(stored_password_hash, password):
        print("Incorrect password!")
        log_failed_attempt(username)
        return

    challenge = os.urandom(32)
    
    private_key = load_private_key(f"keys/{username}_private_key.pem")
    signature = sign_challenge(challenge, private_key)

    if verify_signature(public_key_pem, signature, challenge):
        print(f"User {username} authenticated successfully.")
        failed_attempts[username] = {'count': 0, 'last_attempt': time.time()}
    else:
        print(f"Authentication failed for user {username}.")
        log_failed_attempt(username)

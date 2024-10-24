users_db = {}

def store_user_public_key(username, public_key_pem):
    users_db[username] = public_key_pem
    print(f"Stored public key for user {username}.")

def get_public_key_from_db(username):
    public_key_pem = users_db.get(username)
    if public_key_pem is None:
        print(f"Public key not found for user {username}")
    return public_key_pem
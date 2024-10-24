from signup import sign_up
from login import login

def main():
    print("1. Sign Up")
    print("2. Log In")
    choice = input("Choose an option: ")

    if choice == "1":
        username = input("Enter username: ")
        sign_up(username)
    elif choice == "2":
        username = input("Enter username: ")
        login(username)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()

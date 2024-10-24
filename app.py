from signup import sign_up
from login import login

def main():
    print("1. Sign Up")
    print("2. Log In")
    option = input("Choose an option: ")

    if option == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        try:
            sign_up(username, password)
        except ValueError as e:
            print(f"Error during sign-up: {e}")
    elif option == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(username, password)
    else:
        print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

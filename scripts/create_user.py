# take input from user


import re


def input_password():
    password = input("Enter password: ")
    return password


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{7}$"

    if re.match(pattern, password):
        return True
    else:
        return False


def main():
    print("Enter email: ")
    email = input()
    print("Enter password: ")
    # cehck password using regex to match 7 in lentgh, 1 uppercase, 1 lowercase, 1 number
    password = input()

    if not validate_password(password):
        print(
            "Password must be at least 7 characters long, contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"
        )
        return


if __name__ == "__main__":
    main()

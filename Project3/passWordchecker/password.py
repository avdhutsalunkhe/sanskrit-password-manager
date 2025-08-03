def is_strong_password(password):
    # Check length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # Check for uppercase letter
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."

    # Check for lowercase letter
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."

    # Check for digit
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."

    # Check for special character
    special_characters = "!@#$%^&*"
    if not any(char in special_characters for char in password):
        return False, "Password must contain at least one special character (!@#$%^&*)."

    return True, "Password is strong!"

# Main program
password = input("Enter your password: ")
status, message = is_strong_password(password)
print(message)


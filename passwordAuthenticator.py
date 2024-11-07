old_passwords = []


# Check if the length of password is atleast 10 charcters or not.
def checkLength(new_password):
    if len(new_password) < 10:
        print("Password must be at least 10 characters long")
        return False
    return True


# Counting number of different types of characters
# type_count[0] =>digits
# type_count[1] =>Uppercase character
# type_count[2] =>Lowercase character
# type_count[3] =>Special characters
def check_count_Character(new_password):
    type_count = [0, 0, 0, 0]

    for char in new_password:
        if ord(char) > 47 and ord(char) < 58:
            type_count[0] = type_count[0] + 1
        elif ord(char) > 64 and ord(char) < 91:
            type_count[1] = type_count[1] + 1
        elif ord(char) > 96 and ord(char) < 123:
            type_count[2] = type_count[2] + 1
        else:
            type_count[3] += 1

    # Error based on number of characters
    if type_count[0] < 2:
        print("Password must contains atleast 2 digits between 0-9.")
    if type_count[1] < 2:
        print("Password must contain atleast two uppercase characters")
    if type_count[2] < 2:
        print("Password must contain atleast two lowercase characters")
    if type_count[3] < 2:
        print("Password must contain atleast two special characters")
    if type_count[0] < 2 or type_count[1] < 2 or type_count[2] < 2 or type_count[3] < 2:
        return False
    else:
        return True


# The password should not contain any sequence of three or more consecutive characters from the username
def username_pass_match_check(username, new_password):
    for i in range(len(new_password) - 2):
        if new_password[i : i + 3] in username:
            print(
                "More than two consecutive characters from username avaialble in password"
            )
            return False
    return True


# No character should repeat more than three times in a row
def character_repeat_check(new_password):
    for i in range(len(new_password) - 3):
        if (
            new_password[i]
            == new_password[i + 1]
            == new_password[i + 2]
            == new_password[i + 3]
        ):
            print("More than three consecutive same characters")
            return False
    return True


# ● The new password must not be the same as the last three passwords used by the user.
def old_new_match_check(new_password):
    for old_pass in old_passwords:
        if new_password == old_pass:
            print("New password same as old password")
            return False
    return True


def password_checker():
    username = input("Enter username : ")
    print("\nEnter your last 3 passwords")
    for x in range(3):
        old_passwords.append(input(f"Enter password {x+1} : "))
    correct = False
    while correct == False:
        new_password = input("\nEnter new password : ")
        if checkLength(new_password) == False:
            continue
        elif check_count_Character(new_password) == False:
            continue
        elif username_pass_match_check(username, new_password) == False:
            continue
        elif character_repeat_check(new_password) == False:
            continue
        elif old_new_match_check(new_password) == False:
            continue
        else:
            print("Congratulations!! password set successfully.")


print("\n\n")
print(
    "************************This is a Password Authentication System******************************\n\n"
)
print(
    "Please ensure following points while creating a new password:\n\nThe password must be at least 10 characters long.\nCharacter Variety: It must contain at least:\n● Two uppercase letters.\n● Two lowercase letters.\n● Two digit\n● Two special characters (e.g., @, #, $, %, &, *, !).\n\nSequence and Repetition Restrictions:\n● The password should not contain any sequence of three or more consecutive characters from the username .\n● No character should repeat more than three times in a row (e.g., 'aaa' is allowed, but 'aaaa' is not).\n\nHistorical Password Check:\n● The new password must not be the same as the last three passwords used by the user)\n"
)
password_checker()

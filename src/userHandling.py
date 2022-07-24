import hashlib
import pickle
import sys

from src import logging
import fileSystem

current_user = {}


class UserNotFoundException(BaseException):
    def __init__(self, username: str):
        super().__init__(f"User {username} does not exist on this system")


with open("users.dat", "rb") as g:
    users = pickle.load(g)
logging.log("UserHandler", "Initialization", "Users have been registered and indexed", False)


def __get_user__(username: str) -> dict:
    """Searches for a user and returns it"""
    logging.log("UserHandler", "Fetch.Request", f"User {username} has been requested", False)
    for i in range(0, len(users)):
        if users[i]["name"] == username:
            logging.log("UserHandler", "Fetch.Success", f"User {username} has been fetched", False)
            return users[i]
    logging.log("UserHandler", "Fetch.Failure", f"User {username} has not been found", False)
    raise UserNotFoundException(username)


def __check_user__(username: str) -> bool:
    logging.log("UserHandler", "Check.Request", f"User {username} has been requested to be checked", False)
    for i in range(0, len(users)):
        if users[i]["name"] == username:
            logging.log("UserHandler", "Check.Success", f"User {username} has been checked: positive", False)
            return True
    logging.log("UserHandler", "Check.Failure", f"User {username} has been checked: negative", False)
    return False


def __check_pw__(username: str, pw: str) -> bool:
    logging.log("UserHandler", "PasswordCheck.Request", f"A password check for user {username} has been requested",
                False)
    try:
        user = __get_user__(username)
        if user["password"] == hashlib.sha512(pw.encode()).digest():
            logging.log("UserHandler", "PasswordCheck.Success", f"The password check for user {username} was successful",
                        False)
            return True
        else:
            logging.log("UserHandler", "PasswordCheck.Failure", f"The password check for user {username} failed", False)
    except UserNotFoundException:
        return False


def add(username: str, password: str, admin: str):
    logging.log("UserHandler", "ADD.Request", f"The addition of user {username} has been requested", False)
    if not __check_user__(username):
        user = {
            "name": username,
            "password": hashlib.sha512(password.encode()).digest(),
            "admin": "y" in admin.lower()
        }
        users.append(user)
        save()
        fileSystem.new_user(username)
        logging.log("UserHandler", "ADD.Success", f"User {username} has been added", False)
        print(f"User {username} has been added")
    else:
        print(f"ERROR: User {username} already exists")
    logging.log("UserHandler", "ADD.Failure", f"User {username} cannot be added (Already exists)")


def delete(username: str):
    logging.log("UserHandler", "DELETE.Request", f"The deletion of user {username} has been requested", False)
    try:
        user = __get_user__(username)
    except UserNotFoundException:
        print(f"ERROR: User {username} does not exist")
        return
    print("WARNING: This will delete ALL the data for the user!")
    if input("Continue? (Y/N): ").lower() == "y":
        for i in range(len(users)):
            if users[i] == user:
                del users[i]
        save()
        fileSystem.delete_user(username)
        logging.log("UserHandler", "DELETE.Success", f"User {username} has been deleted", False)
        print(f"User {username} has been deleted")


# noinspection SpellCheckingInspection
def change_name(username: str, new_name: str):
    logging.log("UserHandler", "NAMECHANGE.Request", f"A name change for user {username} was requested")
    try:
        __get_user__(username)
    except UserNotFoundException:
        print(f"ERROR: User {username} does not exist")
        return
    for i in range(0, len(users)):
        if users[i]["name"] == username:
            users[i]["name"] = new_name
            save()
            logging.log("UserHandler", "NAMECHANGE.Success", f"User {username} has been renamed to {new_name}")


# noinspection SpellCheckingInspection
def change_pw(username: str, pw_old: str, pw_new: str):
    logging.log("UserHandler", "PWCHANGE.Request", f"A password change for user {username} was requested")
    try:
        __get_user__(username)
    except UserNotFoundException:
        print(f"ERROR: User {username} does not exist")
        return
    for i in range(0, len(users)):
        if users[i]["name"] == username:
            if __check_pw__(username, pw_old):
                users[i]["password"] = hashlib.sha512(pw_new.encode()).digest()
                save()
                logging.log("UserHandler", "PWCHANGE.Success", f"The password for user {username} has been changed")
            else:
                print("ERROR: Wrong password provided")
                return


def login():
    global current_user
    while current_user == {}:
        username = input("Username: ")
        if username.lower() == "exit":
            sys.exit()
        password = input("Password: ")
        logging.log("UserHandler", "LoginRequest", f"A login request for user {username} has been made", False)
        try:
            user = __get_user__(username)
            if __check_pw__(username, password):
                current_user = user
                logging.log("UserHandler", "LoginSuccess", f"The login request for user {username} was successful",
                            False)
            else:
                print("Incorrect password")
                logging.log("UserHandler", "LoginFailurePassword", f"The login request for user {username} has failed "
                                                                   f"due to an incorrect password", False)
        except UserNotFoundException:
            print("That user does not exist on this system")
            logging.log("UserHandler", "LoginFailureUser", f"The login request for user {username} has failed due to "
                                                           f"a non-existent user", False)


def save():
    with open("users.dat", "wb") as f:
        pickle.dump(users, f)

from typing import List

from src import userHandling

user = {}


def initialize(info: dict):
    global user
    user = info["user"]
    return main


def main(com: List[str]):
    if len(com) > 1:
        option = com[1]
    else:
        print("Available sub-commands:\n1. add\n2. edit\n3. delete")
        command = input("Option (1/2/3): ")
        try:
            option = ["add", "edit", "delete"][int(command) - 1]
        except ValueError:
            print("ERROR: Invalid option (1/2/3)")
            return
        except IndexError:
            print("ERROR: Invalid option (1/2/3)")
            return
    if option == "add":
        if len(com) > 2:
            username = com[2]
        else:
            username = input("Username: ")
        if len(com) > 3:
            password = com[3]
        else:
            password = input("Password: ")
        if user["admin"]:
            if len(com) > 4:
                admin = com[4]
            else:
                admin = input("Admin (Y/N): ")
            if len(com) > 5:
                print("ERROR: Too many arguments")
                return
        else:
            admin = "n"
            if len(com) > 4:
                print("ERROR: Too many arguments")
                return
        userHandling.add(username, password, admin)

    elif option == "edit":
        if len(com) > 2:
            sub_option = com[2]
        else:
            print("Available options:\n1. username\n2. password")
            command = input("Option (1/2): ")
            try:
                sub_option = ["username", "password"][int(command) - 1]
            except ValueError:
                print("ERROR: Invalid option (1/2)")
                return
            except IndexError:
                print("ERROR: Invalid option (1/2)")
                return
        if sub_option == "username":
            if len(com) > 3:
                username_old = com[3]
            else:
                username_old = input("Old Username: ")
            if not user["admin"] and username_old != user["name"]:
                print("ERROR: Insufficient permissions")
                return
            if len(com) > 4:
                username_new = com[4]
            else:
                username_new = input("New Username: ")
            if len(com) > 5:
                print("ERROR: Too many arguments")
                return
            userHandling.change_name(username_old, username_new)
        elif sub_option == "password":
            if len(com) > 3:
                username = com[3]
            else:
                username = input("Username: ")
            if not user["admin"] and username != user["name"]:
                print("ERROR: Insufficient permissions")
                return
            if len(com) > 4:
                password_old = com[4]
            else:
                password_old = input("Old Password: ")
            if len(com) > 5:
                password_new = com[5]
            else:
                password_new = input("New Password: ")
            if len(com) > 6:
                print("ERROR: Too many arguments")
                return
            userHandling.change_pw(username, password_old, password_new)

    elif option == "delete":
        if len(com) > 2:
            username = com[2]
        else:
            username = input("Username: ")
        userHandling.delete(username)
    else:
        print("ERROR: Unknown sub-command (add/edit/delete)")
        return

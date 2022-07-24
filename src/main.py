import os

from src import logging
import userHandling
import commandInterpreter
import fileSystem


if __name__ == "__main__":
    logging.init()

    userHandling.login()
    os.system("cls" if os.name == "nt" else "clear")
    print("==================================================PythOS==================================================")
    print("Logged in as " + userHandling.current_user["name"] +
          (" (Admin)" if userHandling.current_user["admin"] else ""))
    fileSystem.initialize(userHandling.current_user)
    commandInterpreter.initialize(userHandling.current_user)

from src import logging
import json
import sys
import os

import fileSystem

current_user = {}
running = True

PROMPT = "§"

info = {}

group_mapping = {}

INFO_REQUIRE_ADMIN = []
INFO_REQUIRE_CONFIRM = [
    "escape"
]


def initialize(user: dict):
    global current_user, info
    current_user = user
    info = {
        "user": current_user,
        "escape": escape,
        "files": fileSystem
    }
    sys.path.append(os.path.abspath("commands"))
    try:
        with open("commands/group_index.json") as f:
            group_index = json.load(f)
    except FileNotFoundError:
        logging.log("Shell", "Index_Error", f"Group index has not been found!", False, True)
        return
    for group in group_index:
        for command in group["commands"]:
            group_mapping[command] = group["location"]
        sys.path.append(os.path.abspath(f"./commands{group['location']}"))
    while running:
        com = input(PROMPT)
        run(com)


def escape():
    global running
    running = False


def run(command: str):
    com = command.split(" ")
    group = ""
    if com[0] in group_mapping.keys():
        group = group_mapping[com[0]]
    try:
        with open(f"./commands{group}/{com[0]}.json") as f:
            com_info = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Command {com[0]} has not been found!")
        logging.log("Shell", "RUN_Error", f"Command {com[0]} has not been found!", False)
        return
    else:
        try:
            admin_required = com_info["security"]["admin_required"]
            ask_before_running = com_info["security"]["ask_before_run"]
            required_info = com_info["required_info"]
        except KeyError:
            print(f"ERROR: Command {com[0]} is incompatible!")
            logging.log("Shell", "RUN_Error", f"Command {com[0]} is incompatible! (Missing crucial information in "
                                              f"info-file)", False)
            return
        else:
            passed_info = {}
            for key in required_info:
                try:
                    passed_info[key] = info[key]
                except KeyError:
                    print(f"ERROR: Command {com[0]} asked for non-existent info!")
                    logging.log("Shell", "RUN_Error", f"Command {com[0]} asked for non-existent info! ({key})", False)
                    return
                else:
                    if not admin_required:
                        admin_required = key in INFO_REQUIRE_ADMIN
                    if not ask_before_running:
                        ask_before_running = key in INFO_REQUIRE_CONFIRM
            if admin_required:
                if not current_user["admin"]:
                    print(f"Error: Command {com[0]} requires admin permissions!")
                    logging.log("Shell", "RUN_Error", f"Command {com[0]} requires admin permissions!", False)
                    return
            if ask_before_running:
                if "y" not in input("Are you sure you want to run this command (Y/N)? ").lower():
                    return
        try:
            com_module = __import__(com_info["executable"])
            com_func = com_module.initialize(passed_info)
        except ImportError:
            print(f"ERROR: Command {com[0]} has not been found!")
            logging.log("Shell", "RUN_Error", f"Command {com[0]} executable has not been found!", False)
            return
        except AttributeError:
            print(f"ERROR: Command {com[0]} is incompatible!")
            logging.log("Shell", "RUN_Error", f"Command {com[0]} is incompatible! (Missing initialization function)",
                        False)
            return
        except TypeError:
            print(f"ERROR: Command {com[0]} is incompatible!")
            logging.log("Shell", "RUN_Error", f"Command {com[0]} is incompatible! (Incorrect initialization function - "
                                              f"Unmatching args count)", False)
            return
        else:
            if type(com_func) != type(initialize):
                print(f"ERROR: Command {com[0]} is incompatible!")
                logging.log("Shell", "RUN_Error",
                            f"Command {com[0]} is incompatible! (Incorrect initialization function - "
                            f"Incorrect return type)", False)
                return
            try:
                com_func(com)
            except TypeError:
                print(f"ERROR: Command {com[0]} is incompatible!")
                logging.log("Shell", "RUN_Error",
                            f"Command {com[0]} is incompatible! (Incorrect initialization function - "
                            f"Incorrect argument type)", False)
                return


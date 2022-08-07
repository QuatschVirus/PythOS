import os
import json
from src import logging

from typing import List, Tuple


# noinspection PyUnusedLocal
def initialize(info: dict):
    return main


def main(com: List[str]):
    logging.log("Commands", "Help", f"Help was requested (Clause: {com})", False)
    coms = {}
    group_coms = []
    try:
        with open("./commands/group_index.json") as f:
            group_index = json.load(f)
    except FileNotFoundError:
        logging.log("Shell", "Index_Error", f"Group index has not been found!", False, True)
        return
    for group in group_index:
        for command in group["commands"]:
            group_coms.append(os.path.join(group["location"][1:], command + ".json"))
    for path in os.listdir("./commands") + group_coms:
        if "." in path and "group_index.json" not in path:
            if len(path.split(".")) > 1:
                if path.split(".")[0] not in coms.keys() and path.split(".")[-1] == "json":
                    logging.log("Commands", "Help", f"Indexing command file: {path}", False)
                    try:
                        with open("./commands/" + path) as f:
                            data = json.load(f)
                        name = path.split(".")[0].split("\\")[-1].split("/")[-1]
                        coms[name] = (data["general"]["description"], data["general"]["usage"])
                    except FileNotFoundError:
                        pass
    print("Arguments within () are mandatory, arguments within [] are optional. Wildcards used, everything in \"\" is "
          "literal. / is used to differentiate paths, {} indicates multiple options within the same path. - indicates "
          "no argument for this branch on this level")
    if len(com) > 1:
        for command in com[1:]:
            print_out(command, coms[command])
    else:
        for command in coms.keys():
            print_out(command, coms[command])


def print_out(com: str, data: Tuple[str, str]):
    print(f"{com}: {data[0]}. Usage: {data[1]}")

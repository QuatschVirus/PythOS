files = __import__("fileSystem")


def initialize(info: dict):
    global files
    files = info["files"]
    return main


def main(com: list):
    files.cd(com[1] if len(com) > 1 else "")

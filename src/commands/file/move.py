files = __import__("fileSystem")


def initialize(info: dict):
    global files
    files = info["files"]
    return main


def main(com: list):
    files.move(com[1], com[2])

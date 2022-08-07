from typing import List

from src import logging


def __func__():
    pass


escape_func = __func__


def initialize(info: dict):
    global escape_func
    escape_func = info["escape"]
    return main


# noinspection PyUnusedLocal
def main(com: List[str]):
    logging.log("Commands", "Shutdown", "The system has been shut down", False)
    escape_func()

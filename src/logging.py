import time
import sys

MAIN_LOG = "./logs/system.log"
TIME_FORMAT = "[%a %d-%m-%Y %H:%M:%S]"


def init():
    with open(MAIN_LOG, "w") as g:
        g.write(time.strftime(TIME_FORMAT) + ": System.Logger.Initialization: This is the start of the main system "
                                             "log files\n")


def log(host: str, typus: str, msg: str, verbose=False, fatal=False):
    log_str = time.strftime(TIME_FORMAT) + ": " + host + "." + typus + ": " + msg + "\n"
    with open(MAIN_LOG, "a") as g:
        g.write(log_str)
    if verbose:
        print(log_str)
    if fatal:
        sys.exit(host + "." + typus + ": " + msg)

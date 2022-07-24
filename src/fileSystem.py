import os
import shutil

current_user = {}

EDITOR_PATH = os.path.abspath("ressources/editor/editor")
DEFAULT_README_PATH = os.path.abspath("ressources/default_readme.txt")

DEFAULT_PATH = os.path.abspath("files")
FILES_PATH = os.path.abspath("files")
current_path = os.path.abspath("files")


def __accessing_other_user(path: str):
    chk_path = os.path.realpath(os.path.abspath(path))
    if chk_path.startswith(FILES_PATH):
        return not chk_path.startswith(DEFAULT_PATH)
    return False


def initialize(user: dict):
    global current_user, current_path, DEFAULT_PATH
    current_user = user
    current_path = os.path.join(current_path, user["name"])
    DEFAULT_PATH = current_path


def new_user(username: str):
    try:
        os.mkdir(os.path.abspath(os.path.join(os.path.abspath("files"), username)))
        shutil.copy2(DEFAULT_README_PATH, os.path.join(os.path.abspath("files"), username, "readme.txt"))
        os.symlink(os.path.abspath("files/global"), os.path.abspath(os.path.join("files", username, "global")))
    except FileExistsError:
        pass


def mkdir(path: str):
    if not os.path.abspath(os.path.join(current_path, path)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, path)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not in your file tree")
        return
    try:
        os.mkdir(os.path.join(current_path, path))
    except FileExistsError:
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} does already exist")
    except FileNotFoundError:
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path, ''))} does not exist")


def rename(path: str, new_name: str):
    if not os.path.exists(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, path))} does not exist")
        return
    if not os.path.isfile(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not an editable file")
        return
    if not os.path.abspath(os.path.join(current_path, path)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, path)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not in your file tree")
        return
    dst = list(os.path.split(os.path.join(current_path, path)))
    dst[-1] = "/" + new_name
    out = ""
    for fol in dst:
        out += fol
    os.rename(os.path.abspath(os.path.join(current_path, path)), os.path.abspath(out))


def editfile(path: str):
    if not os.path.exists(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, path))} does not exist")
        return
    if not os.path.abspath(os.path.join(current_path, path)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, path)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not in your file tree")
        return
    if not os.path.isfile(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not an editable file")
        return
    os.system(os.path.abspath(EDITOR_PATH) + " " + os.path.abspath(os.path.join(current_path, path)))


def __del__(path: str):
    if os.path.isfile(os.path.join(current_path, path)):
        os.remove(os.path.join(current_path, path))
    elif os.path.isdir(os.path.join(current_path, path)):
        for sub_path in os.listdir(os.path.join(current_path, path)):
            __del__(os.path.join(os.path.join(current_path, path), sub_path))
        os.rmdir(os.path.join(current_path, path))


def delete(path: str):
    global current_path
    if not os.path.exists(os.path.join(current_path, path)):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, path))} does not exist")
        return
    if not os.path.abspath(os.path.join(current_path, path)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, path)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not in your file tree")
        return
    __del__(os.path.join(current_path, path))
    if os.path.abspath(os.path.join(current_path, path)) in os.path.abspath(current_path):
        current_path = os.path.abspath(os.path.join(current_path, path, ""))


def copy(source: str, destination: str):
    if not os.path.abspath(os.path.join(current_path, source)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, source)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, source))} is not in your file tree")
        return
    if not os.path.abspath(os.path.join(current_path, destination)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, destination)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, destination))} is not in your file tree")
        return
    if not os.path.exists(os.path.join(current_path, source)):
        print(f"ERROR: File {os.path.join(current_path, source)} does not exist")
    if os.path.isdir(os.path.join(current_path, source)):
        shutil.copytree(os.path.join(current_path, source), os.path.join(current_path, destination))
    else:
        shutil.copy2(os.path.join(current_path, source), os.path.join(current_path, destination))


def move(source: str, destination: str):
    copy(source, destination)
    delete(source)


def ls(path: str):
    if not os.path.exists(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, path))} does not exist")
        return
    if not os.path.isdir(os.path.abspath(os.path.join(current_path, path))):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not a folder")
        return
    if not os.path.abspath(os.path.join(current_path, path)).startswith(DEFAULT_PATH) or __accessing_other_user(
            os.path.join(current_path, path)):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, path))} is not in your file tree")
        return
    for subs in os.listdir(os.path.join(current_path, path)):
        print(subs)


def cd(path: str):
    global current_path
    new_path = os.path.abspath(os.path.join(current_path, path))
    if not os.path.exists(new_path):
        print(f"ERROR: File {new_path} does not exist")
        return
    if not os.path.isdir(new_path):
        print(f"ERROR: {new_path} is not a folder")
        return
    if not new_path.startswith(DEFAULT_PATH) or __accessing_other_user(new_path):
        print(f"ERROR: {new_path} is not in your file tree")
        return
    current_path = new_path


def mount(source: str, destination: str, link: bool):
    if not os.path.exists(os.path.abspath(os.path.join(current_path, source))):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, source))} does not exist")
        return
    if not os.path.isdir(os.path.abspath(os.path.join(current_path, source))):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, source))} is not a folder")
        return
    if not os.path.abspath(os.path.join(current_path, source)).startswith(DEFAULT_PATH) and link:
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, source))} is not your file tree")
        return
    if os.path.exists(os.path.abspath(os.path.join(current_path, destination))):
        print(f"ERROR: File {os.path.abspath(os.path.join(current_path, destination))} already exists")
        return
    if not os.path.abspath(os.path.join(current_path, destination)).startswith(DEFAULT_PATH):
        print(f"ERROR: {os.path.abspath(os.path.join(current_path, destination))} is not your file tree")
        return
    os.symlink(os.path.abspath(os.path.join(current_path, source)),
               os.path.abspath(os.path.join(current_path, destination)),
               target_is_directory=True)


def delete_user(username: str):
    global current_path
    cache = current_path
    current_path = os.path.abspath(os.path.join("files", username))
    delete("/")
    current_path = cache

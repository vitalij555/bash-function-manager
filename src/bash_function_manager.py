#!/usr/bin/env python3
import pwd
import sys
import re
import os

from function_registry import JsonKeyValueStore


LINK_DIR = "/usr/local/bin"  # Change this to the desired directory
SCRIPTS_FOLDER_NAME = "scripts"
MASTER_SCRIPT_NAME = "my_functions_master.sh"
MASTER_SCRIPT_PATH = os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME, MASTER_SCRIPT_NAME)
DB_PATH = "/usr/local/bash_function_registry/registry.json"


def get_real_user():
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user is not None:
        return sudo_user
    return pwd.getpwuid(os.getuid())[0]


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)


def ensure_file_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a') as f:
        pass



def register(script_name):
    if script_name.startswith('.') or '\\' in script_name or '/' in script_name:  #we have relative path
        script_full_path = os.path.abspath(os.path.join(os.getcwd(), script_name))
    else:
        script_full_path = os.path.abspath(script_name)

    with open(script_full_path, 'r') as f:
        script_contents = f.read()

    function_regex = r"(?<!#private\n)function\s+(\w+)\s*\n*\(*\)*\s*\n*\{([\s\S]*?)\}\n*(?=\s*$)"

    function_defs = re.findall(function_regex, script_contents, re.DOTALL | re.MULTILINE | re.UNICODE)

    # ensure_directory_exists(os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME))

    script_destination_full_path = os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME, script_name)
    ensure_directory_exists(os.path.dirname(script_destination_full_path))

    with open(script_destination_full_path, 'w') as script_f:
        script_f.write(script_contents)

    print("#"*50 + "\n\n")
    for name, contents in function_defs:
        link_path = os.path.join(LINK_DIR, name)
        print(f"Registering {name} from {script_destination_full_path}")
        print(f"Function contents is {contents}")
        print("#"*50 + "\n\n")

        with open(link_path, 'w') as f:
            f.write(f"""#!/bin/bash
source {script_destination_full_path}
{name} "$@"
""")

        real_user = get_real_user()
        uid = pwd.getpwnam(real_user).pw_uid
        gid = pwd.getpwnam(real_user).pw_gid

        # Change the owner of the file
        os.chown(link_path, uid, gid)

        # Change the permissions of the file to allow owner read, write, and execute
        os.chmod(link_path, 0o700)


        # os.chmod(link_path, 0o755)
        # ensure_directory_exists(os.path.dirname(MASTER_SCRIPT_PATH))

        # with open(MASTER_SCRIPT_PATH, 'a+') as master_f:
        #     master_f.seek(0)
        #     master_contents = master_f.read()

        # function_regex = r"function\s+" + re.escape(name) + r"\s*\n*\(*\)*\n*\{([\s\S]*?)\}\n*(?=\s*$)"
        # match = re.search(function_regex, master_contents)

        # # condition below is used to understand whether we "update existing" or "insert new one".
        # if match:
        #     start_idx = match.start()
        #     end_idx = match.end()
        #     updated_master_contents = master_contents[:start_idx] + f"\nfunction {name}\n" + "{" + contents + "\n}" + master_contents[end_idx:]
        # else:
        #     updated_master_contents = master_contents + f"\n\nfunction {name}\n" + "{" + contents + "\n}"

        # with open(MASTER_SCRIPT_PATH, 'w') as master_f:
        #     master_f.write(updated_master_contents)

        
        ensure_file_exists(DB_PATH)
        registry = JsonKeyValueStore(DB_PATH)
        registry.set(name, script_full_path)
        registry.save()
        


def list_commands():
    ensure_file_exists(DB_PATH)
    store = JsonKeyValueStore(DB_PATH)  

    for key in store.data.keys():
        print(key)


def edit_command(command_name):
    ensure_file_exists(DB_PATH)
    store = JsonKeyValueStore(DB_PATH)  
    if command_name in store.data:
        source_file = store.data[command_name]
        os.system(f"xdg-open {source_file}")


if __name__ == "__main__":
    if sys.argv[0].endswith("register"):
        if len(sys.argv) > 1:
            register(sys.argv[1])
        else:
            print("Error: Script file name is missing!")
            print("""Usage:
            register script_name""")
    elif sys.argv[0].endswith("list_commands"):
        list_commands()
    elif sys.argv[0].endswith("edit_command"):
        edit_command(sys.argv[1])
    else:
        print("Unknown command")

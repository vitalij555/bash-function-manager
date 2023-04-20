#!/usr/bin/env python3

import sys
import re
import os

LINK_DIR = "/usr/local/bin"  # Change this to the desired directory
SCRIPTS_FOLDER_NAME = "scripts"
MASTER_SCRIPT_NAME = "my_functions_master.sh"
MASTER_SCRIPT_PATH = os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME, MASTER_SCRIPT_NAME)


def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)


def register(script_name):
    with open(script_name, 'r') as f:
        script_contents = f.read()

    function_regex = r"function\s+(\w+)\s*{([\s\S]*?)}(?=\s*$)"
    function_defs = re.findall(function_regex, script_contents, re.DOTALL | re.MULTILINE | re.UNICODE)

    ensure_directory_exists(os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME))

    script_destination_full_path = os.path.join(LINK_DIR, SCRIPTS_FOLDER_NAME, script_name)
    ensure_directory_exists(os.path.dirname(script_destination_full_path))

    with open(script_destination_full_path, 'w') as script_f:
        script_f.write(script_contents)

    for name, contents in function_defs:
        link_path = os.path.join(LINK_DIR, name)

        with open(link_path, 'w') as f:
            f.write(f"""#!/bin/bash
source {script_destination_full_path}
{name} "$@"
""")
        os.chmod(link_path, 0o755)

        ensure_directory_exists(os.path.dirname(MASTER_SCRIPT_PATH))

        with open(MASTER_SCRIPT_PATH, 'a+') as master_f:
            master_f.seek(0)
            master_contents = master_f.read()

        function_regex = r"function\s+" + re.escape(name) + r"\s*{([\s\S]*?)}(?=\s*$)"
        match = re.search(function_regex, master_contents)

        if match:
            start_idx = match.start()
            end_idx = match.end()
            updated_master_contents = master_contents[:start_idx] + f"\nfunction {name}\n" + "{" + contents + "\n}" + master_contents[end_idx:]
        else:
            updated_master_contents = master_contents + f"\n\nfunction {name}\n" + "{" + contents + "\n}"

        with open(MASTER_SCRIPT_PATH, 'w') as master_f:
            master_f.write(updated_master_contents)


def list_commands():
    try:
        with open(MASTER_SCRIPT_PATH, 'r') as f:
            contents = f.read()
    except FileNotFoundError:
        print("There is no registered commands yet")
        return

    function_regex = r"function\s+(\w+)\s*{"
    matches = re.findall(function_regex, contents)
    if not matches:
        print("There is no registered commands yet")
        return
    matches.sort()

    max_len = max(map(len, matches))
    num_cols = max(1, os.get_terminal_size().columns // (max_len + 2))

    for i, name in enumerate(matches):
        if i % num_cols == 0:
            print()
        print(f"{name:{max_len}}", end='  ')

    print()


if __name__ == "__main__":
    if sys.argv[0].endswith("register"):
        register(sys.argv[1])
    elif sys.argv[0].endswith("list_commands"):
        list_commands()
    else:
        print("Unknown command")

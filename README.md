# Bash Function Manager

Manage and organize Bash functions with this command-line utility. Easily register functions from Bash scripts, create soft links for quick access, and list all registered functions.

## Features

- Register functions from a Bash script
- Create soft links for individual functions in a specified directory
- List all registered functions
- Update or create function definitions in a master script

## Installation

Run the installer script to install the required dependencies and make the commands "register" and "list_commands" available system-wide:

```bash
./install.sh
```

## Usage

Register a script containing Bash functions:

```bash
register /path/to/your_script.sh
```

List all registered commands:

```bash
list_commands
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
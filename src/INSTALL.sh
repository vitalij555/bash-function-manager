#!/bin/bash

chmod +x bash_function_manager.py
ln -sf $(pwd)/bash_registry.py /usr/local/bin/register
ln -sf $(pwd)/bash_registry.py /usr/local/bin/list_commands

#!/bin/bash

# Get the directory path of the script
script_dir="$(cd "$(dirname "$0")" && pwd)"

# Set the Python interpreter path
python_interpreter="$script_dir/venv/bin/python"

# Set the Python script path
python_script="$script_dir/main.py"

# Set the configuration argument
config_arg="-c $script_dir/config"

# Run the Python script with the configuration argument
$python_interpreter $python_script $config_arg

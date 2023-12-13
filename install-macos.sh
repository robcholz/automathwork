#!/bin/bash

# Get the directory path of the script
script_dir="$(cd "$(dirname "$0")" && pwd)"
# Set the Python interpreter path
python_interpreter="python3"

# create venv
$python_interpreter -m venv "$script_dir"/venv
# activate venv
source "$script_dir"/venv/bin/activate

# install deps
pip install PyQt5
pip install PyQtWebEngine
pip install httpx
pip install httpx[socks]
pip install openai

# use pandoc
pandoc_version="3.1.9"
mkdir "$script_dir"/cache
# Set the URL of the zip file to download
pandoc_arch=""
if [[ $(uname -m) == 'arm64' ]]; then
  echo "Arch: arm64"
  pandoc_arch="arm64"
else
  echo "Arch: x86_64"
  pandoc_arch="x86_64"
fi
zip_url="https://github.com/jgm/pandoc/releases/download/$pandoc_version/pandoc-$pandoc_version-$pandoc_arch-macOS.zip"
# Set the path where the zip file will be downloaded
zip_file="$script_dir/cache/pandoc.zip"
# Set the directory where the zip file will be extracted
extract_dir="$script_dir/cache"
# Set the destination directory for the binary file
destination_dir="$script_dir/config"
# Download the zip file
# Extract the contents of the zip file
echo "Download pandoc from $zip_url"
curl -L "$zip_url" --output "$zip_file" && unzip "$zip_file" -d "$extract_dir"
# Copy the binary file to the destination directory
cp "$extract_dir/pandoc-$pandoc_version-$pandoc_arch/bin/pandoc" "$destination_dir"
# delete download cache
rm -r "$extract_dir"

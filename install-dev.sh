#!/usr/bin/env bash
# install-dev.sh is a script that installs the development dependencies and activates the virtual environment.
set -e

./install.sh

echo "Installing dev dependencies..."
pip install -r requirements-dev.txt
echo "Installation complete!"

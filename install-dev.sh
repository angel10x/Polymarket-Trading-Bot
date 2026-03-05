#!/usr/bin/env bash

set -e

./install.sh

echo "Installing dev dependencies..."
pip install -r requirements-dev.txt
echo "Installation complete!"

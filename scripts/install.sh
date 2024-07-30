#!/bin/bash
# install.sh

cd ../

# Update and install required packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-dev libffi-dev libssl-dev alsa-utils mpg123 redis-server

# Install Python dependencies
pip3 install -r src/requirements.txt

# Set permissions for the audio devices
sudo usermod -aG audio ${USER}

# Enable and start the Redis server
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo "Installation complete. Please log out and log back in for changes to take effect."

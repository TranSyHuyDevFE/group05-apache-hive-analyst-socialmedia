#!/bin/bash
set -e
#!/bin/bash
# Update and upgrade system packages
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install required dependencies
echo "Installing dependencies..."
sudo apt install -y software-properties-common curl

# Add deadsnakes PPA
echo "Adding deadsnakes PPA..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.11
echo "Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-distutils

# Install pip for Python 3.11
echo "Installing pip for Python 3.11..."
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11

# Add Python 3.11 to alternatives system
echo "Setting Python 3.11 as a selectable alternative..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Prompt user to select default python3 version
echo "To set Python 3.11 as default, select it from the list:"
sudo update-alternatives --config python3

# Verify installation
echo "Verifying Python and pip versions..."
python3.11 --version
python3.11 -m pip --version
python3 --version

echo "✅ Python 3.11 installation complete."

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
supervisord -c supervisord.conf

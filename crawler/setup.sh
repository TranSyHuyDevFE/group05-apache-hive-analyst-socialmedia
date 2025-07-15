#!/bin/bash
set -e
sudo apt update && sudo apt install -y python3 && sudo apt install -y python-pip
pip install -r requirements.txt
supervisord -c supervisord.conf 

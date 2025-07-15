#!/bin/bash
set -e
sudo apt update && sudo apt install -y python3.11 python3.11-venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
supervisord -c supervisord.conf

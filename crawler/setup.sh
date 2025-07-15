#!/bin/bash
set -e
pip install -r requirements.txt
supervisord -c supervisord.conf 

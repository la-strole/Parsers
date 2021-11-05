#!/bin/bash
path_line='/home/ub/Documents/GIT/parsers'
python3 -m venv "$path_line/parsers_venv" &>> "$path_line/log.txt"
source "$path_line/parsers_venv/bin/activate" &>> "$path_line/log.txt"
pip install -r "$path_line/requirements.txt" &>> "$path_line/log.txt"
python "$path_line/main.py" &>> "$path_line/log.txt"
deactivate

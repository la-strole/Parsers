#!/bin/bash
path_line='/home/ub/Documents/GIT/parsers'
source "$path_line/venv/bin/activate" &>> "$path_line/log.txt"
python "$path_line/main.py" &>> "$path_line/log.txt"
deactivate

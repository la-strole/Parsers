#!/bin/bash
path_line='/home/ub/Documents/GIT/parsers'
source "$path_line/parsers_venv/bin/activate" &>> "$path_line/log.txt"
python "$path_line/main.py" -path "$path_line/" &>> "$path_line/log.txt"
deactivate

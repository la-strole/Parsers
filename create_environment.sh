path_line='/home/ub/Documents/GIT/parsers'
python3 -m venv "$path_line/parsers_venv" &>> "$path_line/log.txt"
source "$path_line/parsers_venv/bin/activate" &>> "$path_line/log.txt"
pip install -r "$path_line/requirements.txt" &>> "$path_line/log.txt"
wget -P "$path_line/" https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz
tar -xvzf geckodriver-v0.30.0-linux32.tar.gz
rm geckodriver-v0.30.0-linux32.tar.gz
deactivate

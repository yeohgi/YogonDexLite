#!/bin/bash
# install httpd (Linux 2 version)
yum update -y

#install
yum install -y httpd
yum install -y php
yum install -y tmux
yum install -y git
yum install python3-pip -y

#pip install
pip3 install dask
pip3 install fuzzywuzzy
pip3 install pandas
pip3 install python-Levenshtein

#create a new directory to import YogonDexLite files
mkdir -p ydl
cd ydl

git clone https://github.com/yeohgi/YogonDexLite.git .

#create a new tmux session to let the server run indefinitly
tmux new-session -d -s myserver "python3 server.py 80"
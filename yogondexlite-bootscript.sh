#!/bin/bash
# Use this for your user data (script from top to bottom)
# install httpd (Linux 2 version)
yum update -y

#install
yum install -y httpd
yum install -y php
yum install -y tmux
yum install -y git

yum install python3-pip -y
pip3 install dask
pip3 install fuzzywuzzy
pip3 install pandas
pip3 install python-Levenshtein

mkdir -p ydl
cd ydl

git clone https://github.com/yeohgi/YogonDexLite.git .

tmux new-session -d -s myserver "python3 awsserver.py 58061"
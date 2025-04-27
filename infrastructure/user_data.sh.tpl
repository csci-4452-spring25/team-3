#!/bin/bash
# Update and install dependencies
yum update -y
yum install -y git python3 python3-pip

# Create a directory for the bot
cd /home/ec2-user

# Clone GitHub repo
git clone https://github.com/csci-4452-spring25/team-3.git
cd team-3

# Install Python dependencies
pip3 install -r requirements.txt

# Run the Python script
nohup python3 infrastructure/Code/bot.py &
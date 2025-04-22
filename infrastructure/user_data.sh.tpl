#!/bin/bash
# Update and install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip

# Create a directory for the bot
mkdir -p /home/ubuntu/discord-bot

# Write bot code
cat <<EOF > /home/ubuntu/discord-bot/bot.py
${python_script}
EOF

# Create the .env file
cat <<EOF > /home/ubuntu/discord-bot/.env
${env_file}
EOF

# Write requirements.txt
cat <<EOF > /home/ubuntu/discord-bot/requirements.txt
${requirements}
EOF

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Run the Python script
python3 /home/ubuntu/discord-bot/bot.py
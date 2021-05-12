#!/bin/sh

## update and setup dependencies
sudo apt update
sudo apt -y upgrade
sudo apt -y install git unzip python3-pip

## setup script server
pip3 install tornado

cd /home/ubuntu
wget https://github.com/bugy/script-server/releases/latest/download/script-server.zip
unzip script-server.zip -d script-server
rm script-server.zip

## setup script server configs
cd /home/ubuntu/script-server/conf
rm -rf *
git clone https://github.com/uh-soco/script-server-configs.git .

sudo chown -R ubuntu /home/ubuntu/script-server/
sudo chgrp -R ubuntu /home/ubuntu/script-server/

## start script server
cd /home/ubuntu
echo "[Unit]
Description=Script server automatic server management tool
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/script-server/launcher.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target" > script-server.service
sudo mv /home/ubuntu/script-server.service /etc/systemd/system/
sudo chmod 755 /etc/systemd/system/script-server.service
sudo systemctl daemon-reload
sudo systemctl enable script-server.service
sudo systemctl start script-server.service

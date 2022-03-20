#!/bin/bash

/usr/bin/git pull
echo "Restarting tempest service"
sudo systemctl restart tempest

chmod +x update.sh

/home/pi/tempest-eink/venv/bin/python /home/pi/tempest-eink/main.py



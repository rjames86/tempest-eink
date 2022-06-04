#!/bin/bash

/usr/bin/git pull
echo "Restarting tempest service"
sudo systemctl restart tempest

chmod +x update.sh



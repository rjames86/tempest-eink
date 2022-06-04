#!/bin/bash

/usr/bin/git pull
echo "Restarting tempest service"
sudo systemctl restart tempest

chmod a+x update.sh



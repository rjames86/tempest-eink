# tempest-eink

## Installation

    sudo apt-get update
    sudo apt-get upgrade
    
    sudo apt-get install git python3-pip libopenjp2-7 libatlas-base-dev nginx
    sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools ufw python3-venv
    sudo ufw enable
    sudo ufw allow 'Nginx HTTP'
    
    sudo raspi-config
    # Interface options
    # Enable SPI
    
    git clone https://github.com/rjames86/tempest-eink
    
    # Set up the web server
    # Pulled from https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
    
    
    python3 -m venv venv
    source venv/bin/activate
    
    
    
    pip3 install wheel gunicorn flask
    pip3 install -r requirements.txt
    
    sudo ufw allow 5000
    
    sudo nano /etc/systemd/system/tempest.service
    
    
Put this in the file
    
    [Unit]
    Description=Ryans Tempest E-ink Project
    After=network.target
    
    [Service]
    User=pi
    Group=www-data
    
    WorkingDirectory=/home/pi/tempest-eink/server
    Environment="PATH=/home/pi/tempest-eink/venv/bin"
    ExecStart=/home/pi/tempest-eink/venv/bin/gunicorn --bind unix:tempest.sock -m 007 wsgi:app
    
    [Install]
    WantedBy=multi-user.target


    sudo systemctl start tempest
    sudo systemctl enable tempest
    
    sudo nano /etc/nginx/sites-available/tempest
    
Put this in the file

    server {
        listen 80;
        server_name tempest-eink.local;
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/sammy/myproject/server/tempest.sock;
        }
    }
    

    sudo ln -s /etc/nginx/sites-available/tempest /etc/nginx/sites-enabled/
    
    sudo ufw delete allow 5000
    sudo ufw allow 'Nginx Full'
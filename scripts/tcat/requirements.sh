#!/bin/sh

## install requirements
sudo apt -y install php-mbstring libmysqlclient-dev mariadb-plugin-tokudb php-curl php-mysql
## geo?
pip3 install -r requirements.txt

sudo /etc/init.d/apache2 reload

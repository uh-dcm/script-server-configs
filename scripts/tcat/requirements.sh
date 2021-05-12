#!/bin/sh

## install requirements
sudo apt -y install php-mbstring libmysqlclient-dev mariadb-plugin-tokudb php-curl
## geo?
pip3 install -r requirements.txt

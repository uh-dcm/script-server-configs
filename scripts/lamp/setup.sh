#!/bin/sh

cd /home/ubuntu/script-server/conf/scripts/lamp

## LAMP setup
sudo apt -y install apache2
sudo apt -y install php libapache2-mod-php
sudo systemctl restart apache2

### add ubuntu to www-data group
sudo adduser ubuntu www-data
chmod -R 777 /var/www/html/

## setup mysql

ADMIN_PASS=$( tr -cd '[:alnum:]' < /dev/urandom | fold -w50 | head -n1 )
if [ ! -f ~/mysql_admin.txt ]; then
  echo $ADMIN_PASS > ~/mysql_admin.txt
fi

sudo apt -y install mysql-server mysql-client python3-dev default-libmysqlclient-dev build-essential

yes | sudo apt install expect

./mysql.sh $ADMIN_PASS

echo ""
echo ""
echo "[OK] LAMP setup succesful. Will reboot, come back in a minute."

sudo shutdown -r 1

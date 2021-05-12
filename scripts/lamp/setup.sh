## LAMP setup
yes | sudo apt install apache2
yes | sudo apt-get install php libapache2-mod-php
sudo systemctl restart apache2

### add ubuntu to www-data group
sudo adduser ubuntu www-data

## setup mysql

ADMIN_PASS=$( tr -cd '[:alnum:]' < /dev/urandom | fold -w50 | head -n1 )
echo $ADMIN_PASS > ~/mysql_admin.txt

yes | sudo apt-get install mysql-server mysql-client python3-dev default-libmysqlclient-dev build-essential

yes | sudo apt install expect

./mysql.sh $ADMIN_PASS

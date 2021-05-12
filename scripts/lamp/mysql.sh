#!/usr/bin/expect

spawn sudo mysql -u root -p
expect "Enter password: "
send -- "\r"
expect "mysql> "
send -- "CREATE USER 'admin'@'localhost' IDENTIFIED BY '$1';\r"
expect "mysql> "
send -- "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;\r"
expect "mysql> "
send -- "FLUSH PRIVILEGES;\r"
expect "mysql> "
send -- "quit\r"

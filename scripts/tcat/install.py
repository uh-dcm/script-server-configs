#!/usr/bin/python3

## install dependencies
import os
os.system('cd %s; ./requirements.sh' % ( os.path.dirname( __file__ ) ) )

import os
import sys
import argparse
import git
import re
import secrets
from sqlalchemy import create_engine
from crontab import CronTab
import shutil

parser = argparse.ArgumentParser(description='Setups DMI-TCAT.')
parser.add_argument('--email', dest='admin_email')
parser.add_argument('--project', dest='project')
parser.add_argument('--twitter_consumer_key', dest='twitter_consumer_key')
parser.add_argument('--twitter_consumer_secret', dest='twitter_consumer_secret')
parser.add_argument('--twitter_user_token', dest='twitter_user_token')
parser.add_argument('--twitter_user_secret', dest='twitter_user_secret')

args = parser.parse_args()

clean = lambda str: re.sub(r"\s+", '_', re.sub(r"[^\w\s-]", '', str.lower() ) )

proper_project = clean( args.project )

install_path = '/var/www/html/'
install_path += proper_project + '/'

try:
    git.Repo.clone_from('https://github.com/digitalmethodsinitiative/dmi-tcat.git', install_path )
except:
    print("Copying instance [FAIL]")
    quit(-1)

print("Copying instance [OK]")

## setup database

mysql_root_password = open('/home/ubuntu/mysql_admin.txt').read().strip()

user_password = secrets.token_hex( 50 )

try:
    ## todo: SQL injections?
    engine = create_engine('mysql://admin:%s@localhost' % mysql_root_password, echo=True)
    connection = engine.connect()
    connection.execute( "CREATE DATABASE tcat_%s;" % proper_project )
    connection.execute( "GRANT ALL PRIVILEGES ON tcat_{0}.* TO 'tcat_{0}'@'localhost' IDENTIFIED BY '{1}';".format( proper_project, user_password ) )
    connection.execute( "FLUSH PRIVILEGES;" )
    connection.close()
    print("Database [OK]")
except:
    print("Database [FAIL]")
    quit(-1)


## setup configurations

config = open( install_path + '/config.php.example', 'r' ).read()

## generic config
config = config.replace('$database = "twittercapture";', '$database = "tcat_%s";' % proper_project )
config = config.replace('$mail_to = "";', '$mail_to = "%s";' % args.admin_email )
config = config.replace('$dbuser = "";\n$dbpass = "";', '$dbuser = "tcat_%s";\n$dbpass = "%s";' % (proper_project, user_password ) )

## twitter config
config = config.replace( '$twitter_consumer_key = "";', '$twitter_consumer_key = "%s";' % args.twitter_consumer_key )
config = config.replace( '$twitter_consumer_secret = "";', '$twitter_consumer_secret = "%s";' % args.twitter_consumer_secret )
config = config.replace( '$twitter_user_token = "";', '$twitter_user_token = "%s";' % args.twitter_user_token )
config = config.replace( '$twitter_user_secret = "";', '$twitter_user_secret = "%s";' % args.twitter_user_secret )

## todo: check how to make these sane
config = config.replace("define('ADMIN_USER', serialize(array('admin', 'admin2')));", "// define('ADMIN_USER', serialize(array('admin', 'admin2')));")
config = config.replace("define('MYSQL_ENGINE_OPTIONS', 'ENGINE=TokuDB COMPRESSION=TOKUDB_LZMA');", "// define('MYSQL_ENGINE_OPTIONS', 'ENGINE=TokuDB COMPRESSION=TOKUDB_LZMA');")


open( install_path + '/config.php', 'w' ).write( config )

print("Configurations [OK]")

## create required folders and setup permissions for them

try:
    for folder in ['analysis/cache/', 'logs/', 'proc/']:
        folder = install_path + folder
        os.makedirs( folder , 0o755 )
        shutil.chown( folder , group = 'www-data' )
    print("Creating folders [OK]")
except:
    print("Creating folders [FAIL]")
    quit(-1)

## setup cronjobs

cron = CronTab(user='ubuntu')
job = cron.new(command='(cd {0}capture/stream/; php controller.php)'.format( install_path ) )
job.minute.every(1)
cron.write()

print("Recurrency [OK]")

print("DMI-TCAT installation [OK]")

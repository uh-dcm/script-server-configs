#!/usr/bin/python3
import sys
import argparse
import git
import re
import secrets
from sqlalchemy import create_engine

parser = argparse.ArgumentParser(description='Setups DMI-TCAT.')
parser.add_argument('--email', dest='admin_email')
parser.add_argument('--project', dest='project')
parser.add_argument('--twitter_api_key', dest='twitter_api_key')

args = parser.parse_args()

clean = lambda str: re.sub(r"\s+", '_', re.sub(r"[^\w\s]", '', str.lower() ) )

proper_project = clean( args.project )

install_path = '/Users/mnelimar/code/digital-infrastructure-creator/'
install_path += proper_project + '/'

try:
    git.Repo.clone_from('https://github.com/digitalmethodsinitiative/dmi-tcat.git', install_path )
except:
    pass ## for non-debug: die, project name not unique

## setup database

mysql_root_password = input('Database root password')

user_password = secrets.token_hex( 50 )

try:
    ## todo: SQL injections?
    engine = create_engine('mysql://root:%s@localhost' % mysql_root_password, echo=True)
    connection = engine.connect()
    connection.execute( "CREATE DATABASE 'tcat_%s';" % proper_project )
    connection.execute( "GRANT ALL PRIVILEDGES ON 'tcat_%s'.* TO 'tcat_‰s'@'localhost' IDENTIFIED BY '%s';" % ( proper_project, proper_project, user_password ) )
    connection.close()
except:
    pass ## for non-debug: die, something wrong with SQL


## setup configurations

config = open( install_path + '/config.php.example', 'r' ).read()

config = config.replace('$database = "twittercapture";', '$database = "tcat_%s";' % proper_project )
config = config.replace('$mail_to = "";', '$mail_to = "%s";' % args.admin_email )
config = config.replace('$dbuser = "";\n$dbpass = "";', '$dbuser = "tcat_%s";\n$dbpass = "%s";' % (proper_project, user_password ) )

open( install_path + '/config.php3', 'w' ).write( config )

print("All done.")

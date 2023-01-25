import os


DBUSER = os.environ.get('DBUSER', 'admin')
DBPASSWORD = os.environ.get('DBPASSWORD', 'admin')
DBHOST = os.environ.get('DBHOST', 'localhost')
DBNAME = os.environ.get('DBNAME', 'postgres')
DBPORT = os.environ.get('DBPORT', '5432')
RESET_DB = os.environ.get('RESET_DB', 'False')

# Installation
Install prerequisites:
```bash
conda install -f environments.yml -n <env_name>
conda activate <env_name>
```
Set up .env file:
```python
# .env
SECRET_KEY = '<secret_key>'
DEBUG = False
ALLOWED_HOSTS = '<allowed_host>, ...'
```

## Setting up Postgresql database

````python
# api/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'userinterface_db',
        'USER': 'admin',
        'PASSWORD': '<adminpassword>',
        'HOST': 'localhost',
        'PORT': '', # default = 5432
    }
}
````

In the terminal, initialize a postgres database by:
````bash
initdb -D database
````

start the server modus/instance of postgres

````bash
pg_ctl -D database -l logfile start

#waiting for server to start.... done
#server started
````
now the server is up.


create a non-superuser (more safety!)

````bash
createuser --encrypted --pwprompt admin
# asks for name and password
````

using this super user, create inner database inside the base database

````bash
createdb --owner=admin userinterface_db
````



````python
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
````

#### Stop running the postgres instance (under ubuntu)

monitor whether a postgres instance/server is running or not
````bash
ps aux | grep postgres
````
if no instance is running, you will see only one line as the answer to your query - which is from your grep search!
ending with: grep --color=auto postgres
ignore this line!

e.g. the output of `ps aux | grep postgres` was:
````bash
# username  2673  0.0  0.0  14760   512 pts/11   S+   07:34   0:00 grep --color=auto postgres
# username 30550  0.0  0.0 179144 18996 ?        S    Jun13   0:01 /home/username/miniconda3/envs/django/bin/postgres -D mylocal_db
# username 30552  0.0  0.0 179276  4756 ?        Ss   Jun13   0:00 postgres: checkpointer process   
# username 30553  0.0  0.0 179144  5216 ?        Ss   Jun13   0:01 postgres: writer process   
# username 30554  0.0  0.0 179144  8464 ?        Ss   Jun13   0:01 postgres: wal writer process   
# username 30555  0.0  0.0 179700  5792 ?        Ss   Jun13   0:01 postgres: autovacuum launcher process   
# username 30556  0.0  0.0  34228  3416 ?        Ss   Jun13   0:03 postgres: stats collector process  
````

if an instance of postgresql server is running, then several processes are running
you can kill the server by the first number of the leading line!

````bash
kill <number>
````

then # 2673 is just the 'grep --color=auto postgres' so ignore
the line ending with 'postgres -D /path/to/mylocal_db' is the leading line!
take first number occuring in this line (PID - process ID number) which is 30550, therefore kill it by:

````bash
kill 30550
````


run postgres as a non-server in the background
````bash
postgres -D db_djangogirls & # runs postgres
````
press RET (return) to send it to background!

you can stop and switch to server mode by
following 'stop running postgres instance under ubuntu'



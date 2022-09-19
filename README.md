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

TIME_ZONE = 'Europe/Berlin'

DB_NAME = 'userinterface_db'
DB_USER = 'admin'
DB_PASSWORD = '<admin_password>'
DB_HOST = 'localhost'
DB_PORT = '5432'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = '<allowed_origins>, ... '
```

## Setting up Postgresql database

````python
# api/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
````

In the terminal (backend), initialize a postgres database by:
````bash
initdb -D database
````

start the server modus/instance of postgres

````bash
pg_ctl -D database -l logfile start

#waiting for server to start.... done
#server started
````

create a non-superuser (more safety!)

````bash
createuser --encrypted --pwprompt admin
# asks for name and password
````

using this super user, create inner database inside the base database

````bash
createdb --owner=admin userinterface_db
````
Migrations to the database need to be applied by:
```python
python3 manage.py makemigrations
python3 manage.py migrate
```
If you want to add entries to the database yourself, you need to create a superuser first:
```python
python3 manage.py createsuperuser
```
Otherwise, you can populate the database with example data (including superuser (email:'admin@admin.com', password:'admin'))
```python
django-admin loaddata init.json
```

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



run postgres as a non-server in the background:
````bash
postgres -D db_djangogirls & 
````

you can stop and switch to server mode by following 'stop running postgres instance under ubuntu'


# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

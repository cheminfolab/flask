# Installation

### Setting up the `.env` file

```python
# .env
SECRET_KEY='<secret_key>'
DEBUG=False
ALLOWED_HOSTS='<allowed_host>, ...'

TIME_ZONE='Europe/Berlin'

POSTGRES_DB='flask_database'
POSTGRES_USER='admin'
POSTGRES_PASSWORD='<admin_password>'

#CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS='<allowed_origins>, ... '
```

## Installation using Docker Containers

Install prerequisites:
- docker

## Native Installation

Install prerequisites:
- conda
- npm (node.js)

### Django

Setting up the environment:

```bash
conda install -f environment.yml
conda activate flask
```

### React

In the `frontend/` directory, run:

````bash
npm install
````

# Running the ELN instance

### Backend
````bash
docker compose up -d --build
````
or with a respective .env file:
````bash
docker compose --env-file .env up -d --build
````
### Frontend

In `frontend/`, run:

````bash
npm start
````

#### Stop running the Postgres Instance

````bash
docker compose down
````

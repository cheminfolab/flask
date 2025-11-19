# Overview

- [Overview](#overview)
- [Installation](#installation)
    - [Setting up the `.env` file](#setting-up-the-env-file)
  - [Installation using Docker Containers](#installation-using-docker-containers)
  - [Native Installation](#native-installation)
    - [Django](#django)
    - [React](#react)
- [Running the ELN instance](#running-the-eln-instance)
  - [Docker](#docker)
    - [Running a frontend development server](#running-a-frontend-development-server)
    - [Stop running the instances](#stop-running-the-instances)

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
## Docker

````bash
docker compose up -d --build
````
or with a respective .env file:
````bash
docker compose --env-file .env up -d --build
````
### Running a frontend development server

In `frontend/`, run:

````bash
npm run dev
````

### Stop running the instances

````bash
docker compose down
````

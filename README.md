# premstats ⚽️

A natural language querying system for Premier League stats. This project is comprised of 2 parts:

1. An API for all Premier League sports data
2. A frontend that parses a natural language query and returns the relevant sports statistics

Part 1 is within the `backend/` directory. This also serves Part 2. Part 2 is defined in the `frontend/` directory. 

## Usage

To use 2., you can go to this website for querying - 

To use 1., you can refer to the documentation for the API here - 

## Setup

To run this system, you only need to have Docker installed. The technology stack is as follows:

**Backend**

- FastAPI for the Python backend API.
  - SQLModel for the Python SQL database interactions (ORM).
  - Pydantic, used by FastAPI, for the data validation and settings management.
  - PostgreSQL as the SQL database.

**Frontend**

- Next.js for the frontend.
  - Using TypeScript, TailwindCSS and Vite
  - Chakra UI for the frontend components.


To develop the system further, I recommend reading through the [backend README](/backend/README.md) and [frontend README]() to understand how to setup your developer environment for these tasks.

## Running

To run this system locally, you only need to make a .env file. The docker compose file handles the rest.
Your .env file must look like this and must be placed in this directory (at the same level as the docker-compose.yml file)

```.env
# Domain
# This would be set to the production domain with an env var on deployment
DOMAIN=localhost

# Environment: local, staging, production
ENVIRONMENT=local

PROJECT_NAME=<name-of-your-project>

# Backend
BACKEND_CORS_ORIGINS="http://localhost,http://localhost:5173,https://localhost,https://localhost:5173"
SECRET_KEY=<key>
FIRST_SUPERUSER=keanejonathan3@gmail.com
FIRST_SUPERUSER_PASSWORD=<password>

# Postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Configure these with your own Docker registry images
DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_FRONTEND=frontend
```

The above .env file will ensure that your application runs locally. To run the system, do the following

```bash
docker compose up --build
```

This will do 3 things:

1. Create 3 services (db, backend, frontend) - it makes their images and starts running the containers
2. Creates a volume called app-db-data where all the database data is stored.
3. Exposes ports `localhost:5432` for the db, `localhost:8000` for the backend and `localhost:5173` for the frontend

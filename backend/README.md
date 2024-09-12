# Premstats Backend

This file documents how to work with the backend and continue development on it.

## Setup

To setup your developer environment, you will need

1. [Docker](https://docs.docker.com/desktop/)
2. [Poetry](https://python-poetry.org/docs/)

You can get them from the relevant links provided. To run the backend you only need docker 

## Running

The easiest way to run this is to run the `docker compose up --build` command in the previous directory. This boots up the database and the backend and exposes the ports necessary. Follow the instructions in the project README.md to get started on this approach.

Another way of running the server is using `uvicorn`. To do so you need to have a `.env` file in the current directory.


## Development

To continue developing this backend, you can

### Project Structure

The project structure is explained below

```
.
├── Dockerfile
├── README.md           # this file
├── alembic.ini         # alembic migrations configuration file
├── app                 # all the FastAPI code is here
│   ├── __init__.py
│   ├── __pycache__
│   ├── alembic         # migrations in this directory
│   ├── api             # all the routes are defined here 
│   ├── core            # essentials like config, db, etc.
│   ├── main.py         # entrypoint
│   ├── models.py       # the tables in the database
│   ├── pre_start.py    # prestart script like checking if the database is online, etc.
│   └── tests           # testing directory
├── fly.toml            # the configuration file for fly.io to deploy
├── poetry.lock         # lock file for Poetry
├── prestart.sh         # the prestart script (running migrations, calling app/pre_start.py, etc.)
└── pyproject.toml      # the project configuration file (Poetry dependencies, etc.) 
```

## Testing

## Deployment

I use fly.io for deploying this server to staging and production.

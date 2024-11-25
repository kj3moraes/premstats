# Development

This page documents the traditional process for documenting the project. There are 3 environment for this project

1. Local
2. Development
3. Production

Local is your quite literally your local environment (all the data and processing happens on-device, except the model calls of course). All of the components reside locally.

Development is your staging environment. This occurs only when there is a PR in review. It will activate the `premstats-dev` app in fly.io to service requests so you can test your app in a non-local setting with real data.

Production is your production environment that services users. There is no way to access the database with an API call outside of the app. You can interact with the Premstats API at `premstats.fly.dev/docs`. This sends requests to the `premstats` app in fly.io which will then service requests.

## Components

All the components are tied up neatly tied up in the `docker-compose.yaml` file. You should simply make a .env file as shown in the README.md and you should be good to go.

### Database

The database is a Postgres14 database. In the local development environment, all the data is on a volume and the `docker compose up` command brings it up.
In the development environment, this will be the `dev/<username>` branch in Neon.

For developing a new feature, it is highly recommended that you branch your database from `main`. This allows you to work on a copy of the `main` data so that you do not affect the production environment. The development backend component is auto-configured to interact with the `dev/kj3moraes` branch of the Neon database.

### Backend

The backend is written in FastAPI. It is located in the `backend` directory of this repository. Once again, in the local environment it is packaged with the `docker-compose.yaml` so all you need to do is bring it up and you can access the backend via the `localhost:8000` hostname and port.

In the development environment (i.e when a PR is open), the backend can be found in the `premstats-dev` app and can be accessed via `premstats-dev.fly.dev`. This allows you to test your backend in a non-local staging environment.j

Optionally you can push to the `premstats-dev` app outside a PR via the following command from this directory

```bash
fly  deploy -c ./backend/fly.staging.toml
```

### Frontend

The frontend is a Next.js project. It is located in the `premstats-frontend` directory. For local running, you can go to the directory and type in

```bash
pnpm i
pnpm run dev
```

All the staging and production is handled by Vercel.

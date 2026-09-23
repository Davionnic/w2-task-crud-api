# PostgreSQL Docker Setup

## Running PostgreSQL in Docker

Start PostgreSQL with persistent storage:

```bash
docker compose up db
```

This will:
- Start PostgreSQL 15 in a container
- Create a database named `tasks`
- Use persistent named volume `postgres_data` 
- Expose on port 5432
- Use default credentials: `postgres/postgres`

## Connect to Database

```bash
# Using psql (if installed locally)
psql -h localhost -p 5432 -U postgres -d tasks

# Using Docker
docker compose exec db psql -U postgres -d tasks
```

## Stop and Clean Up

```bash
# Stop containers
docker compose down

# Remove volumes (deletes data)
docker compose down -v
```
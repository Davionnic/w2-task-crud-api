# Task API with PostgreSQL

A containerized FastAPI-based CRUD API for managing tasks with PostgreSQL persistence. This project demonstrates full-stack containerization using Docker and Docker Compose.

## 🚀 Quick Setup (One Command)

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Start the entire stack:
```bash
docker compose up
```

That's it! The API will be available at `http://localhost:8000` and the interactive docs at `http://localhost:8000/docs`.

## 📋 Environment Variables

The application requires these environment variables (configured in `.env`):

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@172.17.0.1:5432/tasks` |

## 🔌 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check with database status | 200 |
| GET | `/tasks` | Get all tasks (supports `?done=true/false` and `?search=text`) | 200 |
| GET | `/tasks/{id}` | Get single task by ID | 200, 404 |
| POST | `/tasks` | Create new task | 201, 400 |
| PUT | `/tasks/{id}` | Update existing task | 200, 400, 404 |
| DELETE | `/tasks/{id}` | Delete task by ID | 204, 404 |
| GET | `/stats` | Get task statistics | 200 |
| POST | `/reset` | Reset to seed data | 200 |

## 🧪 API Examples

Here are sample curl commands demonstrating the API:

### Health Check
```bash
curl -i http://localhost:8000/health
```
```
HTTP/1.1 200 OK
date: Wed, 23 Sep 2026 10:14:22 GMT
server: uvicorn
content-length: 42
content-type: application/json

{"status":"ok","database":"connected"}
```

### Get All Tasks
```bash
curl http://localhost:8000/tasks
```

### Create a New Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker"}'
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Master Docker", "done": true}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/tasks/1 -i
```

## 🐳 Docker Architecture

### Services
- **api**: FastAPI application container
- **db**: PostgreSQL 15 database container

### Networking
- Both services run on the same Docker network
- Database accessible to API via service name `db`
- API exposed on host port 8000
- Database exposed on host port 5432 for development

### Storage
- PostgreSQL data persisted in named volume `postgres_data`
- Data survives container restarts and updates

## 🔄 Data Persistence Verification

To verify that data persists across container restarts:

1. Create some tasks:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Persistence test"}'
```

2. Stop the stack:
```bash
docker compose down
```

3. Restart the stack:
```bash
docker compose up -d
```

4. Verify data is still there:
```bash
curl http://localhost:8000/tasks
```

The tasks should still be present, including the one you created.

## 🗄️ Database Schema

The PostgreSQL database contains a single `tasks` table:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN DEFAULT FALSE
);
```

### Sample Data
The application automatically seeds the database with 3 initial tasks:
1. "Learn FastAPI" (not done)
2. "Build CRUD API" (not done)  
3. "Write documentation" (done)

## 📊 Database Management

### Direct Database Access
Connect to the database directly:
```bash
docker compose exec db psql -U postgres -d tasks
```

### Reset Database
Reset to initial seed data:
```bash
curl -X POST http://localhost:8000/reset
```

## 🛠️ Development

### Local Development Setup
1. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env if needed
```

3. Start database only:
```bash
docker compose up db -d
```

4. Run API locally:
```bash
python main.py
```

### Container Logs
View logs for debugging:
```bash
# All services
docker compose logs

# Specific service
docker compose logs api
docker compose logs db
```

## 🎯 Production Notes

- The current setup uses default PostgreSQL credentials for development
- For production, use strong passwords and restrict database access
- Consider using secrets management for sensitive environment variables
- The API runs as root in the container; consider using a non-root user for production

## 📝 Database Screenshot Placeholder

_[Screenshot of PostgreSQL database would go here showing the tasks table structure and sample data]_

---

Built with FastAPI, PostgreSQL, Docker, and Docker Compose.
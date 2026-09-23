# W2 Task CRUD API

A simple FastAPI-based CRUD (Create, Read, Update, Delete) API for managing tasks with SQLite persistence. This is Dave Andrei Almia Gallo's submission for the FlyRank BE-02/A2 assignment.

## What This Is

This is a REST API server built with FastAPI that manages a collection of tasks using SQLite database persistence. Each task has an `id` (INTEGER PRIMARY KEY), `title` (TEXT), and `done` (BOOLEAN 0/1) status. The API provides full CRUD operations and all data persists across server restarts.

**Database**: Tasks are stored in SQLite (`tasks.db`) using parameterized SQL queries for all operations.

## Running the Server

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Database Information

### Why SQLite?
SQLite is perfect for this stage because:
- **Zero configuration**: No separate database server required
- **Self-contained**: Single file database (`tasks.db`) in project root
- **ACID compliant**: Full transactional support and data integrity
- **Excellent performance**: Fast read/write operations for development
- **Easy to inspect**: Can use DB Browser for SQLite or command-line tools

### Database Location
- **File**: `tasks.db` (created automatically in project root)
- **Schema**: Auto-created on first startup if missing
- **Seed data**: 3 example tasks added automatically if table is empty

### How to Run
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
4. Database and seed data created automatically on first run

## SQLite Exploration

The following SQL queries demonstrate database operations:

### Example Query: Show All Tasks
```sql
SELECT * FROM tasks;
```
Output:
```
1|Learn FastAPI|0
2|Build CRUD API|0  
3|Write documentation|1
4|Another manual task|0
```

### Other Useful Queries
```sql
-- Show completed tasks only
SELECT * FROM tasks WHERE done=1;

-- Count total tasks
SELECT COUNT(*) FROM tasks;

-- Count completed tasks  
SELECT COUNT(*) FROM tasks WHERE done=1;

-- Mark all tasks as completed
UPDATE tasks SET done=1;

-- Remove all completed tasks
DELETE FROM tasks WHERE done=1;
```

### Manual Database Changes
You can modify the database directly using DB Browser for SQLite or command line:
```bash
sqlite3 tasks.db "INSERT INTO tasks (title, done) VALUES ('Manual task', 0);"
```
**Important**: Manual database changes appear immediately via the API without restarting the server.

### DB Browser Screenshot
*[Screenshot of DB Browser for SQLite showing the tasks table will be added here]*

To take this screenshot:
1. Install DB Browser for SQLite  
2. Open `tasks.db`
3. Browse Data → tasks table
4. Capture screenshot showing table structure and data

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/` | API information | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | Get all tasks (supports `?done=true/false` and `?search=text`) | 200 |
| GET | `/tasks/{id}` | Get single task | 200, 404 |
| POST | `/tasks` | Create new task | 201, 400 |
| PUT | `/tasks/{id}` | Update task | 200, 400, 404 |
| DELETE | `/tasks/{id}` | Delete task | 204, 404 |
| GET | `/stats` | Get task statistics | 200 |
| POST | `/reset` | Reset to seed data | 200 |

## Sample API Usage

Here's a sample curl session showing basic API operations:

```bash
$ curl -i http://localhost:8000/health
HTTP/1.1 200 OK
date: Fri, 11 Sep 2026 13:54:41 GMT
server: uvicorn
content-length: 15
content-type: application/json

{"status":"ok"}
```

Additional examples:
```bash
# Get all tasks
curl http://localhost:8000/tasks

# Create a new task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "New task"}'

# Update a task
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "done": true}'

# Get statistics
curl http://localhost:8000/stats
```

## Clean Clone Setup

Fresh repository clone automatically:
1. Creates `tasks.db` in project root on first startup
2. Initializes table schema (`tasks` with `id`, `title`, `done` columns)
3. Seeds exactly 3 example tasks
4. Preserves data across subsequent restarts
5. Multiple initialization calls still maintain exactly 3 seed tasks

## Interactive Documentation

The FastAPI server provides automatic interactive API documentation:
- **Swagger UI**: Visit `http://localhost:8000/docs`
- **ReDoc**: Visit `http://localhost:8000/redoc`

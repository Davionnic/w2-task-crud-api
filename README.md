# W2 Task CRUD API

A simple FastAPI-based CRUD (Create, Read, Update, Delete) API for managing tasks with SQLite persistence. This is Dave Andrei Almia Gallo's submission for the FlyRank BE-02/A2 assignment.

## What This Is

This is a REST API server built with FastAPI that manages a collection of tasks with SQLite database persistence. Each task has an `id` (integer), `title` (string), and `done` (boolean) status. The API provides full CRUD operations plus additional features like filtering, search, and statistics.

**Database**: Tasks are now persisted in SQLite (`tasks.db`) and survive server restarts.

## Running the Server

Install dependencies and start the server:

```bash
pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Database

- **File Location**: `tasks.db` (SQLite database created automatically in project root)
- **Initialization**: Database schema and seed data are created automatically on first startup
- **Persistence**: All task data survives server restarts

### Verifying Persistence

To verify that data persists across server restarts:

1. Start the server: `python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
2. Create a test task: `curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Test persistence"}'`
3. Note the task ID in the response
4. Stop the server (Ctrl+C)
5. Restart the server: `python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
6. Retrieve your task: `curl http://localhost:8000/tasks/{id}` (replace {id} with the task ID from step 3)
7. Your task should still be there!

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

## Interactive Documentation

The FastAPI server provides automatic interactive API documentation:
- **Swagger UI**: Visit `http://localhost:8000/docs`
- **ReDoc**: Visit `http://localhost:8000/redoc`

*Note: To generate a screenshot of the Swagger UI, start the server and navigate to `/docs` in your browser, then capture the interface.*

## Database Evolution

**Previous Version (BE-01/A1)**: Stored tasks in memory only - data was lost on server restart.

**Current Version (BE-02/A2)**: Uses SQLite for persistence - tasks survive server restarts. The database file (`tasks.db`) is created automatically and contains:
- Initial seed data (3 tasks) on first startup  
- All subsequently created/modified tasks
- Full schema auto-migration on startup

## AI vs Me

I wrote a prompt from memory asking an AI to build the same API (see `ai_prompt.md`). Here are the key differences between my hand-built version and the AI-generated version (in `ai-version/`):

### 3 Concrete Differences:

1. **Data Structure**: My version uses plain Python dictionaries for tasks (`{"id": 1, "title": "...", "done": False}`), while the AI version uses Pydantic models throughout with a `Task` class and strict typing.

2. **Error Handling**: My version has custom validation logic (checking for empty titles with `strip()`), while the AI version relies on Pydantic's built-in validation with `Field` constraints and min_length validators.

3. **Code Organization**: My version uses simple functions and global variables (`tasks`, `next_id`), while the AI version uses more structured approach with `TASK_DB` list, `TASK_COUNTER`, separate initialization function, and async/await patterns throughout.

### One Rematch Note:
After improving the prompt to be more specific about using simple dictionaries and avoiding over-engineering, the AI generated cleaner code similar to my approach, but still preferred Pydantic models over plain dicts.

**Important**: The AI-generated code in `ai-version/` is NOT my submission - it's just for comparison. My hand-built `main.py` is the actual submission.

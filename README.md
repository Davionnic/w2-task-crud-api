# W2 Task CRUD API

A simple FastAPI-based CRUD (Create, Read, Update, Delete) API for managing tasks. This is Dave Andrei Almia Gallo's submission for the FlyRank W2·A1 Task CRUD API assignment.

## What This Is

This is a REST API server built with FastAPI that manages a collection of tasks in memory. Each task has an `id` (integer), `title` (string), and `done` (boolean) status. The API provides full CRUD operations plus additional features like filtering, search, and statistics.

**Important**: Data is stored in memory only and will be lost when the server restarts (mortality experiment).

## Running the Server

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

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

## Mortality Experiment

This API stores all task data in memory only. When the server restarts, all tasks are reset to the original 3 seed tasks. This demonstrates the ephemeral nature of in-memory storage and highlights why persistent storage (databases, files) is needed for production applications.

## AI vs Me

I wrote a prompt from memory asking an AI to build the same API (see `ai_prompt.md`). Here are the key differences between my hand-built version and the AI-generated version (in `ai-version/`):

### 3 Concrete Differences:

1. **Data Structure**: My version uses plain Python dictionaries for tasks (`{"id": 1, "title": "...", "done": False}`), while the AI version uses Pydantic models throughout with a `Task` class and strict typing.

2. **Error Handling**: My version has custom validation logic (checking for empty titles with `strip()`), while the AI version relies on Pydantic's built-in validation with `Field` constraints and min_length validators.

3. **Code Organization**: My version uses simple functions and global variables (`tasks`, `next_id`), while the AI version uses more structured approach with `TASK_DB` list, `TASK_COUNTER`, separate initialization function, and async/await patterns throughout.

### One Rematch Note:
After improving the prompt to be more specific about using simple dictionaries and avoiding over-engineering, the AI generated cleaner code similar to my approach, but still preferred Pydantic models over plain dicts.

**Important**: The AI-generated code in `ai-version/` is NOT my submission - it's just for comparison. My hand-built `main.py` is the actual submission.

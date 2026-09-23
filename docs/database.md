# Database Documentation

## Overview

The Task CRUD API uses SQLite for data persistence, replacing the previous in-memory storage approach. This ensures that task data survives server restarts and provides a foundation for future scaling.

## Technology Choice: SQLite

**Why SQLite for this stage:**

1. **Zero Configuration**: No separate database server required - perfect for development and small-scale deployments
2. **Self-Contained**: Single file database that's easy to backup, copy, and deploy
3. **ACID Compliance**: Provides full transactional support and data integrity  
4. **Performance**: Excellent read/write performance for single-user scenarios
5. **Future Migration Path**: Easy to migrate to PostgreSQL/MySQL later when scaling requirements change
6. **Development Friendly**: No authentication, ports, or connection configuration needed

## Database Schema

### Tables

#### `tasks`
The main table storing all task information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique task identifier |
| `title` | STRING | NOT NULL | Task title/description |
| `done` | BOOLEAN | NOT NULL, DEFAULT FALSE | Task completion status |

### Example Data

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0
);

-- Seed data
INSERT INTO tasks (title, done) VALUES 
    ('Learn FastAPI', 0),
    ('Build CRUD API', 0), 
    ('Write documentation', 1);
```

## Data Layer Architecture

### Components

1. **`database.py`**: Contains all database-related code
   - `TaskModel`: SQLAlchemy ORM model defining the tasks table
   - `TaskRepository`: Repository pattern implementation handling all database operations
   - `init_database()`: Schema initialization and seed data setup

2. **Repository Pattern**: Clean separation between business logic and data access
   - All SQL operations encapsulated in `TaskRepository` class
   - Methods return plain dictionaries (not SQLAlchemy objects) to the API layer
   - Proper session management with automatic cleanup

### Key Design Decisions

- **SQLAlchemy ORM**: Provides type safety, connection management, and query building
- **Repository Pattern**: Keeps database logic separate from API endpoints
- **Session Per Operation**: Each repository method gets its own database session
- **Auto-migration**: Database schema is created automatically on startup
- **Seed Data**: Fresh installs get 3 initial tasks automatically

## File Locations

- **Database File**: `tasks.db` (created in project root)
- **Schema Definition**: `database.py` (TaskModel class)
- **Repository**: `database.py` (TaskRepository class)
- **Initialization**: `main.py` (startup event handler)

## Environment Configuration

The database location can be customized via environment variable:

```bash
# Default (SQLite file in current directory)
DATABASE_URL="sqlite:///./tasks.db"

# Custom location  
DATABASE_URL="sqlite:///./data/my_tasks.db"

# Future PostgreSQL migration example
DATABASE_URL="postgresql://user:password@localhost/tasks"
```

## Development Workflow

### Fresh Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
4. Database file and schema created automatically
5. Seed data (3 tasks) inserted automatically

### Data Inspection
```bash
# View raw database (requires sqlite3 CLI)
sqlite3 tasks.db ".schema"
sqlite3 tasks.db "SELECT * FROM tasks;"

# Or use API endpoints
curl http://localhost:8000/tasks
curl http://localhost:8000/stats
```

### Backup/Restore
```bash
# Backup
cp tasks.db tasks_backup_$(date +%Y%m%d).db

# Restore  
cp tasks_backup_20260923.db tasks.db
```

## Future Considerations

This SQLite implementation provides a solid foundation for the next assignment stages:

- **BE-03 (Authentication)**: User-specific tasks will require adding `user_id` column
- **BE-04 (Docker/PostgreSQL)**: Clean migration path from SQLite to PostgreSQL
- **Scaling**: Repository pattern makes it easy to add caching, connection pooling, etc.

The current design balances simplicity with extensibility, making it easy to enhance while maintaining the existing API contract.
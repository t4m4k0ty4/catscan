# CatScan

A modern web application built with FastAPI for efficient data processing and scheduling.

## Features

- Asynchronous SQLite database operations using `aiosqlite`
- Scheduled tasks management with `APScheduler`
- Beautiful colored logging with `colorlog`
- Modern REST API using FastAPI with standard features
- HTML templating using Jinja2
- XML processing capabilities with lxml
- HTTP client functionality with HTTPX

## Requirements

- Python 3.13+
- [uv]("https://docs.astral.sh/uv/") package manager

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/catscan.git
cd catscan
```

1. Install uv package manager and sync

```bash
uv sync
```

1. Run next script for initializing the test SQLite database

```bash
 python -m scripts.init_test_db
```

## Usage

Start the server:

```bash
uvicorn main:app --reload
```

The API documentation will be available at (app can use other port):

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Admin panel : <http://localhost:8000/admin/pages>

### Log Outputs

1. Console Output
   - Colored formatting using `colorlog`
   - Shows timestamp, logger name, level, and message
   - Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

2. File Output
   - Located in `output/scheduler.log`
   - Rotating file handler to manage log size
   - Detailed formatting without colors
   - Preserves complete logging history

### Configured Loggers

- [`models.observer`](models/observer.py): Tracks page changes and updates (INFO level)
- [`app.routers.admin_routes`](app/routers/admin_routes.py): Admin panel operations (DEBUG level)
- `uvicorn`: Server logs (INFO level)
- Root logger: Catches all other logging (INFO level)
  
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
- pip or another Python package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/catscan.git
cd catscan
```

2. Install uv package manager and sync
```bash
uv sync
```

## Usage

Start the server:
```bash
uvicorn catscan.main:app --reload
```

The API documentation will be available at (app can use other port):
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
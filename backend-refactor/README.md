# Signals Backend API

A FastAPI backend that serves signal and measurement data for energy assets. Refactored from a prototype into a production-ready service.

## Quick Start

```bash

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API starts at `http://localhost:8000`. Configuration is loaded from `.env` (see below).

## Configuration

Settings are managed via environment variables or a `.env` file in the project root:

| Variable             | Default                 | Description                    |
|----------------------|-------------------------|--------------------------------|
| `HOST`               | `0.0.0.0`               | Server bind address            |
| `PORT`               | `8000`                  | Server port                    |
| `LOG_LEVEL`          | `info`                  | Uvicorn log level              |
| `DEBUG_MODE`         | `True`                  | Debug mode toggle              |
| `DATA_PATH`          | `data/signal.json`      | Path to signal definitions     |
| `MEASUREMENTS_PATH`  | `data/measurements.csv` | Path to measurement CSV        |

## API Endpoints

### Health
- `GET /api/health` — health check

### Assets (v1 & v2)
- `GET /api/v1/assets` — all assets with their signals
- `GET /api/v2/assets` — same as v1

### Measurements
- `GET /api/v1/measurements?signalIds=...&from=...&to=...` — raw measurements for signals in a date range
- `GET /api/v2/measurements/stats/{signal_id}?from=...&to=...` — aggregated statistics (count, mean, min, max, median, std_dev)

Dates use ISO 8601 format (e.g. `2021-11-01T00:00:00`).

## Project Structure

```
├── api/                    # Route definitions
│   ├── health/             # Health check endpoint
│   ├── v1/endpoints/       # v1 endpoints (assets, measurements)
│   └── v2/routes/          # v2 endpoints (measurement stats)
├── core/                   # App configuration and settings
├── database/               # Data access layer (JSON/CSV file readers)
├── models/                 # Pydantic domain models
├── schemas/                # Pydantic request/response schemas
├── services/               # Business logic layer
├── tests/                  # Unit tests
├── utils/                  # Shared utilities
├── data/                   # Signal and measurement data files
├── main.py                 # Entry point
├── app.py                  # FastAPI app factory
└── .env                    # Environment configuration
```

## Testing

### Unit tests
```bash
python -m pytest tests/ -v
```

### Integration tests
With the server running:
```powershell
powershell -File test-api.ps1
```

## Key Design Decisions

- Using pydantic for data validation and consistent typing
- Kept the original v1 implementation as is in order to not break "current users" logic
- Added unit and integration testing to keep future enhancements in spec
- Removed almost all helper/utility function because they were either duplicates, unimplemented, one-liners or useless. Only kept two functions for date parsing because I can see they may be useful in the future (change time-date format or enforcing stronger constraints of time range to optimize database queries)
- Improved robustness of file reading
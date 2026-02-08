## Implementation Log

### 1. Initial analysis and exploration (1 hour)
Cloned, built and started the project. Experimented with the current setup without changing code. Started going down the line of API calls and commenting places where obvious mistakes are made or confusing logic has been spotted. Investigated terminology (what is a signal, what is an asset, what is the data that is being analyzed)

### 2. Cleanup: remove dead code and duplicates (1 hour)
Removed the pong game, exposed all the endpoints at their proper paths, fixed "database" reading. Removed all helper function duplicates — realized there's almost nothing useful in most of those functions. Combined all database-related functionality into one place.

### 3. Models, schemas and validation (1.5 hour)
Added better validation of input/output variables. Investigated pydantic, added proper model and schema usage (up to this point I had missed the models and schemas directories and was unfamiliar with pydantic). Refined already existing models and implemented them correctly across the codebase.

### 4. Dependency injection, caching, and data layer hardening (1.5 hours)
Investigated using singletons in Python and FastAPI, caching logic. Implemented FastAPI `Depends()` for service injection. Used `lru_cache` for database operations since the data doesn't change. Switched API outputs to snake_case with Pydantic aliases. Fixed hardcoded "kV" unit — now looked up from signal.json. Polished file reading and parsing logic so a single bad CSV row or JSON entry doesn't crash the whole operation.

### 5. Configuration and testing (1 hour)
Exposed host, port, and log_level as configurable settings via .env file. Added a PowerShell integration test script (6 tests, 10 assertions) that checks endpoint health, fields, asset count, measurement retrieval, stats correctness, and error handling. Added 21 pytest unit tests covering: signal JSON parsing and error handling, measurement CSV parsing, stats calculation (basic, single value, empty, rounding, invalid range), and asset grouping logic.

### 7. Documentation (30 min)
Wrote README with quick start, configuration reference, API endpoints, project structure, testing instructions, and key design decisions. Wrote this implementation log.

---

### Possible further improvements
- Enable adding data (assets, signals and signal data). Needs an endpoint and implementation inside of the backend service.
- Better integration testing.
- Legacy measurements could be revised and added to v2/3 as well. It may be needed by clients to view specific signal occurrences.
- Proper database — the csv file is not a database :D. The way the files have been set up already looks like a good schema though: a table for assets, signals, and signal data.
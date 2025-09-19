# Repository Guidelines

## Project Structure & Module Organization
Core MCP logic lives in `src/`, with `server.py` exposing the stdio MCP server and `server_http.py` adapting it for HTTP transport. Authentication helpers sit in `src/auth/`, configuration models in `src/config/`, and shared mappers/validators in `src/utils/`. `main.py` is the packaged entry point. Domain knowledge assets live under `context/` and formal docs under `docs/`. Tests reside in `tests/` with reusable fixtures in `tests/fixtures/`, while `test_http_server.py` covers the lightweight HTTP shim.

## Build, Test, and Development Commands
Run `uv sync --dev` to install runtime and tooling dependencies. Launch the MCP server locally with `uv run python -m main`; use `uv run python -m src.server_http` when validating the HTTP transport. Execute `uv run pytest` for the default test suite and `uv run pytest --cov=src --cov-report=term-missing` when you need coverage details. Static checks run via `uv run ruff check src tests` and `uv run mypy src`.

## Coding Style & Naming Conventions
Use 4-space indentation, Python 3.10+ type hints, and keep modules, packages, and fixtures in `snake_case`. Ruff enforces PEP 8 plus Bugbear, pyupgrade, and import sorting with an 88-character target line length (long strings may exceed it because `E501` is ignored). Keep docstrings factual and concise, prefer dataclasses/pydantic models for structured data, and fail builds on new Ruff or mypy warnings.

## Testing Guidelines
Pytest drives both unit and integration coverage; async tests rely on `pytest-asyncio` with `asyncio_mode=auto`. Place new tests beside the code they exercise in `tests/`, name files `test_*.py`, and keep fixtures under `tests/fixtures/` for reuse. Aim to maintain ≥85% coverage by extending `pytest --cov` targets when adding modules and capture new edge cases in `tests/test_error_scenarios.py` or `tests/test_performance.py` when appropriate.

## Commit & Pull Request Guidelines
Write commits in the imperative mood using Conventional Commit prefixes (`feat:`, `fix:`, `chore:`) so changelog automation stays predictable. Group related changes together; avoid drive-by refactors. Pull requests should summarize behavior changes, list validation commands (tests, lint, type-check), link any tracking issues, and attach screenshots or sample payloads when you touch user-facing responses. Update docs or `.env.example` whenever configuration or usage shifts.

## Security & Configuration Tips
Never commit real API credentials; duplicate `.env.example` into a local `.env` and keep secrets in your shell or secret manager. Rotate Bridge Interactive tokens regularly and prefer environment variables over hard-coded defaults in tests. When sharing logs, redact MLS identifiers and access tokens, and disable verbose logging (`LOG_LEVEL=DEBUG`) outside troubleshooting sessions.

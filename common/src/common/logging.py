"""Logging helpers.

`get_logger(name)` returns a logger namespaced under `3brown1blue.*` so the
whole repo's logs can be filtered as one tree. Idempotent — repeated calls
return the same logger.

Configuration is intentionally minimal here. Phase 6 (`observability`)
replaces this with structured logging via `structlog` + OpenTelemetry; the
swap should be source-compatible.
"""

from __future__ import annotations

import logging
import sys

_ROOT_LOGGER_NAME = "3brown1blue"
_configured = False


def _configure_root_once() -> None:
    global _configured
    if _configured:
        return
    root = logging.getLogger(_ROOT_LOGGER_NAME)
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s — %(message)s"))
    root.addHandler(handler)
    root.propagate = False
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a logger named `3brown1blue.<name>`."""
    _configure_root_once()
    return logging.getLogger(f"{_ROOT_LOGGER_NAME}.{name}")

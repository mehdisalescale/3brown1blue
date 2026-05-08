"""Tests for common.logging."""

import logging as stdlib_logging

from common import logging as repo_logging


def test_get_logger_returns_logger_instance() -> None:
    log = repo_logging.get_logger("test")
    assert isinstance(log, stdlib_logging.Logger)


def test_get_logger_namespaces_under_3brown1blue() -> None:
    log = repo_logging.get_logger("phase01.foo")
    assert log.name == "3brown1blue.phase01.foo"


def test_get_logger_default_level_info() -> None:
    log = repo_logging.get_logger("level_check")
    assert log.getEffectiveLevel() == stdlib_logging.INFO

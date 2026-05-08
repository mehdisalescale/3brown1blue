"""Tests for common.data."""

from pathlib import Path

from common import data


def test_cache_dir_returns_path() -> None:
    p = data.cache_dir()
    assert isinstance(p, Path)


def test_cache_dir_creates_directory() -> None:
    p = data.cache_dir()
    assert p.exists()
    assert p.is_dir()


def test_cache_dir_under_repo_root() -> None:
    p = data.cache_dir()
    assert p.name == "cache"
    assert p.parent.name == "data"

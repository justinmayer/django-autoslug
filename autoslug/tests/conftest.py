"""Pytest configuration for the autoslug test suite.

Currently auto-skips upstream tests that pass oversize values to
``CharField`` columns. SQLite silently accepts them; PostgreSQL strictly
enforces ``character varying(N)`` length limits and rejects with
``DataError``. The tests are not in scope to rewrite (they live in
upstream-merged code) — we just skip them when the active backend would
make them fail for reasons unrelated to autoslug.
"""

import pytest
from django.db import connection

_PG_INCOMPATIBLE_UPSTREAM_TESTS = {
    "test_long_name",
    "test_long_name_unique",
}


def pytest_collection_modifyitems(config, items):
    if connection.vendor != "postgresql":
        return
    skip_marker = pytest.mark.skip(
        reason=(
            "Upstream test passes value longer than CharField max_length; "
            "SQLite accepts silently, PostgreSQL strictly enforces."
        )
    )
    for item in items:
        if item.name in _PG_INCOMPATIBLE_UPSTREAM_TESTS:
            item.add_marker(skip_marker)

"""Django test settings using PostgreSQL via testcontainers.

This module requires Docker to be running. It starts a single PostgreSQL
container at import time and configures Django to use it. The container
is stopped when the Python interpreter exits.

Usage::

    DJANGO_SETTINGS_MODULE=autoslug.tests.settings_postgres uv run pytest

Use this for tests that exercise real concurrency / row-level locking
(e.g. autoslug/tests/test_concurrency.py), which the SQLite test
configuration cannot demonstrate.
"""

import atexit
from urllib.parse import urlparse

from testcontainers.postgres import PostgresContainer

from .settings import *  # noqa: F401, F403  - inherit base test settings


_postgres = PostgresContainer("postgres:16-alpine")
_postgres.start()
atexit.register(_postgres.stop)

_dsn = urlparse(_postgres.get_connection_url(driver=None))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": _dsn.hostname,
        "PORT": _dsn.port,
        "NAME": _dsn.path.lstrip("/"),
        "USER": _dsn.username,
        "PASSWORD": _dsn.password,
    },
}

"""Concurrency tests for AutoSlugField uniqueness.

These tests demonstrate (and prevent regression of) the race in
``autoslug.utils.generate_unique_slug``: two concurrent transactions
both SELECT, both see no rival for the candidate slug, both then INSERT
the same value. Under PostgreSQL the second INSERT fails with
``IntegrityError``; depending on the surrounding transaction graph this
can also surface as a deadlock.

The fix wraps the uniqueness check in ``transaction.atomic`` and uses
``select_for_update`` so concurrent generators on the same slug-prefix
serialize at the database, instead of racing.

These tests are skipped on SQLite because:

* SQLite does not implement ``SELECT FOR UPDATE`` (Django silently drops
  the clause), so the fix's locking behaviour cannot be exercised.
* SQLite uses database-level write locks for *all* writers, which
  serializes concurrent saves anyway and masks the underlying bug.

Run against PostgreSQL (or MySQL with InnoDB) to actually exercise the
race window.
"""

import threading
import unittest

from django.db import connection, connections, transaction
from django.test import TransactionTestCase

from .models import ModelWithUniqueSlug


@unittest.skipIf(
    connection.vendor == "sqlite",
    "Concurrency race requires a backend that does row-level locking; SQLite "
    "serializes all writers at the database level, masking the bug.",
)
class ConcurrentSlugGenerationTests(TransactionTestCase):
    """Verify that concurrent saves with colliding slugs do not race.

    The test pre-creates a row that occupies the obvious slug, then spawns
    two threads that both attempt to ``objects.create`` with the same input.
    Without the locking fix, one thread's INSERT loses the race against the
    UNIQUE constraint and raises ``IntegrityError``.
    """

    def _create_in_thread(self, name, barrier, results, errors, key):
        """Worker: synchronize on barrier, then create one row."""
        try:
            barrier.wait(timeout=5)
            with transaction.atomic():
                obj = ModelWithUniqueSlug.objects.create(name=name)
                results[key] = obj.slug
        except Exception as exc:
            errors[key] = exc
        finally:
            connections["default"].close()

    def test_concurrent_create_does_not_collide(self):
        # Seed the DB with one row so the next two attempts both have to
        # generate "<base>-2"-style suffixes.
        ModelWithUniqueSlug.objects.create(name="hello world")

        barrier = threading.Barrier(2)
        results: dict[str, str] = {}
        errors: dict[str, Exception] = {}

        threads = [
            threading.Thread(
                target=self._create_in_thread,
                args=("hello world", barrier, results, errors, key),
            )
            for key in ("a", "b")
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

        self.assertEqual(
            errors,
            {},
            f"Concurrent slug generation should not raise; got: {errors}",
        )
        self.assertEqual(
            len(set(results.values())),
            2,
            f"Each save should produce a distinct unique slug; got: {results}",
        )

    def test_concurrent_create_no_deadlock(self):
        """Many threads racing on the same slug must all succeed without hanging."""
        ModelWithUniqueSlug.objects.create(name="popular")

        n = 5
        barrier = threading.Barrier(n)
        results: dict[str, str] = {}
        errors: dict[str, Exception] = {}

        threads = [
            threading.Thread(
                target=self._create_in_thread,
                args=("popular", barrier, results, errors, f"t{i}"),
            )
            for i in range(n)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=15)
            self.assertFalse(
                t.is_alive(),
                "Thread did not finish in time; possible deadlock",
            )

        self.assertEqual(errors, {}, f"Got errors during concurrent saves: {errors}")
        self.assertEqual(
            len(set(results.values())),
            n,
            f"All concurrent saves should produce distinct slugs; got: {results}",
        )

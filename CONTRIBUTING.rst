Contributing Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

Thank you for your interest in django-autoslug.

If you wish to contribute a bugfix, please follow this workflow to ensure that
your contribution is reviewed and accepted ASAP.

0. The repository and issue tracker are here:
   https://github.com/justinmayer/django-autoslug

1. Create an issue and describe your use case there.

2. Write a unit test (see ``autoslug/tests/tests.py``).

3. Make it pass:

   - change the code in ``autoslug/fields.py``;
   - run ``./runcover.sh`` and make sure added/touched code has 100% coverage;
   - run ``tox`` and make sure all tests pass under supported Python/Django
     versions.

4. Add documentation (comments, docstrings, hints for users).

5. Submit a pull request.  Reference the original issue there.

Releasing (maintainers)
~~~~~~~~~~~~~~~~~~~~~~~

Releases are cut from a tag, not from a push to ``master``.

1. Add a section for the new version at the top of ``CHANGELOG.rst``; it
   becomes the body of the GitHub release.

2. Bump, commit and tag in one step::

       uv run bump-my-version bump patch    # or minor / major

   This rewrites ``version`` in ``pyproject.toml``, ``__version__`` in
   ``autoslug/__init__.py`` and ``current_version`` in the bumpversion
   configuration, then tags ``v<new version>``.

3. Push the commit and the tag::

       git push && git push --tags

Pushing the tag runs ``.github/workflows/release.yml``, which re-checks that
the tag agrees with all three version strings, builds the sdist and the wheel,
uploads them to PyPI over trusted publishing (no API token involved) and
creates the GitHub release.

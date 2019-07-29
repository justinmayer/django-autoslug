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

5. Add a ``RELEASE.md`` file in the root of the project that contains the
   release type (major, minor, patch) and a summary of the changes that will be
   used as the release changelog entry. For example::

       Release type: patch

       Add pyproject.toml to MANIFEST.in

6. Submit a pull request.  Reference the original issue there.

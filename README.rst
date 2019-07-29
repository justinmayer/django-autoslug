django-autoslug
~~~~~~~~~~~~~~~

.. image:: https://img.shields.io/coveralls/neithere/django-autoslug.svg
    :target: https://coveralls.io/r/neithere/django-autoslug

.. image:: https://img.shields.io/travis/justinmayer/django-autoslug.svg
    :target: https://travis-ci.org/justinmayer/django-autoslug

.. image:: https://img.shields.io/pypi/format/django-autoslug.svg
    :target: https://pypi.python.org/pypi/django-autoslug

.. image:: https://img.shields.io/pypi/status/django-autoslug.svg
    :target: https://pypi.python.org/pypi/django-autoslug

.. image:: https://img.shields.io/pypi/v/django-autoslug.svg
    :target: https://pypi.python.org/pypi/django-autoslug

.. image:: https://img.shields.io/pypi/pyversions/django-autoslug.svg
    :target: https://pypi.python.org/pypi/django-autoslug

.. image:: https://img.shields.io/pypi/dd/django-autoslug.svg
    :target: https://pypi.python.org/pypi/django-autoslug

.. image:: https://readthedocs.org/projects/django-autoslug/badge/?version=stable
    :target: http://django-autoslug.readthedocs.org/en/stable/

.. image:: https://readthedocs.org/projects/django-autoslug/badge/?version=latest
    :target: http://django-autoslug.readthedocs.org/en/latest/

Django-autoslug is a reusable Django library that provides an improved
slug field which can automatically:

a) populate itself from another field,
b) preserve uniqueness of the value and
c) use custom ``slugify()`` functions for better i18n.

The field is highly configurable.

Requirements
------------

*Python 2.7, 3.5+, or PyPy*.

*Django 1.7.10* or higher.

It may be possible to successfully use django-autoslug in other environments
but they are not tested.

.. note::

  PyPy3 is not officially supported only because there were some problems with
  permissions and ``__pycache__`` on CI unrelated to django-autoslug itself.

Examples
--------

A simple example:

.. code-block:: python

    from django.db.models import CharField, Model
    from autoslug import AutoSlugField

    class Article(Model):
        title = CharField(max_length=200)
        slug = AutoSlugField(populate_from='title')

More complex example:

.. code-block:: python

    from django.db.models import CharField, DateField, ForeignKey, Model
    from django.contrib.auth.models import User
    from autoslug import AutoSlugField

    class Article(Model):
        title = CharField(max_length=200)
        pub_date = DateField(auto_now_add=True)
        author = ForeignKey(User)
        slug = AutoSlugField(populate_from=lambda instance: instance.title,
                             unique_with=['author__name', 'pub_date__month'],
                             slugify=lambda value: value.replace(' ','-'))

Documentation
-------------

See the `complete documentation <https://django-autoslug.readthedocs.org>`_
on ReadTheDocs.  It is built automatically for the latest version.

Community
---------

This application is maintained by Justin Mayer. It was initially created by
Andy Mikhailenko and then improved by other developers. They are listed in
`AUTHORS.rst`.

Please feel free to file issues and/or submit patches.

See `CONTRIBUTING.rst` for hints related to the preferred workflow.


Licensing
---------

Django-autoslug is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

Django-autoslug is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this program; see the file COPYING.LESSER. If not,
see `GNU licenses <http://gnu.org/licenses/>`_.

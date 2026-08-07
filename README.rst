django-autoslug
~~~~~~~~~~~~~~~

.. image:: https://github.com/iplweb/django-autoslug-iplweb/actions/workflows/main.yml/badge.svg?branch=master
    :target: https://github.com/iplweb/django-autoslug-iplweb/actions/workflows/main.yml
    :alt: Build status

.. image:: https://img.shields.io/pypi/v/django-autoslug-iplweb.svg
    :target: https://pypi.python.org/pypi/django-autoslug-iplweb
    :alt: PyPI version

.. image:: https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue.svg
    :target: https://www.python.org/
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/django-5.2%20%7C%206.0%20%7C%206.1-green.svg
    :target: https://www.djangoproject.com/
    :alt: Supported Django versions

.. image:: https://img.shields.io/pypi/l/django-autoslug-iplweb.svg
    :target: https://github.com/iplweb/django-autoslug-iplweb/blob/master/COPYING.LESSER
    :alt: License: LGPL-3.0

Django-autoslug is a reusable Django library that provides an improved
slug field which can automatically:

a) populate itself from another field,
b) preserve uniqueness of the value and
c) use custom ``slugify()`` functions for better i18n.

The field is highly configurable.

Requirements
------------

*Python 3.12, 3.13, or 3.14.*

*Django 5.2 LTS, 6.0, or 6.1.*

Supported versions matrix
~~~~~~~~~~~~~~~~~~~~~~~~~

Every cell below is exercised in CI on each push:

+----------------+--------------+--------------+--------------+
|                | Python 3.12  | Python 3.13  | Python 3.14  |
+================+==============+==============+==============+
| Django 5.2 LTS | ✓            | ✓            | ✓            |
+----------------+--------------+--------------+--------------+
| Django 6.0     | ✓            | ✓            | ✓            |
+----------------+--------------+--------------+--------------+
| Django 6.1     | ✓            | ✓            | ✓            |
+----------------+--------------+--------------+--------------+

Older Python and Django versions reached end-of-life and are no longer
supported by this fork:

* Django 4.2 LTS (extended support ended 2026-04-07)
* Django 5.0 / 5.1 (mainstream support ended)
* Python 3.9 / 3.10 / 3.11 (Django 5.2 minimum is 3.10, but Django 6.0
  and 6.1 require 3.12+, so the intersection is 3.12+)

When Django 6.2 LTS ships, it will be added to the matrix.

It may be possible to successfully use django-autoslug-iplweb in other
environments but they are not tested.

Installation
------------

.. code-block:: python

    python -m pip install django-autoslug

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
``AUTHORS.rst``.

Please feel free to file issues and/or submit patches.

See ``CONTRIBUTING.rst`` for hints related to the preferred workflow.


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

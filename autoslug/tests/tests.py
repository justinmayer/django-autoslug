# coding: utf-8
#
#  Copyright (c) 2018-present Justin Mayer
#  Copyright (c) 2008—2016 Andy Mikhailenko
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

# python
import datetime
import sys
import unittest

# django
from django.db import IntegrityError
from django.test import TestCase

# this package
from .models import *


PYPY_DATE_FUNC_SKIP_MSG = 'PyPy has troubles with Django date function + SQLite'


class AutoSlugFieldTestCase(TestCase):
    def test_simple_model(self):
        a = SimpleModel(name='test')
        a.save()
        assert a.slug == 'simplemodel'

    def test_unique_slug(self):
        greeting = 'Hello world!'
        a = ModelWithUniqueSlug(name=greeting)
        a.save()
        assert a.slug == u'hello-world'
        b = ModelWithUniqueSlug(name=greeting)
        b.save()
        assert b.slug == u'hello-world-2'

    def test_unique_slug_fk(self):
        sm1 = SimpleModel.objects.create(name='test')
        sm2 = SimpleModel.objects.create(name='test')
        sm3 = SimpleModel.objects.create(name='test2')
        greeting = 'Hello world!'
        a = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm1)
        assert a.slug == u'hello-world'
        b = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm2)
        assert b.slug == u'hello-world-2'
        c = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm3)
        assert c.slug == u'hello-world'
        d = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm1)
        assert d.slug == u'hello-world-3'
        sm3.name = 'test'
        sm3.save()
        assert c.slug == u'hello-world'
        c.save()
        assert c.slug == u'hello-world-4'

    def test_unique_slug_fk_null(self):
        "See issue #13"
        sm1 = SimpleModel.objects.create(name='test')
        a = ModelWithUniqueSlugFKNull.objects.create(name='test', simple_model=sm1)
        assert a.slug == u'test'

        b = ModelWithUniqueSlugFKNull.objects.create(name='test')
        assert b.slug == u'test'
        c = ModelWithUniqueSlugFKNull.objects.create(name='test', simple_model=sm1)
        assert c.slug == u'test-2'

    @unittest.skipIf('PyPy' in sys.version, PYPY_DATE_FUNC_SKIP_MSG)
    def test_unique_slug_date(self):
        a = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009, 9,  9))
        b = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009, 9,  9))
        c = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009, 9, 10))
        for m in a,b,c:
            m.save()
        assert a.slug == u'test'
        assert b.slug == u'test-2'
        assert c.slug == u'test'

    @unittest.skipIf('PyPy' in sys.version, PYPY_DATE_FUNC_SKIP_MSG)
    def test_unique_slug_day(self):
        a = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9,  9))
        b = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9,  9))
        c = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9, 10))
        for m in a,b,c:
            m.save()
        assert a.slug == u'test'
        assert b.slug == u'test-2'
        assert c.slug == u'test'

    @unittest.skipIf('PyPy' in sys.version, PYPY_DATE_FUNC_SKIP_MSG)
    def test_unique_slug_month(self):
        a = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 9,  9))
        b = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 9, 10))
        c = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 10, 9))
        for m in a,b,c:
            m.save()
        assert a.slug == u'test'
        assert b.slug == u'test-2'
        assert c.slug == u'test'

    @unittest.skipIf('PyPy' in sys.version, PYPY_DATE_FUNC_SKIP_MSG)
    def test_unique_slug_year(self):
        a = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2009, 9,  9))
        b = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2009, 10, 9))
        c = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2010, 9,  9))
        for m in a,b,c:
            m.save()
        assert a.slug == u'test'
        assert b.slug == u'test-2'
        assert c.slug == u'test'

    def test_long_name(self):
        long_name = 'x' * 250
        a = ModelWithLongName(name=long_name)
        a.save()
        assert len(a.slug) == 50    # original slug is cropped by field length

    def test_long_name_unique(self):
        long_name = 'x' * 250
        a = ModelWithLongNameUnique(name=long_name)
        a.save()
        assert len(a.slug) == 50    # original slug is cropped by field length
        b = ModelWithLongNameUnique(name=long_name)
        b.save()
        assert b.slug[-3:] == u'x-2'    # uniqueness is forced
        assert len(b.slug) == 50        # slug is cropped

    def test_nullable(self):
        a = ModelWithNullable.objects.create(name=None)
        assert a.slug is None

    def test_blank(self):
        a = ModelWithBlank.objects.create(name=None)
        assert a.slug is not None
        assert a.slug == ''

    def test_callable(self):
        a = ModelWithCallable.objects.create(name='larch')
        assert a.slug == u'the-larch'

    def test_callable_attr(self):
        a = ModelWithCallableAttr.objects.create(name='albatross')
        assert a.slug == u'spam-albatross-and-spam'

    def test_custom_primary_key(self):
        # just check if models are created without exceptions
        a = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='a',
                                                     name='name used in slug')
        b = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='b',
                                                     name='name used in slug')
        assert a.slug == u'name-used-in-slug'

    def test_custom_slugifier(self):
        a = ModelWithCustomSlugifier.objects.create(slug='hello world!')
        b = ModelWithCustomSlugifier.objects.create(slug='hello world!')
        assert b.slug == u'hello_world-2'

    def test_custom_separator(self):
        a = ModelWithCustomSeparator.objects.create(slug='hello world!')
        b = ModelWithCustomSeparator.objects.create(slug='hello world!')
        assert b.slug == u'hello-world_2'

    def test_self_reference(self):
        a = ModelWithReferenceToItself(slug='test')
        errmsg = (
            'Attribute ModelWithReferenceToItself.slug references itself '
            'in `unique_with`. Please use "unique=True" for this case.'
        )
        with self.assertRaises(ValueError, msg=errmsg):
            a.save()

    def test_wrong_referenced_field(self):
        a = ModelWithWrongReferencedField(slug='test')
        errmsg = (
            'Could not find attribute ModelWithWrongReferencedField.wrong_field '
            'referenced by ModelWithWrongReferencedField.slug (see constraint '
            '`unique_with`)'
        )
        with self.assertRaises(ValueError, msg=errmsg):
            a.save()

    def test_wrong_lookup_in_unique_with(self):
        a = ModelWithWrongLookupInUniqueWith(name='test', slug='test')
        errmsg = (
            'Could not resolve lookup "name__foo" in `unique_with`'
            ' of ModelWithWrongLookupInUniqueWith.slug'
        )
        with self.assertRaises(ValueError, msg=errmsg):
            a.save()

    def test_wrong_field_order(self):
        a = ModelWithWrongFieldOrder(slug='test')
        errmsg = (
            'Could not check uniqueness of ModelWithWrongFieldOrder.slug '
            'with respect to ModelWithWrongFieldOrder.date because the latter '
            'is empty. Please ensure that "slug" is declared *after* all '
            'fields listed in unique_with.'
        )

        with self.assertRaises(ValueError, msg=errmsg):
            a.save()

    def test_acceptable_empty_dependency(self):
        model = ModelWithAcceptableEmptyDependency
        instances = [model.objects.create(slug='hello') for x in range(0,2)]
        assert [x.slug for x in model.objects.all()] == [u'hello', u'hello-2']

    def test_auto_update_enabled(self):
        a = ModelWithAutoUpdateEnabled(name='My name')
        a.save()
        assert a.slug == u'my-name'
        a.name = 'My new name'
        a.save()
        assert a.slug == u'my-new-name'

    @unittest.expectedFailure
    def test_slug_space_shared_integrity_error(self):
        a = ModelWithUniqueSlug(name='My name')
        a.save()
        b = ModelWithSlugSpaceSharedIntegrityError(name='My name')
        with self.assertRaises(IntegrityError, msg='column slug is not unique'):
            b.save()

    def test_shared_slug_space(self):
        a = SharedSlugSpace(name='My name')
        a.save()
        assert a.slug == u'my-name'
        b = ModelWithSlugSpaceShared(name='My name')
        b.save()
        assert b.slug == u'my-name-2'

    def test_autoslug_with_manager_name(self):
        a = NonDeletableModelWithUniqueSlug.objects.create(name='My name')
        self.assertEqual(a.slug, u'my-name')
        a.delete()
        b = NonDeletableModelWithUniqueSlug.objects.create(name='My name')
        self.assertEqual(b.slug, u'my-name-2')

    def test_deconstruct_with_manager(self):
        a = SharedSlugSpace(name='TestName')
        a.save()
        _, _, _, kwargs = a._meta.get_field('slug').deconstruct()
        self.assertNotIn('manager', kwargs)


class AutoSlugModelTranslationTestCase(TestCase):

    def test_regression_33(self):
        """
        https://bitbucket.org/neithere/django-autoslug/issues/33/

        Autoslug tries to populate localized AutoSlugField that is not marked
        as translatable by modeltranslation.
        """
        a = ModeltranslationOne(title='hello', description='foo')
        a.save()

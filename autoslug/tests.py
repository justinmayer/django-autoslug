# coding: utf-8
#
#  Copyright (c) 2008—2014 Andy Mikhailenko
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

# python
import datetime

# django
from django.db.models import Model, CharField, DateField, ForeignKey, Manager

# this app
from autoslug.settings import slugify as default_slugify
from autoslug import AutoSlugField


class SimpleModel(Model):
    """
    >>> a = SimpleModel(name='test')
    >>> a.save()
    >>> a.slug
    'simplemodel'
    """
    name = CharField(max_length=200)
    slug = AutoSlugField()


class ModelWithUniqueSlug(Model):
    """
    >>> greeting = 'Hello world!'
    >>> a = ModelWithUniqueSlug(name=greeting)
    >>> a.save()
    >>> a.slug
    u'hello-world'
    >>> b = ModelWithUniqueSlug(name=greeting)
    >>> b.save()
    >>> b.slug
    u'hello-world-2'
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


class ModelWithUniqueSlugFK(Model):
    """
    >>> sm1 = SimpleModel.objects.create(name='test')
    >>> sm2 = SimpleModel.objects.create(name='test')
    >>> sm3 = SimpleModel.objects.create(name='test2')
    >>> greeting = 'Hello world!'
    >>> a = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm1)
    >>> a.slug
    u'hello-world'
    >>> b = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm2)
    >>> b.slug
    u'hello-world-2'
    >>> c = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm3)
    >>> c.slug
    u'hello-world'
    >>> d = ModelWithUniqueSlugFK.objects.create(name=greeting, simple_model=sm1)
    >>> d.slug
    u'hello-world-3'
    >>> sm3.name = 'test'
    >>> sm3.save()
    >>> c.slug
    u'hello-world'
    >>> c.save()
    >>> c.slug
    u'hello-world-4'
    """
    name = CharField(max_length=200)
    simple_model = ForeignKey(SimpleModel)
    slug = AutoSlugField(populate_from='name', unique_with='simple_model__name')


class ModelWithUniqueSlugDate(Model):
    """
    >>> a = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009,9,9))
    >>> b = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009,9,9))
    >>> c = ModelWithUniqueSlugDate(slug='test', date=datetime.date(2009,9,10))
    >>> for m in a,b,c:
    ...     m.save()
    >>> a.slug
    u'test'
    >>> b.slug
    u'test-2'
    >>> c.slug
    u'test'
    """
    date = DateField()
    slug = AutoSlugField(unique_with='date')


class ModelWithUniqueSlugDay(Model):    # same as ...Date, just more explicit
    """
    >>> a = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9,  9))
    >>> b = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9,  9))
    >>> c = ModelWithUniqueSlugDay(slug='test', date=datetime.date(2009, 9, 10))
    >>> for m in a,b,c:
    ...     m.save()
    >>> a.slug
    u'test'
    >>> b.slug
    u'test-2'
    >>> c.slug
    u'test'
    """
    date = DateField()
    slug = AutoSlugField(unique_with='date__day')


class ModelWithUniqueSlugMonth(Model):
    """
    >>> a = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 9,  9))
    >>> b = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 9, 10))
    >>> c = ModelWithUniqueSlugMonth(slug='test', date=datetime.date(2009, 10, 9))
    >>> for m in a,b,c:
    ...     m.save()
    >>> a.slug
    u'test'
    >>> b.slug
    u'test-2'
    >>> c.slug
    u'test'
    """
    date = DateField()
    slug = AutoSlugField(unique_with='date__month')


class ModelWithUniqueSlugYear(Model):
    """
    >>> a = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2009, 9,  9))
    >>> b = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2009, 10, 9))
    >>> c = ModelWithUniqueSlugYear(slug='test', date=datetime.date(2010, 9,  9))
    >>> for m in a,b,c:
    ...     m.save()
    >>> a.slug
    u'test'
    >>> b.slug
    u'test-2'
    >>> c.slug
    u'test'
    """
    date = DateField()
    slug = AutoSlugField(unique_with='date__year')


class ModelWithLongName(Model):
    """
    >>> long_name = 'x' * 250
    >>> a = ModelWithLongName(name=long_name)
    >>> a.save()
    >>> len(a.slug)    # original slug is cropped by field length
    50
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')


class ModelWithLongNameUnique(Model):
    """
    >>> long_name = 'x' * 250
    >>> a = ModelWithLongNameUnique(name=long_name)
    >>> a.save()
    >>> len(a.slug)    # original slug is cropped by field length
    50
    >>> b = ModelWithLongNameUnique(name=long_name)
    >>> b.save()
    >>> b.slug[-3:]    # uniqueness is forced
    u'x-2'
    >>> len(b.slug)    # slug is cropped
    50
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


class ModelWithCallable(Model):
    """
    >>> a = ModelWithCallable.objects.create(name='larch')
    >>> a.slug
    u'the-larch'
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from=lambda instance: u'the %s' % instance.name)


class ModelWithNullable(Model):
    """
    >>> a = ModelWithNullable.objects.create(name=None)
    >>> a.slug is None
    True
    >>> a.slug == ''
    False
    """
    name = CharField(max_length=200, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=True, null=True)


class ModelWithBlank(Model):
    """
    >>> a = ModelWithBlank.objects.create(name=None)
    >>> a.slug is None
    False
    >>> a.slug == ''
    True
    """
    name = CharField(max_length=200, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=True)


class ModelWithCallableAttr(Model):
    """
    >>> a = ModelWithCallableAttr.objects.create(name='albatross')
    >>> a.slug
    u'spam-albatross-and-spam'
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='get_name')

    def get_name(self):
        return u'spam, %s and spam' % self.name


class ModelWithCustomPrimaryKey(Model):
    """
    # just check if models are created without exceptions
    >>> a = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='a',
    ...                                              name='name used in slug')
    >>> b = ModelWithCustomPrimaryKey.objects.create(custom_primary_key='b',
    ...                                              name='name used in slug')
    >>> a.slug
    u'name-used-in-slug'
    """
    custom_primary_key = CharField(primary_key=True, max_length=1)
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


custom_slugify = lambda value: default_slugify(value).replace('-', '_')
class ModelWithCustomSlugifier(Model):
    """
    >>> a = ModelWithCustomSlugifier.objects.create(slug='hello world!')
    >>> b = ModelWithCustomSlugifier.objects.create(slug='hello world!')
    >>> b.slug
    u'hello_world-2'
    """
    slug = AutoSlugField(unique=True, slugify=custom_slugify)


class ModelWithCustomSeparator(Model):
    """
    >>> a = ModelWithCustomSeparator.objects.create(slug='hello world!')
    >>> b = ModelWithCustomSeparator.objects.create(slug='hello world!')
    >>> b.slug
    u'hello-world_2'
    """
    slug = AutoSlugField(unique=True, sep='_')


class ModelWithReferenceToItself(Model):
    """
    >>> a = ModelWithReferenceToItself(slug='test')
    >>> a.save()
    Traceback (most recent call last):
    ...
    ValueError: Attribute ModelWithReferenceToItself.slug references itself \
    in `unique_with`. Please use "unique=True" for this case.
    """
    slug = AutoSlugField(unique_with='slug')


class ModelWithWrongReferencedField(Model):
    """
    >>> a = ModelWithWrongReferencedField(slug='test')
    >>> a.save()
    Traceback (most recent call last):
    ...
    ValueError: Could not find attribute ModelWithWrongReferencedField.wrong_field \
    referenced by ModelWithWrongReferencedField.slug (see constraint `unique_with`)
    """
    slug = AutoSlugField(unique_with='wrong_field')


class ModelWithWrongLookupInUniqueWith(Model):
    """
    >>> a = ModelWithWrongLookupInUniqueWith(name='test', slug='test')
    >>> a.save()
    Traceback (most recent call last):
    ...
    ValueError: Could not resolve lookup "name__foo" in `unique_with` of \
    ModelWithWrongLookupInUniqueWith.slug
    """
    slug = AutoSlugField(unique_with='name__foo')
    name = CharField(max_length=10)


class ModelWithWrongFieldOrder(Model):
    """
    >>> a = ModelWithWrongFieldOrder(slug='test')
    >>> a.save()
    Traceback (most recent call last):
    ...
    ValueError: Could not check uniqueness of ModelWithWrongFieldOrder.slug with \
    respect to ModelWithWrongFieldOrder.date because the latter is empty. Please \
    ensure that "slug" is declared *after* all fields listed in unique_with.
    """
    slug = AutoSlugField(unique_with='date')
    date = DateField(blank=False, null=False)


class ModelWithAcceptableEmptyDependency(Model):
    """
    >>> model = ModelWithAcceptableEmptyDependency
    >>> instances = [model.objects.create(slug='hello') for x in range(0,2)]
    >>> [x.slug for x in model.objects.all()]
    [u'hello', u'hello-2']
    """
    date = DateField(blank=True, null=True)
    slug = AutoSlugField(unique_with='date')


class ModelWithAutoUpdateEnabled(Model):
    """
    >>> a = ModelWithAutoUpdateEnabled(name='My name')
    >>> a.save()
    >>> a.slug
    u'my-name'
    >>> a.name = 'My new name'
    >>> a.save()
    >>> a.slug
    u'my-new-name'
    """
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True)


class ModelWithSlugSpaceSharedIntegrityError(ModelWithUniqueSlug):
    """
    >>> a = ModelWithUniqueSlug(name='My name')
    >>> a.save()
    >>> b = ModelWithSlugSpaceSharedIntegrityError(name='My name')
    >>> b.save()
    Traceback (most recent call last):
    ...
    IntegrityError: column slug is not unique
    """


class SharedSlugSpace(Model):
    objects = Manager()
    name = CharField(max_length=200)
    # ensure that any subclasses use the base model's manager for testing
    # slug uniqueness
    slug = AutoSlugField(populate_from='name', unique=True, manager=objects)


class ModelWithSlugSpaceShared(SharedSlugSpace):
    """
    >>> a = SharedSlugSpace(name='My name')
    >>> a.save()
    >>> a.slug
    u'my-name'
    >>> b = ModelWithSlugSpaceShared(name='My name')
    >>> b.save()
    >>> b.slug
    u'my-name-2'
    """

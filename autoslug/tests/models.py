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
from django.db.models import (
    Model, CharField, DateField, DateTimeField, BooleanField, ForeignKey, Manager, CASCADE
)

# this app
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify


class SimpleModel(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField()


class ModelWithUniqueSlug(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


class ModelWithUniqueSlugFK(Model):
    name = CharField(max_length=200)
    simple_model = ForeignKey(SimpleModel, on_delete=CASCADE)
    slug = AutoSlugField(populate_from='name', unique_with='simple_model__name')


class ModelWithUniqueSlugDate(Model):
    date = DateField()
    slug = AutoSlugField(unique_with='date')


class ModelWithUniqueSlugDay(Model):  # same as ...Date, just more explicit
    date = DateTimeField()
    slug = AutoSlugField(unique_with='date__day')


class ModelWithUniqueSlugMonth(Model):
    date = DateField()
    slug = AutoSlugField(unique_with='date__month')


class ModelWithUniqueSlugYear(Model):
    date = DateField()
    slug = AutoSlugField(unique_with='date__year')


class ModelWithLongName(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')


class ModelWithLongNameUnique(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


class ModelWithCallable(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from=lambda instance: 'the %s' % instance.name)


class ModelWithCallableAttr(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='get_name')

    def get_name(self):
        return 'spam, %s and spam' % self.name


class ModelWithNullable(Model):
    name = CharField(max_length=200, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=True, null=True)


class ModelWithBlank(Model):
    name = CharField(max_length=200, blank=True, null=True)
    slug = AutoSlugField(populate_from='name', blank=True)


class ModelWithCustomPrimaryKey(Model):
    custom_primary_key = CharField(primary_key=True, max_length=1)
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)


custom_slugify = lambda value: default_slugify(value).replace('-', '_')


class ModelWithCustomSlugifier(Model):
    slug = AutoSlugField(unique=True, slugify=custom_slugify)


class ModelWithCustomSeparator(Model):
    slug = AutoSlugField(unique=True, sep='_')


class ModelWithReferenceToItself(Model):
    slug = AutoSlugField(unique_with='slug')


class ModelWithWrongReferencedField(Model):
    slug = AutoSlugField(unique_with='wrong_field')


class ModelWithWrongLookupInUniqueWith(Model):
    slug = AutoSlugField(unique_with='name__foo')
    name = CharField(max_length=10)


class ModelWithWrongFieldOrder(Model):
    slug = AutoSlugField(unique_with='date')
    date = DateField(blank=False, null=False)


class ModelWithAcceptableEmptyDependency(Model):
    date = DateField(blank=True, null=True)
    slug = AutoSlugField(unique_with='date')


class ModelWithAutoUpdateEnabled(Model):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', always_update=True)


class ModelWithSlugSpaceSharedIntegrityError(ModelWithUniqueSlug):
    pass


class SharedSlugSpace(Model):
    objects = Manager()
    name = CharField(max_length=200)
    # ensure that any subclasses use the base model's manager for testing
    # slug uniqueness
    slug = AutoSlugField(populate_from='name', unique=True, manager=objects)


class ModelWithSlugSpaceShared(SharedSlugSpace):
    pass


class ModelWithUniqueSlugFKNull(Model):
    name = CharField(max_length=200)
    simple_model = ForeignKey(SimpleModel, null=True, blank=True, default=None, on_delete=CASCADE)
    slug = AutoSlugField(populate_from='name', unique_with='simple_model')


class ModeltranslationOne(Model):
    title = CharField(max_length=255)
    description = CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', always_update=True, unique=True)


class NonDeletedObjects(Manager):
    def get_queryset(self):
        return super(NonDeletedObjects, self).get_queryset().filter(is_deleted=False)


class AbstractModelWithCustomManager(Model):
    is_deleted = BooleanField(default=False)

    objects = NonDeletedObjects()
    all_objects = Manager()

    class Meta:
        abstract = True

    def delete(self, using=None):
        self.is_deleted = True
        self.save()


class NonDeletableModelWithUniqueSlug(AbstractModelWithCustomManager):
    name = CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True, manager_name='all_objects')

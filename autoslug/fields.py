# coding: utf-8
#
#  Copyright (c) 2008—2015 Andy Mikhailenko
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

# django
from django.conf import settings
from django.db.models.fields import SlugField
from django.db.models.signals import post_save

# 3rd-party
try:
    from south.modelsinspector import introspector
except ImportError:
    introspector = lambda self: [], {}

try:
    from modeltranslation import utils as modeltranslation_utils
except ImportError:
    modeltranslation_utils = None

# this app
from autoslug.settings import slugify, autoslug_modeltranslation_enable
from autoslug import utils

__all__ = ['AutoSlugField']

SLUG_INDEX_SEPARATOR = '-'  # the "-" in "foo-2"

try:  # pragma: nocover
    # Python 2.x
    basestring
except NameError:  # pragma: nocover
    # Python 3.x
    basestring = str


class AutoSlugField(SlugField):
    """
    AutoSlugField is an extended SlugField able to automatically resolve name
    clashes.

    AutoSlugField can also perform the following tasks on save:

    - populate itself from another field (using `populate_from`),
    - use custom `slugify` function (using `slugify` or :doc:`settings`), and
    - preserve uniqueness of the value (using `unique` or `unique_with`).

    None of the tasks is mandatory, i.e. you can have auto-populated non-unique
    fields, manually entered unique ones (absolutely unique or within a given
    date) or both.

    Uniqueness is preserved by checking if the slug is unique with given constraints
    (`unique_with`) or globally (`unique`) and adding a number to the slug to make
    it unique.

    :param always_update: boolean: if True, the slug is updated each time the
        model instance is saved. Use with care because `cool URIs don't
        change`_ (and the slug is usually a part of object's URI). Note that
        even if the field is editable, any manual changes will be lost when
        this option is activated.
    :param populate_from: string or callable: if string is given, it is considered
        as the name of attribute from which to fill the slug. If callable is given,
        it should accept `instance` parameter and return a value to fill the slug
        with.
    :param sep: string: if defined, overrides default separator for automatically
        incremented slug index (i.e. the "-" in "foo-2").
    :param slugify: callable: if defined, overrides `AUTOSLUG_SLUGIFY_FUNCTION`
        defined in :doc:`settings`.
    :param unique: boolean: ensure total slug uniqueness (unless more precise
        `unique_with` is defined).
    :param unique_with: string or tuple of strings: name or names of attributes
        to check for "partial uniqueness", i.e. there will not be two objects
        with identical slugs if these objects share the same values of given
        attributes. For instance, ``unique_with='pub_date'`` tells AutoSlugField
        to enforce slug uniqueness of all items published on given date. The
        slug, however, may reappear on another date. If more than one field is
        given, e.g. ``unique_with=('pub_date', 'author')``, then the same slug may
        reappear within a day or within some author's articles but never within
        a day for the same author. Foreign keys are also supported, i.e. not only
        `unique_with='author'` will do, but also `unique_with='author__name'`.

    .. _cool URIs don't change: http://w3.org/Provider/Style/URI.html

    .. note:: always place any slug attribute *after* attributes referenced
        by it (i.e. those from which you wish to `populate_from` or check
        `unique_with`). The reasoning is that autosaved dates and other such
        fields must be already processed before using them in the AutoSlugField.

    Example usage:

    .. code-block:: python

        from django.db import models
        from autoslug import AutoSlugField

        class Article(models.Model):
            '''An article with title, date and slug. The slug is not totally
            unique but there will be no two articles with the same slug within
            any month.
            '''
            title = models.CharField(max_length=200)
            pub_date = models.DateField(auto_now_add=True)
            slug = AutoSlugField(populate_from='title', unique_with='pub_date__month')


    More options:

    .. code-block:: python

        # slugify but allow non-unique slugs
        slug = AutoSlugField()

        # globally unique, silently fix on conflict ("foo" --> "foo-1".."foo-n")
        slug = AutoSlugField(unique=True)

        # autoslugify value from attribute named "title"; editable defaults to False
        slug = AutoSlugField(populate_from='title')

        # same as above but force editable=True
        slug = AutoSlugField(populate_from='title', editable=True)

        # ensure that slug is unique with given date (not globally)
        slug = AutoSlugField(unique_with='pub_date')

        # ensure that slug is unique with given date AND category
        slug = AutoSlugField(unique_with=('pub_date','category'))

        # ensure that slug is unique with an external object
        # assuming that author=ForeignKey(Author)
        slug = AutoSlugField(unique_with='author')

        # ensure that slug is unique with a subset of external objects (by lookups)
        # assuming that author=ForeignKey(Author)
        slug = AutoSlugField(unique_with='author__name')

        # mix above-mentioned behaviour bits
        slug = AutoSlugField(populate_from='title', unique_with='pub_date')

        # minimum date granularity is shifted from day to month
        slug = AutoSlugField(populate_from='title', unique_with='pub_date__month')

        # autoslugify value from a dynamic attribute (i.e. a method)
        slug = AutoSlugField(populate_from='get_full_name')

        # autoslugify value from a custom callable
        # (ex. usage: user profile models)
        slug = AutoSlugField(populate_from=lambda instance: instance.user.get_full_name())

        # specify model manager for looking up slugs shared by subclasses

        class Article(models.Model):
            '''An article with title, date and slug. The slug is not totally
            unique but there will be no two articles with the same slug within
            any month.
            '''
            objects = models.Manager()
            title = models.CharField(max_length=200)
            slug = AutoSlugField(populate_from='title', unique_with='pub_date__month', manager=objects)

        class NewsArticle(Article):
            pass

        # autoslugify value using custom `slugify` function
        from autoslug.settings import slugify as default_slugify
        def custom_slugify(value):
            return default_slugify(value).replace('-', '_')
        slug = AutoSlugField(slugify=custom_slugify)

    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)

        # autopopulated slug is not editable unless told so
        self.populate_from = kwargs.pop('populate_from', None)
        if self.populate_from:
            kwargs.setdefault('editable', False)

        # unique_with value can be string or tuple
        self.unique_with = kwargs.pop('unique_with', ())
        if isinstance(self.unique_with, basestring):
            self.unique_with = (self.unique_with,)

        self.slugify = kwargs.pop('slugify', slugify)
        assert hasattr(self.slugify, '__call__')

        self.index_sep = kwargs.pop('sep', SLUG_INDEX_SEPARATOR)

        if self.unique_with:
            # we will do "manual" granular check below
            kwargs['unique'] = False

        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True

        # A boolean instructing the field to accept Unicode letters in
        # addition to ASCII letters. Defaults to False.
        self.allow_unicode = kwargs.pop('allow_unicode', False)

        # When using model inheritence, set manager to search for matching
        # slug values
        self.manager = kwargs.pop('manager', None)
        self.manager_name = kwargs.pop('manager_name', None)

        self.always_update = kwargs.pop('always_update', False)
        super(SlugField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()

        if self.max_length == 50:
            kwargs.pop('max_length', None)

        if self.populate_from is not None:
            kwargs['populate_from'] = self.populate_from
            if self.editable is not False:
                kwargs['editable'] = self.editable

        if self.unique_with != ():
            kwargs['unique_with'] = self.unique_with
            kwargs.pop('unique', None)

        if self.slugify != slugify:
            kwargs['slugify'] = self.slugify

        if self.index_sep != SLUG_INDEX_SEPARATOR:
            kwargs['sep'] = self.index_sep

        kwargs.pop('db_index', None)

        if self.manager is not None:
            kwargs['manager'] = self.manager

        if self.manager_name is not None:
            kwargs['manager_name'] = self.manager_name

        if self.always_update:
            kwargs['always_update'] = self.always_update

        if 'manager' in kwargs:
            del kwargs['manager']

        return name, path, args, kwargs

    def pre_save(self, instance, add):

        # get currently entered slug
        value = self.value_from_object(instance)

        if self.manager is not None:
            manager = self.manager
        elif self.manager_name is not None:
            manager = getattr(self.model, self.manager_name)
        else:
            manager = None

        # autopopulate
        if self.always_update or (self.populate_from and not value):
            value = utils.get_prepopulated_value(self, instance)

            # pragma: nocover
            if __debug__ and not value and not self.blank:
                print('Failed to populate slug %s.%s from %s' % \
                      (instance._meta.object_name, self.name, self.populate_from))

        slug = None
        if value:
            slug = self.slugify(value)
        if not slug:
            slug = None

            if not self.blank:
                slug = instance._meta.model_name
            elif not self.null:
                slug = ''

        if slug:
            slug = utils.crop_slug(self, slug)

            # ensure the slug is unique (if required)
            if self.unique or self.unique_with:
                slug = utils.generate_unique_slug(self, instance, slug, manager)

            assert slug, 'value is filled before saving'

        # make the updated slug available as instance attribute
        setattr(instance, self.name, slug)

        # modeltranslation support
        if 'modeltranslation' in settings.INSTALLED_APPS \
                and not hasattr(self.populate_from, '__call__') \
                and autoslug_modeltranslation_enable:
            post_save.connect(modeltranslation_update_slugs, sender=type(instance))

        return slug


    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        args, kwargs = introspector(self)
        kwargs.update({
            'populate_from': 'None' if callable(self.populate_from) else repr(self.populate_from),
            'unique_with': repr(self.unique_with)
        })
        return ('autoslug.fields.AutoSlugField', args, kwargs)


def modeltranslation_update_slugs(sender, **kwargs):
    # https://bitbucket.org/neithere/django-autoslug/pull-request/11/modeltranslation-support-fix-issue-19/
    # http://django-modeltranslation.readthedocs.org
    #
    # TODO: tests
    #
    if not modeltranslation_utils:
        return

    instance = kwargs['instance']
    slugs = {}

    for field in instance._meta.fields:
        if type(field) != AutoSlugField:
            continue
        if not field.populate_from:
            continue
        for lang in settings.LANGUAGES:
            lang_code, _ = lang
            lang_code = lang_code.replace('-', '_')

            populate_from_localized = modeltranslation_utils.build_localized_fieldname(field.populate_from, lang_code)
            field_name_localized = modeltranslation_utils.build_localized_fieldname(field.name, lang_code)

            # The source field or the slug field itself may not be registered
            # with translator
            if not hasattr(instance, populate_from_localized):
                continue
            if not hasattr(instance, field_name_localized):
                continue

            populate_from_value = getattr(instance, populate_from_localized)
            field_value = getattr(instance, field_name_localized)

            if not field_value or field.always_update:
                slug = field.slugify(populate_from_value)
                slugs[field_name_localized] = slug

    sender.objects.filter(pk=instance.pk).update(**slugs)

# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008—2009 Andy Mikhailenko
#
#  This file is part of django-autoslug.
#
#  django-autoslug is free software under terms of the GNU Lesser
#  General Public License version 3 (LGPLv3) as published by the Free
#  Software Foundation. See the file README for copying conditions.
#

# django
from django.db.models.fields import DateField, SlugField

# app
from autoslug.settings import slugify

class AutoSlugField(SlugField):
    """
    AutoSlugField is a slug field that can automatically do the following on save:
    - populate itself from another field (using `populate_from`),
    - use custom slugify() function (can be defined in settings), and
    - preserve uniqueness of the value (using `unique` or `unique_with`).

    None of the tasks is mandatory, i.e. you can have auto-populated non-unique fields,
    manually entered unique ones (absolutely unique or within a given date) or both.

    Uniqueness is preserved by checking if the slug is unique with given constraints
    (unique_with) or globally (unique) and adding a number to the slug to make
    it unique. See examples below.

    .. warning:: always declare attributes with AutoSlugField *after* attributes
        from which you wish to 'populate_from' or check 'unique_with' because
        autosaved ates and other such fields must be already processed before
        the checking occurs.

    Usage examples::

        # slugify but allow non-unique slugs
        slug = AutoSlugField()

        # globally unique, silently fix on conflict ("foo" --> "foo-1".."foo-n")
        slug = AutoSlugField(unique=True)

        # autoslugify value from title attr; default editable to False
        slug = AutoSlugField(populate_from='title')

        # same as above but force editable=True
        slug = AutoSlugField(populate_from='title', editable=True)

        # ensure that slug is unique with given date (not globally)
        slug = AutoSlugField(unique_with='pub_date')

        # ensure that slug is unique with given date AND category
        slug = AutoSlugField(unique_with=('pub_date','category'))

        # mix above-mentioned behaviour bits
        slug = AutoSlugField(populate_from='title', unique_with='pub_date')

        # minimum date granularity is shifted from day to month
        slug = AutoSlugField(populate_from='title', unique_with='pub_date__month')

    Please don't forget to declare your slug attribute after the fields
    referenced in `populate_from` and `unique_with`.
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

        # backward compatibility
        if kwargs.get('unique_with_date'):
            from warnings import warn
            warn('Using unique_with_date="foo" in AutoSlugField is deprecated, '\
                 'use unique_with=("foo",) instead.', DeprecationWarning)
            self.unique_with += (kwargs['unique_with_date'],)

        if self.unique_with:
            # we will do "manual" granular check below
            kwargs['unique'] = False
        else:
            # force full uniqueness
            kwargs['unique'] = True

        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(SlugField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        # get currently entered slug
        value = self.value_from_object(instance)

        slug = None

        # autopopulate (unless the field is editable and has some value)
        if value:
            slug = slugify(value)
        elif self.populate_from: # and not self.editable:
            slug = slugify(getattr(instance, self.populate_from))

        if not slug:
            # no incoming value,  use model name
            slug = instance._meta.module_name

        assert slug, 'slug is defined before trying to ensure uniqueness'

        # ensure the slug is unique (if required)
        if self.unique or self.unique_with:
            slug = self._generate_unique_slug(instance, slug)

        assert slug, 'value is filled before saving'

        setattr(instance, self.name, slug) # XXX do we need this?

        return slug
        #return super(AutoSlugField, self).pre_save(instance, add)

    def _generate_unique_slug(self, instance, slug):
        """
        Generates unique slug by adding a number to given value until no model
        is found with such slug. If ``unique_with`` (a tuple of field names) was
        specified for the field, all these fields are included together
        in the query when looking for a "rival" model instance.
        """
        def _get_lookups(instance):
            "Returns a dict'able tuple of lookups to ensure slug uniqueness"
            for _field_name in self.unique_with:
                field_name, inner = _field_name, None

                field = instance._meta.get_field(field_name)

                # `inner` is the 'month' part in 'pub_date__month'.
                # it *only* applies to dates, otherwise it's just ignored.
                if '__' in field:
                    field_name, inner = field.split('__')

                value = getattr(instance, field_name)
                if not value:
                    raise ValueError, 'Could not check uniqueness of %s.%s with'\
                        ' respect to %s.%s because the latter is empty. Please'\
                        ' ensure that "%s" is declared *after* all fields it'\
                        ' depends on (i.e. "%s"), and that they are not blank.'\
                        % (instance._meta.object_name, self.name,
                           instance._meta.object_name, field_name,
                           self.name, '", "'.join(self.unique_with))
                if isinstance(field, DateField):    # DateTimeField is a DateField subclass
                    inner = inner or 'day'
                    parts = 'year', 'month', 'day'
                    try:
                        granularity = parts.index(inner) + 1
                    except ValueError:
                        raise ValueError('expected one of %s, got "%s" in "%s"'
                                         % (parts, inner, _field_name))
                    else:
                        for part in parts[:granularity]:
                            lookup = '%s__%s' % (field_name, part)
                            yield (lookup, getattr(value, part))
                else:
                    yield (field_name, value)
        lookups = tuple(_get_lookups(instance))
        model = instance.__class__
        field_name = self.name
        index = 1
        orig_slug = slug
        # keep changing the slug until it is unique
        while True:
            try:
                # raise model.DoesNotExist if current slug is unique
                rival = model.objects.get(**dict(lookups + ((self.name, slug),) ))
                # not unique, but maybe the "rival" is the instance itself?
                if rival.id == instance.id:
                    raise model.DoesNotExist
                # the slug is not unique; change once more
                index += 1
                slug = '%s-%d' % (orig_slug, index)
            except model.DoesNotExist:
                # slug is unique, no model uses it
                return slug

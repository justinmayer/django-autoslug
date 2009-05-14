# -*- coding: utf-8 -*-

# Original snippet: http://djangosnippets.org/snippets/728/
# Reworked by Andy Mikhailenko <neithere at gmail dot com> in Sep 2008

# django
from django.db.models.fields import DateField, SlugField

# app
from autoslugfield.settings import slugify

class AutoSlugField(SlugField):
    """ A slug field which can automatically do the following two tasks on save:
    - populate itself from another field (using 'populate_from'), and
    - preserve uniqueness of the value (using 'unique' or 'unique_with_date').
    
    None of the tasks is mandatory, i.e. you can have auto-populated non-unique fields,
    manually entered unique ones (absolutely unique or within a given date) or both.

    If both unique_with and unique_with_date are declared,
    
    IMPORTANT NOTE: always declare attributes with AutoSlugField *after* attributes
    from which you wish to 'populate_from' or check 'unique_with_date' because autosaved
    dates and other such fields must be already processed before using them from here.
    
    Usage examples:

    # force unique=True, silently fix on conflict
    slug = AutoSlugField()
    
    # autoslugify value from title attr; default editable to False
    slug = AutoSlugField(populate_from='title')
    
    # same as above but force editable=True
    slug = AutoSlugField(populate_from='title', editable=True)
    
    # force unique=False but ensure that slug is unique for given date
    slug = AutoSlugField(unique_with=('pub_date',))
    
    # mix above-mentioned behaviour bits
    slug = AutoSlugField(unique_with=('pub_date',), populate_from='title')

    # ensure uniqueness for more than one field (intersection will be checked)
    slug = AutoSlugField(unique_with=('pub_date','category'), populate_from='title')
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

        # force full uniqueness unless more granular is specified
        if not self.unique_with:
            kwargs.setdefault('unique', True)

        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(SlugField, self).__init__(*args, **kwargs)

    def pre_save(self, instance, add):
        # get currently entered slug
        value = self.value_from_object(instance)
        
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
        is found with such slug. If unique_with (a tuple of field names) was
        specified for the field, all these fields are included together
        in the query when looking for a "rival" model instance.
        """
        def _get_lookups(instance):
            "Returns a dict'able tuple of lookups to ensure slug uniqueness"
            for field_name in self.unique_with:
                field = instance._meta.get_field(field_name)
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
                    for part in 'year', 'month', 'day':
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

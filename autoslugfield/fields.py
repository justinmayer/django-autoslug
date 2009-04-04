# -*- coding: utf-8 -*-

# Original snippet: http://djangosnippets.org/snippets/728/
# Reworked by Andy Mikhailenko <neithere at gmail dot com> in Sep 2008

# django
from django.db.models.fields import SlugField

# app
from autoslugfield.settings import slugify

class AutoSlugField(SlugField):
    """ A slug field which can automatically do the following two tasks on save:
    - populate itself from another field (using 'populate_from'), and
    - preserve uniqueness of the value (using 'unique' or 'unique_for_date').
    
    None of the tasks is mandatory, i.e. you can have auto-populated non-unique fields,
    manually entered unique ones (absolutely unique or within a given date) or both.
    
    IMPORTANT NOTE: always declare attributes with AutoSlugField *after* attributes
    from which you wish to 'populate_from' or check 'unique_for_date' because autosaved
    dates and other such fields must be already processed before using them from here.
    
    Usage examples:

    # force unique=True, silently fix on conflict
    slug = AutoSlugField()
    
    # autoslugify value from title attr; default editable to False
    slug = AutoSlugField(populate_from='title')
    
    # same as above but force editable=True
    slug = AutoSlugField(populate_from='title', editable=True)
    
    # force unique=False but ensure that slug is unique for given date
    slug = AutoSlugField(unique_for_date='pub_date')
    
    # mix above-mentioned behaviour bits
    slug = AutoSlugField(unique_for_date='pub_date', populate_from='title')
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 50)
        self._populate_from  = kwargs.pop('populate_from', None)
        if self._populate_from:
            kwargs.setdefault('editable', False)
        if not kwargs.get('unique_for_date',None):
            kwargs.setdefault('unique', True)
        # Set db_index=True unless it's been set manually.
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(SlugField, self).__init__(*args, **kwargs)

    def _get_unique_slug(self, model_instance, slug):
        model = model_instance.__class__
        field_name = self.name
        index = 1
        orig_slug = slug
        while True:
            try:
                qargs = {field_name: slug}
                if self.unique_for_date:
                    date = getattr(model_instance, self.unique_for_date)
                    for part in ('year', 'month', 'day'):
                        lookup = '%s__%s' % (self.unique_for_date, part)
                        qargs[lookup] = getattr(date, part)
                o = model.objects.get(**qargs)
                if model_instance.id and o.id == model_instance.id:
                    raise model.DoesNotExist
                index += 1
                slug = '%s-%d' % (orig_slug, index)
            except model.DoesNotExist:
                return slug

    def _prepare_slug(self, model_instance):
        # get currently entered slug
        slug = self.value_from_object(model_instance)
        # autopopulate (unless the field is editable and has some value)
        if self._populate_from:
            if slug and self.editable:
                pass
            else:
                slug = slugify(getattr(model_instance, self._populate_from))
        # ensure the slug is unique (if required)
        if self.unique or self.unique_for_date:
            return self._get_unique_slug(model_instance, slug)
        else:
            return slugify(slug)
        return super(AutoSlugField, self).pre_save(model_instance, add)

    def pre_save(self, model_instance, add):
        value = self._prepare_slug(model_instance)
        setattr(model_instance, self.name, value)
        return value

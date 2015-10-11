import io


__all__ = ['__version__']


# A simple `from autoslug import __version__` would trigger a cascading import
# of `autoslug.fields`, then `django`.  As the latter may not be available
# (being a dependency), we try to work around it.
#
# Cases:
# 1) building the package with a global interpreter and no dependencies
#    installed globally;
# 2) building documentation e.g. on RTFD server (no Django settings available
#    on runtime);
# 3) installing django-autoslug before Django itself (highly unlikely).
#
__version__ = None
with io.open('autoslug/__init__.py', encoding='utf8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)
            break
assert __version__, 'autoslug.__version__ must be imported correctly'

"""
Dynamic settings loader based on DJANGO_ENV environment variable.
"""
import os

env_mode = os.environ.get('DJANGO_ENV', 'development')

if env_mode == 'production':
    from .production import *
else:
    from .development import *

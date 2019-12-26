# flake8: noqa

# Settings for live deployed environments: vagrant, staging, production, etc
import os

from .base import *  # noqa

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

#: deploy environment - e.g. "staging" or "production"
ENVIRONMENT = os.environ.get('ENVIRONMENT',"production")


DEBUG = True


if 'MEDIA_ROOT' in os.environ:
    MEDIA_ROOT = os.getenv('MEDIA_ROOT')


if 'DATABASE_URL' in os.environ:
    # Dokku
    SECRET_KEY = "0!f^p$0k4i30#b2h=k(_9c!l4u36os#$euaimbp!+k%7u_=fz*"

    import dj_database_url
    # Update database configuration with $DATABASE_URL.
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

    # Disable Django's own staticfiles handling in favour of WhiteNoise, for
    # greater consistency between gunicorn and `./manage.py runserver`. See:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    INSTALLED_APPS.remove('django.contrib.staticfiles')
    INSTALLED_APPS.extend([
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
    ])

    #tuple(list(MIDDLEWARE).remove('django.middleware.security.SecurityMiddleware'))
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ] + MIDDLEWARE

    # Allow all host headers (feel free to make this more specific)
    ALLOWED_HOSTS = ['*']

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    WEBSERVER_ROOT = os.path.join(PROJECT_ROOT, 'www')
else:
    SECRET_KEY = "0!f^p$0k4i30#b2h=k(_9c!l4u36os#$euaimbp!+k%7u_=fz*"

    DATABASES['default']['NAME'] = 'AQIService_%s' % ENVIRONMENT.lower()
    DATABASES['default']['USER'] = 'AQIService_%s' % ENVIRONMENT.lower()
    DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
    DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
    DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')

    WEBSERVER_ROOT = '/var/www/AQIService/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
# use TLS or SSL, not both:
assert not (EMAIL_USE_TLS and EMAIL_USE_SSL)
if EMAIL_USE_TLS:
    default_smtp_port = 587
elif EMAIL_USE_SSL:
    default_smtp_port = 465
else:
    default_smtp_port = 25
EMAIL_PORT = os.environ.get('EMAIL_PORT', default_smtp_port)
EMAIL_SUBJECT_PREFIX = '[Aqiservice %s] ' % ENVIRONMENT.title()
DEFAULT_FROM_EMAIL = 'noreply@%(DOMAIN)s' % os.environ
SERVER_EMAIL = DEFAULT_FROM_EMAIL

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = [os.environ['DOMAIN']]

# Use template caching on deployed servers
for backend in TEMPLATES:
    if backend['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
        default_loaders = ['django.template.loaders.filesystem.Loader']
        if backend.get('APP_DIRS', False):
            default_loaders.append('django.template.loaders.app_directories.Loader')
            # Django gets annoyed if you both set APP_DIRS True and specify your own loaders
            backend['APP_DIRS'] = False
        loaders = backend['OPTIONS'].get('loaders', default_loaders)
        for loader in loaders:
            if len(loader) == 2 and loader[0] == 'django.template.loaders.cached.Loader':
                # We're already caching our templates
                break
        else:
            backend['OPTIONS']['loaders'] = [('django.template.loaders.cached.Loader', loaders)]

# Uncomment if using celery worker configuration
# CELERY_SEND_TASK_ERROR_EMAILS = True
# BROKER_URL = 'amqp://AQIService_%(ENVIRONMENT)s:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/AQIService_%(ENVIRONMENT)s' % os.environ  # noqa

# Environment overrides
# These should be kept to an absolute minimum
if ENVIRONMENT.upper() == 'LOCAL':
    # Don't send emails from the Vagrant boxes
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if 'DOKKU_NGINX_SSL_PORT' in os.environ:
    # Dokku with SSL
    # SECURE_SSL_REDIRECT = True
    # Try HTTP Strict Transport Security (increase time if everything looks okay)
    # SECURE_HSTS_SECONDS = 1800
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_REDIRECT_EXEMPT = ['/.well-known']  # For Let's Encrypt

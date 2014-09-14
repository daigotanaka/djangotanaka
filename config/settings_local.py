import os

DEBUG = True

DEBUG_PROPAGATE_EXCEPTIONS = True
TASTYPIE_FULL_DEBUG = True

# If you use foreman, don't forget to define those in .env
LOCAL_POSTGRES_DBNAME = os.getenv('LOCAL_POSTGRES_DBNAME')
LOCAL_POSTGRES_USERNAME = os.getenv('LOCAL_POSTGRES_USERNAME')
LOCAL_POSTGRES_PASSWORD = os.getenv('LOCAL_POSTGRES_PASSWORD')

DJANGO_USERNAME = os.getenv('DJANGO_USERNAME')
DJANGO_API_KEY = os.getenv('DJANGO_API_KEY')

WEBSITE_URL = "http://0.0.0.0:5000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': LOCAL_POSTGRES_DBNAME,            # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': LOCAL_POSTGRES_USERNAME,
        'PASSWORD': LOCAL_POSTGRES_PASSWORD,
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '7501',                      # Set to empty string for default.
    }
}

print DATABASES



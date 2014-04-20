import dj_database_url


DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES = {}
DATABASES['default'] =  dj_database_url.config()

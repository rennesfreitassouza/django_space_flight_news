from .base import *  # noqa
from .base import env, local_env_dir
from django.core.management.utils import get_random_secret_key
#print("local_env_dir", local_env_dir)
# GENERAL
# ------------------------------------------------------------------------------
# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)
print('DEBUG', DEBUG)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default=get_random_secret_key(),
)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
     'default': env.db(
         "DATABASE_URL",
         default="""{\"ENGINE\": 'django.db.backends.sqlite3',
                  "NAME": os.path.join(ROOT_DIR, 'db.sqlite3')}""",
     ),
}
DATABASES["OPTIONS"] = {'sslmode': 'require'}

# https://docs.djangoproject.com/en/4.0/ref/settings/#atomic-requests
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

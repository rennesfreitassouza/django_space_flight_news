from .base import *  # noqa
<<<<<<< HEAD
from .base import env
from django.core.management.utils import get_random_secret_key

=======
from .base import env, local_env_dir
from django.core.management.utils import get_random_secret_key
#print("local_env_dir", local_env_dir)
>>>>>>> main
# GENERAL
# ------------------------------------------------------------------------------
# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)
<<<<<<< HEAD
print(f"{__file__} DEBUG ", DEBUG)
=======
print('DEBUG', DEBUG)
>>>>>>> main
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
<<<<<<< HEAD
         default="postgres:///sfn",
=======
         default="""{\"ENGINE\": 'django.db.backends.sqlite3',
                  "NAME": os.path.join(ROOT_DIR, 'db.sqlite3')}""",
>>>>>>> main
     ),
}
DATABASES["OPTIONS"] = {'sslmode': 'require'}

# https://docs.djangoproject.com/en/4.0/ref/settings/#atomic-requests
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
<<<<<<< HEAD

AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env.str('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID =  env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
=======
>>>>>>> main

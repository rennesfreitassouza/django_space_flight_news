from .base import *  # noqa
from .base import env


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", True)
print("local.py DJANGO_DEBUG", DEBUG)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-=ag=+j15r!klsf%j-hofj9l*6jl$est49lv%(99xcqsq2(()ei",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
print("DJANGO_ALLOWED_HOSTS", ALLOWED_HOSTS)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE'),
        'USER': env.str('USER'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': env.str('HOST'),
        'PORT': env.str('PORT'),
        'TEST_NAME': os.path.join(ROOT_DIR, 'test_' + env.str('DATABASE')),
        #'OPTIONS': {'sslmode': 'require'},
    }
}
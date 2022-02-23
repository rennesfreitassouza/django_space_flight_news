"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="Vb6jizUfTtew3U8PKH4loVGzV474ZQStHYbYXMpjbhzDmaoAlLDOVNofjxplHkpC",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
#TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
#PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
#EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Your stuff...
# ------------------------------------------------------------------------------

# local tests
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

# remote tests
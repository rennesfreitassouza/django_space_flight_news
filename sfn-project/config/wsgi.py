"""
WSGI config for sfn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application


# sfn-project directory.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
#sys.path.append(str(ROOT_DIR / "sfn-project"))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()

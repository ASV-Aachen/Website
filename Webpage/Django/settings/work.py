import os
from Django.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'websiteDB',
        'USER': os.environ["MYSQL_USER"],
        'PASSWORD': os.environ["MYSQL_PASSWORD"],
        'HOST': 'db',   # Or an IP Address that your DB is hosted on
        'PORT': 3306,
    }
}



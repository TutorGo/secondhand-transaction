# debug.py
import urllib

from config.settings.deploy import config_secret_deploy
from .base import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

# WSGI application
WSGI_APPLICATION = 'config.wsgi.debug.application'

# Static URLs
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static_root')

#  media
MEDIA_URL = '/.media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# 디버그모드니까 DEBUG는 True
DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

SITE_URL = 'http://localhost:8000'

NAVER_APP_ID = 'zaZpSNfZzYCNisIZs3L1'
NAVER_SECRET_KEY = common['naver']['local_secret_key']

# Celery
CELERY_BROKER_TRANSPORT = 'sqs'
CELERY_BROKER_URL = 'sqs://{aws_access_key_id}:{aws_secret_access_key}@'.format(
    aws_access_key_id=urllib.parse.quote(config_secret_deploy['aws']['access_key_id'], safe=''),
    aws_secret_access_key=urllib.parse.quote(config_secret_deploy['aws']['secret_access_key'], safe=''),
)
# CELERY_BROKER_URL = 'https://sqs.ap-northeast-2.amazonaws.com/982738052650/celery'
# CELERY_BROKER_URL = 'redis://redis-test.s9cegi.0001.apn2.cache.amazonaws.com:6379'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'ap-northeast-2',
}
CELERY_RESULT_BACKEND = 'django-db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


print('@@@@@@ DEBUG:', DEBUG)
print('@@@@@@ ALLOWED_HOSTS:', ALLOWED_HOSTS)

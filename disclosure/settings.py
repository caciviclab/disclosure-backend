import os
import os.path as op

BASE_DIR = op.dirname(__file__)
REPO_DIR = op.join(BASE_DIR, os.pardir)
SECRET_KEY = 'w11nbg_3n4+e@qk^b55qgo5qygesn^3=&s1kwtlbpkai$(1jv3'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
STATIC_ROOT = op.join(BASE_DIR, ".static")

try:
    # Set CALACCESS_TEST_DOWNLOAD_DIR for testing calaccess data commands.
    import calaccess_raw
    _calaccess_repo_dir = op.join(op.dirname(calaccess_raw.__file__),
                                  os.pardir)
    CALACCESS_TEST_DOWNLOAD_DIR = op.join(_calaccess_repo_dir,
                                          'example', 'test-data')
except:
    pass

CALACCESS_DOWNLOAD_DIR = op.join(REPO_DIR, 'data', 'calaccess')
NETFILE_DOWNLOAD_DIR = op.join(REPO_DIR, 'data', 'netfile')


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'calaccess_raw',
    'netfile_raw',
    'zipcode_metro_raw',
    'locality',
    'ballot_measure',
    'election_day',
    'disclosure'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'disclosure.urls'
WSGI_APPLICATION = 'disclosure.wsgi.application'
REST_FRAMEWORK = {
    'VIEW_NAME_FUNCTION': ('disclosure.'
                           'swagger_nickname.view_name')
}

DATABASES = {
    'default': {
        'NAME': 'calaccess_raw',
        'PASSWORD': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'local_infile': 1,
        }
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

try:
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, 'settings_local.py')) as fp:
        exec(fp.read())
except:
    pass

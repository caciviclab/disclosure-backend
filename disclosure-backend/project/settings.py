import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPO_DIR = os.path.join(BASE_DIR, os.pardir)
SECRET_KEY = 'w11nbg_3n4+e@qk^b55qgo5qygesn^3=&s1kwtlbpkai$(1jv3'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
STATIC_ROOT = os.path.join(REPO_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(REPO_DIR, 'frontend'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'calaccess_raw',
    'netfile',
    'project',
    'zipcode_metro',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
    'pipeline_browserify.compiler.BrowserifyCompiler',
)

PIPELINE_CSS = {
    'app': {
        'source_filenames' : (
            'app/app.less',
        ),
        'output_filename': 'app.css',
    },
}

PIPELINE_JS = {
    'bundle': {
        'source_filenames' : (
            'app/app.browserify.js',
        ),
        'output_filename': 'bundle.js',
    },
    'vendor': {
        'source_filenames' : (
            'thirdparty/index.browserify.js',
        ),
        'output_filename': 'vendor.js',
    },
}

PIPELINE_LESS_BINARY = os.path.join(REPO_DIR, 'node_modules', '.bin', 'lessc')
PIPELINE_BROWSERIFY_BINARY = os.path.join(REPO_DIR, 'node_modules', '.bin', 'browserify')
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

if DEBUG:
    PIPELINE_BROWSERIFY_ARGUMENTS = '-d'

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

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
    from project.settings_local import *
except ImportError:
    pass

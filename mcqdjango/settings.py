from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (bool(int(os.environ.get('DEBUG',1))))  #True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django_static_jquery',
    'amplitude',
    'crispy_forms',
    'mcqgenerator.apps.McqgeneratorConfig',
    'users.apps.UsersConfig',
    'blogs.apps.BlogsConfig',
    'surveys.apps.SurveysConfig',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'amplitude.middleware.SessionInfo',
    'amplitude.middleware.SendPageViewEvent',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcqdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
        os.path.join(BASE_DIR, 'mcqgenerator', 'templates', 'mcqgenerator'),
        os.path.join(BASE_DIR, 'blogs', 'templates', 'blogs'),
        os.path.join(BASE_DIR, 'surveys', 'templates', 'surveys'),
        os.path.join(BASE_DIR, 'users', 'templates', 'users')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]


WSGI_APPLICATION = 'mcqdjango.wsgi.application'


# Settings > Projects > <Your project> > General > API Key
AMPLITUDE_API_KEY = '0509cf23bbf05ae34310ddb2d6f928cd'

# You can also choose if you want to include user and group data (Default False)
AMPLITUDE_INCLUDE_USER_DATA = False
AMPLITUDE_INCLUDE_GROUP_DATA = False

AMPLITUDE_IGNORE_URLS = ['admin', '/admin']


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler"]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


LOGOUT_REDIRECT_URL = 'mcqgenerator:file_drop'
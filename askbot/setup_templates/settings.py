# Django settings for ASKBOT enabled project.
import os.path
import logging
import sys
import askbot

#this line is added so that we can import pre-packaged askbot dependencies
sys.path.append(os.path.join(os.path.dirname(askbot.__file__), 'deps'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # only mysql is supported, more will be in the near future
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

#mail server settings
SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[ASKBOT] '
EMAIL_HOST='askbot.org'
EMAIL_PORT='25'
EMAIL_USE_TLS=False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LANGUAGE_CODE = 'en'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
ASKBOT_FILE_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'askbot', 'upfiles')

PROJECT_ROOT = os.path.dirname(__file__)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = 'sdljdfjkldsflsdjkhsjkldgjlsdgfs s ' 

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    #below is askbot stuff for this tuple
    'askbot.skins.loaders.load_template_source',
    #'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    #'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',

    #below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.pagesize.QuestionsPageSizeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    #'askbot.deps.recaptcha_django.middleware.ReCaptchaMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',
)


ROOT_URLCONF = os.path.basename(os.path.dirname(__file__)) + '.urls'


#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__), 
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


TEMPLATE_DIRS = (
    #specific to askbot
    os.path.join(os.path.dirname(__file__),'askbot','skins').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'askbot.context.application_settings',
    #'django.core.context_processors.i18n',
    'askbot.user_messages.context_processors.user_messages',#must be before auth
    'django.core.context_processors.auth', #this is required for admin
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    #all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'debug_toolbar',
    'askbot',
    'askbot.deps.django_authopenid',
    #'askbot.importers.stackexchange', #se loader
    'south',
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
)


#setup memcached for production use!
#see http://docs.djangoproject.com/en/1.1/topics/cache/ for details
CACHE_BACKEND = 'locmem://'
#needed for django-keyedcache
CACHE_TIMEOUT = 6000
CACHE_PREFIX = 'askbot' #make this unique
#If you use memcache you may want to uncomment the following line to enable memcached based sessions
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache_db'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

#this needs to go
USE_EXTERNAL_LEGACY_LOGIN = False #DO NOT USE, and do not delete this line, will be removed later
if 'USE_EXTERNAL_LEGACY_LOGIN' in locals() and USE_EXTERNAL_LEGACY_LOGIN:
    INSTALLED_APPS += (EXTERNAL_LEGACY_LOGIN_MODULE,)

    if 'EXTERNAL_LEGACY_LOGIN_AUTHENTICATION_BACKEND' in locals():
        AUTHENTICATION_BACKENDS += (EXTERNAL_LEGACY_LOGIN_AUTHENTICATION_BACKEND,)
    if 'EXTERNAL_LEGACY_LOGIN_AUTHENTICATION_MIDDLEWARE' in locals():
        MIDDLEWARE_CLASSES += (EXTERNAL_LEGACY_LOGIN_AUTHENTICATION_MIDDLEWARE,)
    def LOAD_EXTERNAL_LOGIN_APP():
        return __import__(EXTERNAL_LEGACY_LOGIN_MODULE, [], [], ['api','forms','views'])
else:
    LOAD_EXTERNAL_LOGIN_APP = lambda: None


#logging settings
LOG_FILENAME = 'askbot.log'
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'log', LOG_FILENAME),
    level=logging.DEBUG,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = '' #no leading slash, default = '' empty string
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL,_('account/'),_('signin/'))
#note - it is important that upload dir url is NOT translated!!!
ASKBOT_UPLOADED_FILES_URL = '/%s%s' % (ASKBOT_URL, 'upfiles/')

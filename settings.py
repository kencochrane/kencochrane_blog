# Django settings for mysite project.
import os
import deploy

DEBUG = deploy.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = deploy.ADMINS
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True

# Site owner will be used throughout the site.
# This should represent the site author.
SITE_OWNER = deploy.SITE_OWNER
SITE_TITLE = deploy.SITE_TITLE

# These should be defined in the local_settings.py file
EMAIL_HOST = deploy.EMAIL_HOST
EMAIL_HOST_PASSWORD = deploy.EMAIL_HOST_PASSWORD
EMAIL_HOST_USER = deploy.EMAIL_HOST_USER
EMAIL_PORT = deploy.EMAIL_PORT
SERVER_EMAIL = deploy.SERVER_EMAIL

DATABASES = deploy.DATABASES

CACHE_BACKEND = deploy.CACHE_BACKEND
TIME_ZONE = deploy.TIME_ZONE
LANGUAGE_CODE = 'en-us'
USE_I18N = False

SITE_ID = 1

# Base directory (all other paths should be relative to this path, rather 
# than hard-coded)
BASE_DIR = os.path.dirname(__file__)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'site-media/')
ADMIN_MEDIA_ROOT = os.path.join(BASE_DIR, 'site-media/admin/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = deploy.MEDIA_URL

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = deploy.ADMIN_MEDIA_PREFIX

# Make this unique, and don't share it with anybody.
# This should be defined in the local_settings.py file
SECRET_KEY = deploy.SECRET_KEY

# These should be the API key (http://disqus.com/api/get_my_key/) and website
# shortname from your DISQUS account.
DISQUS_API_KEY = deploy.DISQUS_API_KEY
DISQUS_WEBSITE_SHORTNAME = deploy.DISQUS_WEBSITE_SHORTNAME

# http://www.viglink.com used for affiliate link tracking
VIGLINK_KEY = deploy.VIGLINK_KEY
GOOGLE_ANALYTICS_CODE = deploy.GOOGLE_ANALYTICS_CODE

# http://addthis.com sharing widget.
ADDTHIS_USERNAME = deploy.ADDTHIS_USERNAME

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates/'),
)

# Overrides the default in order to remove I18N processor
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'mysite.context_processors.CurrentSite',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'activitysync',
    'blog',
    'disqus',
    'metaweblog',
    'tagging',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'south',
    'memcache_status',
)

# Activity sync settings
ACTIVITYSYNC_PROVIDERS = (
    #'activitysync.providers.googlereader.GoogleReaderProvider',
    'activitysync.providers.twitterprovider.TwitterUserProvider',
    'activitysync.providers.redditprovider.RedditProvider',
)

ACTIVITYSYNC_SETTINGS = deploy.ACTIVITYSYNC_SETTINGS


# Some special settings to aid development in debug mode
if DEBUG:
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + MIDDLEWARE_CLASSES
    
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    
    SEND_BROKEN_LINK_EMAILS = False

    # Match local network IPs to allow access from other machines
    from fnmatch import fnmatch
    class glob_list(list):
        def __contains__(self, key):
            for elt in self:
                if fnmatch(key, elt): return True
            return False

    INTERNAL_IPS = glob_list(['127.0.0.1', '192.168.*.*'])

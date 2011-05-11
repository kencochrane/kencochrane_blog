# Django settings for mysite project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ken Cochrane', 'KenCochrane@gmail.com'),
)

MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = False

# Site owner will be used throughout the site.
# This should represent the site author.
SITE_OWNER = "Ken Cochrane"
SITE_TITLE = "Ken Cochrane"

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = False

SITE_ID = 1

# Base directory (all other paths should be relative to this path, rather 
# than hard-coded)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'site-media/')
ADMIN_MEDIA_ROOT = os.path.join(BASE_DIR, 'site-media/admin/')

MEDIA_URL = "/static/"

STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
# This should be defined in the local_settings.py file
SECRET_KEY = "mySecretKeyIs120u9239234329i40932i4902nknkanfuiasnfaiurThis"

# These should be the API key (http://disqus.com/api/get_my_key/) and website
# shortname from your DISQUS account.
DISQUS_API_KEY = "DISQUS_API_KEY"
DISQUS_WEBSITE_SHORTNAME = "DISQUS_WEBSITE_SHORTNAME"

# http://www.viglink.com used for affiliate link tracking
VIGLINK_KEY = "VIGLINK_KEY"
GOOGLE_ANALYTICS_CODE = "GOOGLE_ANALYTICS_CODE"

# http://addthis.com sharing widget.
ADDTHIS_USERNAME = "ADDTHIS_USERNAME"

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

ACTIVITYSYNC_SETTINGS = None



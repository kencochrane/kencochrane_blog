from django.conf import settings
from django.contrib.sites.models import Site

def CurrentSite(request):
    google_analytics_code = getattr(settings, 'GOOGLE_ANALYTICS_CODE', None)
    site_title = getattr(settings, 'SITE_TITLE', None)
    ADDTHIS_USERNAME = getattr(settings, 'ADDTHIS_USERNAME', None)
    VIGLINK_KEY = getattr(settings, 'VIGLINK_KEY', None)

    return {
        'current_site': Site.objects.get_current(),
        'UA_code': google_analytics_code,
        'SITE_TITLE': site_title,
        'ADDTHIS_USERNAME':ADDTHIS_USERNAME,
        'VIGLINK_KEY':VIGLINK_KEY,
    }

from django.conf.urls.defaults import *
from mysite.metaweblog import views as mw_views


urlpatterns = patterns('',
    # XML-RPC entry point
    url(r'xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc', name='xml_rpc_url'),
    
    # Windows Live Writer manifest file
    url(r'^wlwmanifest.xml$', view=mw_views.wlw_manifest, name='wlw_manifest'),
    
    # Really Simple Discoverability (RSD) manifest file
    url(r'^rsd.xml$', view=mw_views.rsd_manifest, name='rsd_manifest'),
)

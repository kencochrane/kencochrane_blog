from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext

def wlw_manifest(request):
    return render_to_response('metaweblog/wlwmanifest.xml',
                context_instance=RequestContext(request),
                mimetype='application/xml')

def rsd_manifest(request):
    return render_to_response('metaweblog/rsd.xml',
                context_instance=RequestContext(request),
                mimetype='application/xml')

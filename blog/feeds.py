from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from mysite.blog.models import Entry
from tagging.models import Tag, TaggedItem
from django.contrib.sites.models import Site

#from mysite.deploy import SITE_TITLE
SITE_TITLE = "Ken Cochrane"

class LatestEntriesFeed(Feed):
    title = SITE_TITLE
    link = "/"
    
    def items(self):
        return Entry.objects.published()[:5]
    
    def description(self):
        return "Latest blog entries for %s" % Site.objects.get_current().domain
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.body_formatted
        
class LatestEntriesByTagFeed(Feed):
    def get_object(self, request, tag_name):
        return get_object_or_404(Tag, name=tag_name)
        
    def title(self, obj):
        return "%s| %s" % (SITE_TITLE,obj.name)
        
    def link(self, obj):
        return reverse('blog_tag_detail', args=[obj.name])
        
    def description(self, obj):
        return "Latest blog entries tagged with '%s'" % obj.name
        
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Entry.objects.published(), obj)[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.body_formatted

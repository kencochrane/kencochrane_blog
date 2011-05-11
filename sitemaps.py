from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from datetime import datetime

from mysite.blog.models import Entry
from tagging.models import Tag

class SectionSitemap(Sitemap):
    def items(self):
        return ['Home', 'Blog', 'Tags', 'Activity']
        
    def location(self, page):
        if page == 'Home': return reverse('main_index')
        if page == 'Blog': return reverse('blog_index')
        if page == 'Tags': return reverse('blog_tag_list')
        if page == 'Activity': return reverse('main_activity')

    def lastmod(self, page):
        return datetime.now()

    def changefreq(self, page):
        if page == 'Blog' or page == 'Blog-tags':
            return 'weekly'
        else:
            return 'daily'

    def priority(self, page):
        if page == 'Home' or page == 'Blog':
            return 1.0
        elif page == 'Activity':
            return 0.3
        else:
            return 0.5

            
class BlogArchiveSitemap(Sitemap):  
    priority = 0.4
    
    def items(self):
        return Entry.objects.dates('pub_date', 'month', order='DESC')

    def location(self, date):
        return reverse('blog_archive_month', args=[date.year, date.strftime("%m")])

    def lastmod(self, date):
        return datetime.now()

    def changefreq(self, date):
        if date.year == datetime.now().year and date.month == datetime.now().month:
            return 'weekly'
        else:
            return 'never'


class TagSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return Tag.objects.usage_for_queryset(Entry.objects.published())

    def location(self, tag):
        return reverse('blog_tag_detail', args=[tag.name])

from django.conf.urls.defaults import *
from mysite.blog.models import Entry
from mysite.blog import views as blog_views

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        view=blog_views.blog_entry_detail,
        name='blog_entry_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        view=blog_views.blog_archive_month,
        name='blog_archive_month'),

    url(r'^(?P<year>\d{4})/$',
        view=blog_views.blog_archive_year,
        name='blog_archive_year'),
        
    url(r'^tags/(?P<slug>[-\w]+)/$',
        view=blog_views.tag_detail,
        name='blog_tag_detail'),

    url (r'^tags/$',
        view=blog_views.tag_list,
        name='blog_tag_list'),

    #url (r'^search/$',
    #    view=blog_views.search,
    #    name='blog_search'),

    url(r'^page/(?P<page>\d+)/$',
        view=blog_views.blog_entry_list,
        kwargs={'explicit_page_request': True},
        name='blog_index_paged'),
    url(r'^$',
        view=blog_views.blog_entry_list,
        name='blog_index'),
)

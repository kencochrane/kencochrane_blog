from django.contrib.sites.models import Site
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from mysite.blog.models import Entry
from activitysync.models import Activity
from blog.views import blog_entry_detail
from mysite.blog.paginator import InfinitePaginator

@cache_page(60 * 15)
def index(request):
    # This logic is to support theme detection by Windows Live Writer.
    # It needs to see the actual post display, but it stupidly goes to the main
    # blog page rather than the entry's URL. So, if we detect WLW's user agent,
    # let's just make the main index show the latest blog post.
    try:
        if request.META['HTTP_USER_AGENT'].find("Windows Live Writer") > -1:
            post = Entry.objects.published().order_by('-pub_date')[0]
            return blog_entry_detail(request, post.slug, post.pub_date.year, post.pub_date.month)
    except (KeyError, IndexError):
        pass

    return render_to_response('index.html',
                {'blog_entries': Entry.objects.published_for_list()[:2],
                 'activities': Activity.objects.published()[:5] },
                context_instance=RequestContext(request))


def activity(request, page="1", explicit_page_request=False):
    # Make sure page parameter is an integer
    try:
        page = int(page)
    except:
        raise Http404

    # Make sure we only have one canonical first page
    if explicit_page_request and page == 1:
        return redirect('main_activity')

    # Previous URL used GET parameter 'page', so let's check
    # for that and redirect to new view if necessary
    if not explicit_page_request:
        try:
            requestNum = request.GET['page']
            if requestNum != None and requestNum.isdigit():
                return redirect('activity_paged', page=requestNum)
        except KeyError:
            pass

    activity_list = Activity.objects.published().defer("username", "author", "comments", "guid")
    paginator = InfinitePaginator(activity_list, 25)

    try:
        activities = paginator.page(page)
    except:
        raise Http404

    return render_to_response('activity.html',
                activities.create_template_context('activity_paged', 'main_activity'),
                context_instance=RequestContext(request))

def robots(request):
    return HttpResponse("User-agent: *\nDisallow:\nSitemap: http://%s/sitemap.xml" % 
                (Site.objects.get_current().domain), 
                status=200, 
                mimetype='text/plain')

from django.test import TestCase
from mysite.blog.templatetags import blog_extras

class MyTests(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)

    def test_blog(self):
        response = self.client.get('/blog/')
        self.failUnlessEqual(response.status_code, 200)
    
    def test_blog_paged(self):
        # Specifying page 1 outright should work
        response = self.client.get('/blog/?page=1')
        self.failUnlessEqual(response.status_code, 200)

        # Enough entries to reach page 2
        response = self.client.get('/blog/?page=2')
        self.failUnlessEqual(response.status_code, 200)

        # Page 3 does not exist
        response = self.client.get('/blog/?page=3')
        self.failUnlessEqual(response.status_code, 404)

    def test_blog_months(self):
        dates = blog_extras.render_month_links()['dates']
        for date in dates:
            response = self.client.get('/blog/%s/%s/' % (date.year, date.strftime('%m')))
            self.failUnlessEqual(response.status_code, 200)

        # Try a non-existant month
        response = self.client.get('/blog/2009/05/')
        self.failUnlessEqual(response.status_code, 404)

    def test_blog_years(self):
        dates = blog_extras.render_month_links()['dates']
        for date in dates:
            response = self.client.get('/blog/%s/' % date.year)
            self.failUnlessEqual(response.status_code, 200)

        # Try a non-existant year
        response = self.client.get('/blog/2000/')
        self.failUnlessEqual(response.status_code, 404)

    def test_blog_tags(self):
        tag_list = blog_extras.render_all_tag_links()['tag_list']

        for tag in tag_list:
            response = self.client.get('/blog/tags/%s/' % tag.name)
            self.failUnlessEqual(response.status_code, 200)

        # Try a non-existant tag
        response = self.client.get('/blog/tags/tagDoesNotExist/')
        self.failUnlessEqual(response.status_code, 404)

    def test_blog_404(self):
        response = self.client.get('/not/')
        self.failUnlessEqual(response.status_code, 404)
        response = self.client.get('/blog/not/')
        self.failUnlessEqual(response.status_code, 404)

    ######################
    # Tests for activities
    ######################
    def test_activity(self):
        response = self.client.get('/activity/')
        self.failUnlessEqual(response.status_code, 200)
        
    def test_activity_paged(self):
        # Specifying page 1 outright should work
        response = self.client.get('/activity/?page=1')
        self.failUnlessEqual(response.status_code, 200)

        # Enough entries to reach pages 2 and 3
        response = self.client.get('/activity/?page=2')
        self.failUnlessEqual(response.status_code, 200)
        response = self.client.get('/activity/?page=3')
        self.failUnlessEqual(response.status_code, 200)

        # Page 4 does not exist
        response = self.client.get('/activity/?page=4')
        self.failUnlessEqual(response.status_code, 404)

    ######################
    # Tests for RSS feeds
    ######################
    def test_feed(self):
        response = self.client.get('/feeds/latest/')
        self.failUnlessEqual(response.status_code, 200)

    def test_tags_feeds(self):
        tag_list = blog_extras.render_all_tag_links()['tag_list']

        for tag in tag_list:
            response = self.client.get('/feeds/tags/%s/' % tag.name)
            self.failUnlessEqual(response.status_code, 200)

        # Try a non-existant tag
        response = self.client.get('/feeds/tags/tagDoesNotExist/')
        self.failUnlessEqual(response.status_code, 404)

    ######################
    # Tests for Sitemap
    ######################
    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.failUnlessEqual(response.status_code, 200)

    ######################
    # Tests for Admin
    ######################
    def test_admin(self):
        response = self.client.get('/admin/')
        self.failUnlessEqual(response.status_code, 200)

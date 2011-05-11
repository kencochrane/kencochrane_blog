from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse

# Code borrowed from django-pagination.  I ripped it out since I didn't want the
# rest of the functionality it provided (auto-pagination).
class InfinitePaginator(Paginator):
    """
    Paginator designed for cases when it's not important to know how many total
    pages.  This is useful for any object_list that has no count() method or can
    be used to improve performance for MySQL by removing counts.

    The orphans parameter has been removed for simplicity and there's a link
    template string for creating the links to the next and previous pages.
    """

    def __init__(self, object_list, per_page, allow_empty_first_page=True):
        orphans = 0 # no orphans
        super(InfinitePaginator, self).__init__(object_list, per_page, orphans,
            allow_empty_first_page)
        # no count or num pages
        del self._num_pages, self._count

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        page_items = self.object_list[bottom:top]
        # check moved from validate_number
        if not page_items:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return InfinitePage(page_items, number, self)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        raise NotImplementedError
    count = property(_get_count)

    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        raise NotImplementedError
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        raise NotImplementedError
    page_range = property(_get_page_range)


class InfinitePage(Page):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator
        self.cached_has_next = None

    def __repr__(self):
        return '<Page %s>' % self.number

    def has_next(self):
        """
        Checks for one more item than last on this page.
        """
        if self.cached_has_next != None:
            return self.cached_has_next

        try:
            next_item = self.paginator.object_list[
                self.number * self.paginator.per_page]
        except IndexError:
            self.cached_has_next = False
            return False

        self.cached_has_next = True
        return True

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        return ((self.number - 1) * self.paginator.per_page +
            len(self.object_list))

    #Bonus methods for creating links

    def next_link(self, paged_view_name):
        if self.has_next():
            return reverse(paged_view_name, args=[self.number + 1])
        return None

    def previous_link(self, paged_view_name, first_page_view_name=None):
        if self.has_previous():
            if self.number == 2 and first_page_view_name:
                return reverse(first_page_view_name)
            else:
                return reverse(paged_view_name, args=[self.number - 1])
        return None

    def page_title(self):
        if self.number > 1:
            return 'Page %s' % self.number
        return None

    def create_template_context(self, paged_view_name, first_page_view_name=None):
        return {
            'object_list': self.object_list,
            'page_title': self.page_title(),
            'has_next': self.has_next(),
            'has_previous': self.has_previous(),
            'next': self.next_link(paged_view_name),
            'previous': self.previous_link(paged_view_name, first_page_view_name),
        }

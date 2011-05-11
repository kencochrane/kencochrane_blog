from django import template
from mysite.blog.models import Entry
from tagging.models import Tag

register = template.Library()

@register.inclusion_tag('blog/month_links_tag.html')
def render_month_links():
    return {
        'dates': Entry.objects.published().dates('pub_date', 'month', order='DESC'),
    }

@register.inclusion_tag('blog/tag_cloud_tag.html')
def render_tag_cloud():
    return {
        'tag_cloud': Tag.objects.cloud_for_model(Entry, steps=3, filters=dict(published=True)),
    }

@register.inclusion_tag('blog/tag_list_tag.html')
def render_all_tag_links():
    return {
        'tag_list': Tag.objects.usage_for_queryset(Entry.objects.published()),
    }

@register.inclusion_tag('blog/tag_list_tag.html')
def render_tag_links_for_object(entry):
    return {
        'tag_list': Tag.objects.get_for_object(entry),
    }
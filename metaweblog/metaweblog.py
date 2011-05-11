# metaweblog.py is a modified version of the implementation by
# Graham Binns for his Frabjous blog enginer
# Copyright (C) 2009    Graham Binns <graham@grahambinns.com>
# (Frabjous is distributed under the GNU General Public License)
from django.contrib.admin.models import ADDITION, LogEntry
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django_xmlrpc.decorators import xmlrpc_func
from blog.models import Entry
from tagging.models import Tag


class MetaWeblogError(Exception):
    """Raised whenever something goes wrong with a MetaWeblog doodad."""


def mw_authenticate(username, password):
    """Authenticate a metaweblog user.

    :param username: The user to auth.
    :param password: Their password.

    If authentication is successful a `User` instance will be returned.
    Otherwise a MetaWeblogError will be raised.
    """
    user = authenticate(username=username, password=password)
    
    if not user:
        raise MetaWeblogError("Authentication failed")
    if user.has_perm('change_entry'):
        return user
    else:
        raise MetaWeblogError("Permission denied")


@xmlrpc_func(
    name='metaWeblog.getPost', returns='struct',
    args=['int', 'string', 'string'])
def get_post(postid, username, password):
    """Retrieve a Post by ID and return it.

    :param postid: The ID of the Post to retrieve.
    :param username: The Django username being used for authentication
        and authorisation.
    :param password: The Django password to go with username.

    """
    # First, authenticate them
    user = mw_authenticate(username, password)

    # Try to load the post
    try:
        post = Entry.objects.get(pk=int(postid))
    except DoesNotExist, e:
        raise MetaWeblogError("The post you were looking for does not exist")

    # Turn the post into a metaweblog struct
    return post.as_metaweblog_struct()


@xmlrpc_func(
    name='metaWeblog.getRecentPosts', returns='list',
    args=['int', 'string', 'string', 'int'])
def get_recent_posts(blogid, username, password, number_of_posts=5):
    """Return the latest posts for a given blog.

    :param blogid: The ID of the blog to retrieve from. Currently
        ignored as we don't have multiple blogs (yet).
    :param username: The username to authenticate against.
    :param password: The password for username.
    :param number_of_posts: The number of posts to return.
    """
    # Authenticate. This will raise an error on failure that we don't
    # handle.
    user = mw_authenticate(username, password)

    posts = Entry.objects.order_by('-pub_date')[:number_of_posts]
    return [post.as_metaweblog_struct() for post in posts]


@xmlrpc_func(
    name='metaWeblog.getUsersBlogs', returns='list',
    args=['string', 'string', 'string'])
def get_users_blogs(appkey, username, password):
    """Return all blogs accessible to a user.

    :param appkey: Not used.
    :param username: The username to authenticate against.
    :param password: The password for username.
    """
    user = mw_authenticate(username, password)

    return [{
        'isAdmin': user.is_superuser,
        'url': 'http://%s/' % Site.objects.get_current().domain,
        'blogid': 1,
        'blogName': '%s' % Site.objects.get_current().name }]

@xmlrpc_func(
    name='blogger.getUsersBlogs', returns='list',
    args=['string', 'string', 'string'])
def blogger_get_users_blogs(appkey, username, password):
    """Return all blogs accessible to a user.

    :param appkey: Not used.
    :param username: The username to authenticate against.
    :param password: The password for username.
    """
    user = mw_authenticate(username, password)

    return [{
        'isAdmin': user.is_superuser,
        'url': 'http://%s/' % Site.objects.get_current().domain,
        'blogid': 1,
        'blogName': '%s' % Site.objects.get_current().name }]

@xmlrpc_func(
    name='metaWeblog.newPost', returns='int',
    args=['int', 'string', 'string', 'struct', 'boolean'])
def new_post(blogid, username, password, struct, publish):
    """Add a new Post to a Blog.

    :param blogid: The ID of the blog to which the post will be added
        (ignored at present).
    :param username: The username to use for authentication.
    :param password: The password to go with username.
    :param struct: A metaweblog API struct containing the new Post data.
    :param publish: A value indicating whether or not the post should be
        published.
    """
    user = mw_authenticate(username, password)

    # We ignore blogid, but if we didn't we'd use it here.
    if not user.has_perm('add_entry'):
        raise MetaWeblogError("Sorry, you don't have permission to add a Post")

    # We let Entry do the work
    try:
        post = Entry.objects.create_from_metaweblog_struct(struct, user)
    except Exception, e:
        raise MetaWeblogError("Unable to create new post: %s" % str(e))

    # Mark the post as published if that's what's required
    if publish:
        post.published = True
        post.save()

    # Add a log entry for this action.
    #!!!!content_type = ContentType.objects.get(name='post')
    #LogEntry.objects.log_action(
    #    user_id=user.id, content_type_id=content_type.id, object_id=post.id,
    #    object_repr=post.subject, action_flag=ADDITION)

    return post.id


@xmlrpc_func(
    name='metaWeblog.getCategories', returns='list',
    args=['int', 'string', 'string'])
def get_categories(blogid, username, password):
    """Return the categories for a given blog.

    :param blogid: Ignored.
    :param username: The username for authentication.
    :param password: The password for same.
    """
    user = mw_authenticate(username, password)

    # For now we just return a list of the categories available.
    tag_list = []
    domain = Site.objects.get_current().domain
    for tag in Tag.objects.usage_for_queryset(Entry.objects.all()):
        tag_dict = {
            'description': tag.name,
            'htmlUrl': 'http://%s%s' % (
                domain, reverse('blog_tag_detail', args=[tag.name])),
            'rssUrl': 'http://%s%s' % (
                domain, reverse('blog_tagged_rss', args=[tag.name])) }
        tag_list.append(tag_dict)
    return tag_list


@xmlrpc_func(
    name='metaWeblog.editPost', returns='struct',
    args=['int', 'string', 'string', 'struct', 'boolean'])
def edit_post(postid, username, password, struct, publish):
    """Update an extant post with new data from a metaWeblog struct.

    :param postid: The id of the post to update.
    :param username: The username to use to update the post.
    :param password: The password for `username`.
    :param publish: Whether or not the post should be marked as
        published.
    """
    user = mw_authenticate(username, password)

    # If we can load the Post, we can update it with the new data
    try:
        post = Entry.objects.get(pk=int(postid))
        post.populate_from_metaweblog_struct(struct, user)
        
        post.published = publish
        post.save()
            
        return True
    except Exception, e:
        raise MetaWeblogError("Unable to edit post: %s", str(e))

        
@xmlrpc_func(
    name='blogger.deletePost', returns='boolean',
    args=['string', 'int', 'string', 'string', 'boolean'])
def blogger_delete_post(appkey, postid, username, password, publish):
    """Delete an existing post.
    
    :param appkey: Currently ignored.
    :param postid: The id of the post to update.
    :param username: The username to use to update the post.
    :param password: The password for `username`.
    :param publish: Ignored, as this does not matter for deleting.
    """
    user = mw_authenticate(username, password)
    
    if not user.has_perm('delete_entry'):
        raise MetaWeblogError("Sorry, you don't have permission to delete a Post")
        
    # If we can load the Post, we can delete it
    try:
        post = Entry.objects.get(pk=int(postid))
        post.delete()
        return True
    except Exception, e:
        raise MetaWeblogError("Unable to delete post: %s", str(e))

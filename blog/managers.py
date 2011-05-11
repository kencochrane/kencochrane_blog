from django.db.models import Manager
import datetime

class PublishedManager(Manager):
    """Returns published posts that are not in the future."""
   
    def published(self):
        return self.get_query_set().filter(published=True, pub_date__lte=datetime.datetime.now())

    def published_for_list(self):
        return self.published().defer("tags", "body")
        
    def create_from_metaweblog_struct(self, struct, user):
        """Create a Post object from a metaweblog struct and return it.

        :param struct: The metaweblog struct to use to create the Post.
        :param user: The User that is creating the post.
        """
        post = self.model()
        post.populate_from_metaweblog_struct(struct, user)
        return post

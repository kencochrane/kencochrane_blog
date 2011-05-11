# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    depends_on = (
        ("activitysync", "0001_initial"),
    )
    needed_by = (
        ("activitysync", "0002_auto__add_provider__add_field_activity_provider"),
        ("activitysync", "0003_convert_to_provider_objects"),
    )

    def forwards(self, orm):
        try:
            db.delete_table('activitysync_activity')
        except:
            print "activitysync_activity does not exist, so don't have to delete"

        db.rename_table('blog_activities', 'activitysync_activity')
        db.create_table('blog_activities', (('test', models.CharField(max_length=50)),))

    def backwards(self, orm):
        try:
            db.delete_table('blog_activities')
        except:
            print "blog_activities does not exist, so don't have to delete"

        db.rename_table('activitysync_activity', 'blog_activities')
        db.create_table('activitysync_activity', (('test', models.CharField(max_length=50)),))

    models = {
        'activitysync.activity': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Activity', 'db_table': "'blog_activities'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'blog.activity': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Activity', 'db_table': "'blog_activities'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'blog.entry': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Entry', 'db_table': "'blog_entries'"},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'snip': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['activitysync', 'blog']

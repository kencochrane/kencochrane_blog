# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('blog_entries', (
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('snip', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('mod_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('blog', ['Entry'])

        # Adding model 'Activity'
        db.create_table('blog_activities', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('blog', ['Activity'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('blog_entries')

        # Deleting model 'Activity'
        db.delete_table('blog_activities')
    
    
    models = {
        'blog.activity': {
            'Meta': {'object_name': 'Activity', 'db_table': "'blog_activities'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'blog.entry': {
            'Meta': {'object_name': 'Entry', 'db_table': "'blog_entries'"},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mod_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'snip': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['blog']

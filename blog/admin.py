# Blog application admin page
from mysite.blog.models import Entry
from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea

#===============================================================================
class EntryForm(forms.ModelForm):
    snip = forms.CharField(widget=Textarea)
    
    class Meta:
        model = Entry

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'published', 'mod_date')
    list_filter = ['pub_date', 'published']
    search_fields = ['title', 'body']
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ('title',)}
    form = EntryForm

admin.site.register(Entry, EntryAdmin)
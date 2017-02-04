from django.contrib import admin
from .models import Contact, ContactBook

class ContactAdmin(admin.ModelAdmin):
    search_fields=['first_name', 'last_name', 'number']

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactBook)
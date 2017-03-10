from django.contrib import admin
from .models import Contact, ContactBook, Group, UserProfile

class ContactAdmin(admin.ModelAdmin):
    search_fields=['first_name', 'last_name', 'number']

admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactBook)
admin.site.register(Group)
admin.site.register(UserProfile)
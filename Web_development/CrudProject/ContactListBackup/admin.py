from django.contrib import admin
from .models import ContactListBackup


class ContactListBackupAdmin(admin.ModelAdmin):
    list_display = ('SL', 'Name', 'Number')


admin.site.register(ContactListBackup,ContactListBackupAdmin)
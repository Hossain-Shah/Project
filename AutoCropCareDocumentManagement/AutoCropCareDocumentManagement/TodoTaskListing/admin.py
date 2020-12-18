from django.contrib import admin
from . import models


class DocumentListingAdmin(admin.ModelAdmin):
    list_display = ("file_number",  "name_of_product", "expires_on")


class FileNumberAdmin(admin.ModelAdmin):
    list_display = ("number",)


admin.site.register(models.DocumentListing, DocumentListingAdmin)
admin.site.register(models.FileNumber, FileNumberAdmin)

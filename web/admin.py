from django.contrib import admin
from web.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "title", "slug", "modified_at")
    search_fields = ("title", "slug")


admin.site.register(Page, PageAdmin)

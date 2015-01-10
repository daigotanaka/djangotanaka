from django.contrib import admin
from core.models import Command, Log, Page


class CommandAdmin(admin.ModelAdmin):
    list_display = ("created_at", "created_by", "name", "data", "raw_command")
    search_fields = ("name", "data", "raw_command")


class LogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "created_by", "raw_data")
    search_fields = ("raw_command",)


class PageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "created_by", "status", "title", "slug",
                    "modified_at")
    search_fields = ("title", "slug")


admin.site.register(Command, CommandAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Page, PageAdmin)

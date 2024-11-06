from django.contrib import admin
from django.contrib.admin.models import LogEntry

from api.models import WebServiceLog


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'change_message', 'action_flag')
    list_filter = ('action_time', 'content_type', 'action_flag')
    search_fields = ('user__username',)
    ordering = ('-action_time',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WebServiceLog)
class WebServiceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'url', 'status_code', 'status_msg', 'created_on')
    list_filter = ('created_on', 'status_code', 'method')
    search_fields = ('url',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

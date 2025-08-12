from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','short_message','is_read','created_at')
    list_filter = ('is_read','created_at')
    search_fields = ('user__username','message')
    readonly_fields = ('created_at',)

    def short_message(self, obj):
        return obj.message[:60]
    short_message.short_description = 'Message'

admin.site.register(Notification, NotificationAdmin)

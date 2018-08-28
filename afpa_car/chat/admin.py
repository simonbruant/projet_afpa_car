from django.contrib import admin

from .models import Thread, ChatMessage

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    model = Thread
    inlines = [ChatMessage]

    list_display = ('first', 'second', 'updated', 'timestamp')
    readonly_fields = ('updated', 'timestamp')
    fieldsets = (
        (None, {'fields': ('first', 'second', 'updated', 'timestamp')}),
    )

admin.site.register(Thread, ThreadAdmin)

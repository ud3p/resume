from django.contrib import admin

from .models import Request

class RequestAdmin(admin.ModelAdmin):
	list_display = ['date', 'method', 'path', 'priority', 'ip_addr']

admin.site.register(Request, RequestAdmin)

from django.contrib import admin

from apps.hello.models import MyContacts, SignalProcessor

class MyContactsAdmin(admin.ModelAdmin):
	list_display = ['name', 'surname', 'email', 'skype']

class SignalProcessorAdmin(admin.ModelAdmin):
	list_display = ['model_name', 'model_entry', 'date']

admin.site.register(MyContacts, MyContactsAdmin)
admin.site.register(SignalProcessor, SignalProcessorAdmin)

from django.conf.urls import url
from .views import requests, AjaxRequests


urlpatterns = [
    url(r'^$', requests, name='requests'),
    url(r'^ajaxrequests/$', AjaxRequests.as_view(), name='ajaxrequests'),

]

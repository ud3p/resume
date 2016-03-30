from django.conf.urls import patterns, url
from apps.hello import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^edit/(?P<pk>\d+)/$', views.EditInfo.as_view(), name='edit'),
)

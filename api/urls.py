from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^register/', 'api.views.register'),
    url(r'^add_event/', 'api.views.add_event'),
    url(r'^get_event_list/', 'api.views.get_event_list'),
    url(r'^add_guest/', 'api.views.add_guest')
]

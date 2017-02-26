from django.conf.urls import url
# from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^refresh/$', views.refresh),
    url(r'^resolve/$', views.resolve_incident),
    url(r'^show/(?P<id>\d+)/$', views.show)
]

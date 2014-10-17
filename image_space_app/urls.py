from django.conf import settings
from django.conf.urls import patterns, url

from image_space_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    

)

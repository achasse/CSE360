from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'image_space.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('image_space_app.urls')),
    url(r'^admin/', include(admin.site.urls)),           
    url(r'^signup/$', 'image_space_app.views.sign_up'),
    url(r'^login/$', 'image_space_app.views.login_user'),


)

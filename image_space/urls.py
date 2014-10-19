from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'image_space.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #'django.views.static',
    #(r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
     

    
    url(r'^$', include('image_space_app.urls')),
    url(r'^home/$', include('image_space_app.urls')),
    url(r'^admin/', include(admin.site.urls)),           
    url(r'^signup/$', 'image_space_app.views.sign_up'),
    url(r'^login/$', 'image_space_app.views.login_user', name = 'login'),
    url(r'^register/$', 'image_space_app.views.register', name = 'register'),
    url(r'^profile/$', 'image_space_app.views.profile', name = 'profile'),
    url(r'^logout/$', 'image_space_app.views.log_out', name = 'logout'),

)
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )

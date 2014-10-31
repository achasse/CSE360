from django.conf import settings
from django.conf.urls import patterns, url, include

from image_space_app import views
from image_space_app.views import RootView, LoginUserView, RegisterView
from image_space_app.views import PicturesList, PictureDetails, PictureEdit
from image_space_app.views import PictureUpload, ProfileDetails, ProfilePictureChange

urlpatterns = patterns('',
    url(r'^$', RootView.as_view(), name='home'),

    url(r'^login/$', LoginUserView.as_view() , name = 'login'),
    url(r'^logout/$', views.log_out , name = 'logout'),

    url(r'^register/$', RegisterView.as_view(), name = 'register'),
    
    url(r'^profile/$', ProfileDetails.as_view() , name = 'profile'),
    url(r'^profile/picture/(?P<pk>[0-9]+)/$', ProfilePictureChange.as_view(), name = 'change_picture' ),
    url(r'^pictures/$', PicturesList.as_view(), name = 'pictures'),
    url(r'^pictures/upload$', PictureUpload.as_view(), name = 'picture_upload'),
    url(r'^pictures/(?P<pk>[0-9]+)/', include([
      url(r'^$', PictureDetails.as_view(), name =  'picture_details'),
      url(r'^edit/$', PictureEdit.as_view(), name = 'picture_edit' ),
      ])),
)
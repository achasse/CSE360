from django.contrib import admin
from image_space_app.models import UserProfile, UserPicture

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserPicture)
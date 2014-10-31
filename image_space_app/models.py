from django.db import models
from django.contrib.auth.models import User

class UserPicture(models.Model):
    user = models.ForeignKey(User)
    picture = models.ImageField(upload_to='user_images', blank = False)
    title = models.CharField(max_length=20)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.OneToOneField(UserPicture)

    def __unicode__(self):
        return self.user.username


from image_space_app.models import UserProfile, UserPicture
from django.contrib.auth.models import User
from django import forms
from django.core.files.images import get_image_dimensions

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password' )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()

class UserPictureForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ('picture', 'title' )

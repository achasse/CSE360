import datetime

from django.utils import timezone
from django.test import TestCase
from image_space_app.views import *
from django.core.urlresolvers import resolve



class ImageSpaceTests(TestCase):

    def test_will_just_be_success(self):
        """
        Dummy test
        """
        self.assertEqual(False, False)

    #Test ability for an existing user to log in (user is created then authenticated)
    def test_login(self):
        self.user = User.objects.create(username = 'user1', password = 'password', is_active = True, is_superuser = False)
        self.user = authenticate(username = 'user1', password = 'password')
        login = self.c.login(username = 'user1', password = 'password')
        self.assertTrue(login)

    #Test that '/' goes to RootView view
    def test_root(self):
        res = resolve('/')
        self.assertEqual(res.func, RootView)

    #Test that '/login' goes to LoginUserView view
    def test_login_view(self):
        res = resolve('/login/')
        self.assertEqual(res.func, LoginUserView)

    #Test that '/register/' goes to RegisterView view
    def test_register_view(self):
        res = resolve('/register/')
        self.assertEqual(res.func, RegisterView)

    #Test that '/profile/' goes to ProfileDetails view
    def test_profiledetails_view(self):
        res = resolve('/profile/')
        self.assertEqual(res.func, ProfileDetails)
            

    #Test logout (first with an active user logged in)
    def test_logout_currently_logged_in(self):
        self.user = User.objects.create(username = 'user2', password = 'password', is_active = True, is_superuser = False)
        self.user = authenticate(username = 'user2', password = 'password')
        login = self.c.login(username = 'user2', password = 'password')
        logout()
        self.assertTrue(logout)

    #Test logout request when no user logged in
    def test_logout_no_active_user(self):
        logout()

    

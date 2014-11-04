import datetime

from django.utils import timezone
from django.test import TestCase




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

    #def test_register(self):
        #self.user

from django.test import TestCase
from petapp import views
# Create your tests here.

class DemoTest(TestCase):
    def test_demofn(self):
        resp=views.demofn() == 'Welcome'
        self.assertEqual(first="welcome",second="Welcome",msg="error")
    
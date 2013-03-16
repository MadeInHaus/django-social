from .facebook_updater import FacebookUpdater
from django.test import TestCase


class SocialTest(TestCase):
    def test_facebook_update(self):
        fb = FacebookUpdater()
        fb.update()
        #self.assertEqual(1 + 1, 2)
    
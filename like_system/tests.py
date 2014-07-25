from django.test import TestCase


class BasicTests(TestCase):

    def setUp(self):
        pass

    def create_a_like_on_a_site(self):
        print "create_a_like_on_a_site"
        self.assertEqual(1, 1)
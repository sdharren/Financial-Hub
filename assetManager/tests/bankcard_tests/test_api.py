from assetManager.views import get_transactions
from django.test import TestCase

class TestApi(TestCase):
    def setUp(self):
        pass

    def test_get_transactions(self):
        self.assertEquals(get_transactions(),10)

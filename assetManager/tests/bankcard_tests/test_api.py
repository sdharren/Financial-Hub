from assetManager.views import get_transactions,get_accounts
from django.test import TestCase

class TestApi(TestCase):
    def setUp(self):
        pass

    def test_get_transactions(self):
        #self.assertEquals(get_transactions(),15)
        self.assertEquals(get_accounts(),10)

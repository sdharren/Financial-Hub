from assetManager.views import get_accounts,get_transactions
from django.test import TestCase

class TestApi(TestCase):
    def setUp(self):
        pass

    # def test_get_transactions(self):
    #     self.assertNotEquals(get_transactions(),None)

    def test_get_accounts(self):
        self.assertNotEquals(get_accounts(),None)

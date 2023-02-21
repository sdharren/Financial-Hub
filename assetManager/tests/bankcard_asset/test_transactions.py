from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.assets.debit_card import DebitCard
from django.test import TestCase
from assetManager.models import User

class DebitCardSandBoxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json'],['assetManager/tests/fixtures/account_types.json']
    def setUp(self):
        self.plaid_wrapper = DevelopmentWrapper()
        self.user = User.objects.get(email='favero@gmail.com')
        self.debit_card = DebitCard(self.plaid_wrapper, self.user)

    def test_get_transactions(self):
        #self.debit_card.get_institution('ins_12')# query insitutions
        pass

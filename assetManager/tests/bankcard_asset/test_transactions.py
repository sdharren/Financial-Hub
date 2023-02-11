from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.bankcards.debit_card import DebitCard
from django.test import TestCase

class DebitCardSandBoxWrapperTestCase(TestCase):
    def setUp(self):
        self.plaid_wrapper = SandboxWrapper()
        self.debit_card = DebitCard(self.plaid_wrapper)


    def test_get_transactions(self):
        #self.debit_card.get_transactions()
        #self.debit_card.print_class()
        pass

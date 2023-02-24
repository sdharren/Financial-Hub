from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper
from assetManager.assets.debit_card import DebitCard
from django.test import TestCase
from assetManager.models import User
from datetime import date

class DebitCardSandBoxWrapperTestCase(TestCase):
    fixtures = ['assetManager/tests/fixtures/users.json']
    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.plaid_wrapper = SandboxWrapper()

        public_token = self.plaid_wrapper.create_public_token_custom_user()
        self.plaid_wrapper.exchange_public_token(public_token)
        self.plaid_wrapper.save_access_token(self.user, ['transactions'])
        self.debit_card = DebitCard(self.plaid_wrapper, self.user)


    def test_get_transactions(self):
        #start_date = date.fromisoformat('2022-09-01') #change dates to within two years
        #end_date = date.fromisoformat('2022-09-03')
        #self.debit_card.get_transactions(start_date,end_date)

        self.debit_card.get_institution_name_from_db()
        #self.debit_card.get_account_balances()

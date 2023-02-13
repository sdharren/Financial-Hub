from django.test import TestCase
from assetManager.API_wrappers.sandbox_wrapper import SandboxWrapper
from assetManager.models import User

class StocksTestCase(TestCase):
    fixtures = [
        'assetManager/tests/fixtures/users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.wrapper = SandboxWrapper()
        # creating a sandbox public token for vanguard
        public_token = self.wrapper.create_public_token(bank_id='ins_115616', products_chosen=['investments']) 
        self.wrapper.exchange_public_token(public_token)
        self.wrapper.save_access_token(self.user)
        self.access_token = self.wrapper.get_access_token()

    def test_ads(self):
        self.assertEqual("", "")

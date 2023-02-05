import re
from django.test import TestCase
from assetManager.API_wrappers.development_wrapper import DevelopmentWrapper, PublicTokenNotExchanged, LinkTokenNotCreated

class DevelopmentWrapperTestCase(TestCase):
    def setUp(self):
        self.wrapper = DevelopmentWrapper()

    def test_wrapper_creates_link_token(self):
        self.wrapper.create_link_token()
        regex_match = re.match(r"^link-development-[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$", self.wrapper.get_link_token())
        self.assertIsNotNone(regex_match)

    def test_cannot_get_undefined_access_token(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_access_token()

    def test_cannot_get_undefined_item_id(self):
        with self.assertRaises(PublicTokenNotExchanged):
            self.wrapper.get_item_id()

    def test_cannot_get_undefined_link_token(self):
        with self.assertRaises(LinkTokenNotCreated):
            self.wrapper.get_link_token()
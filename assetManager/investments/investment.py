# Represents a single investment
class Investment():
    def __init__(self, holding, security):
        self.name = security['name']
        self.ticker = security['ticker_symbol']
        self.category = security['type']
        self.quantity = holding['quantity']
        self.total_price = holding['institution_value']
        self.security_id = holding['security_id']
        self.returns = {}

    def get_returns(self):
        return self.returns

    def get_name(self):
        return self.name

    def get_ticker(self):
        return self.ticker

    def get_quantity(self):
        return self.quantity

    def get_total_price(self):
        return self.total_price

    def get_category(self):
        return self.category
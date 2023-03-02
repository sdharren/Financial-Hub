class Investment():
    def __init__(self, holding, security):
        self.name = security['name']
        self.ticker = security['ticker_symbol']
        self.category = security['type']
        self.quantity = holding['quantity']
        self.total_price = holding['institution_value']
        self.security_id = holding['security_id']

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
    
    def serialize(self):
        serialized_data = {}
        serialized_data['name'] = self.name
        serialized_data['ticker_symbol'] = self.ticker
        serialized_data['type'] = self.category
        serialized_data['quantity'] = self.quantity
        serialized_data['total_price'] = self.total_price
        serialized_data['security_id'] = self.security_id
        return serialized_data
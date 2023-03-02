class Transaction:
    def __init__(self, transaction_json, ticker):
        self.type = transaction_json['type']
        self.quantity = transaction_json['quantity']
        self.price = transaction_json['price']
        self.amount = transaction_json['amount']
        self.security_id = transaction_json['security_id']
        self.ticker = ticker

    def serialize(self):
        serialized_data = {}
        serialized_data['type'] = self.type
        serialized_data['quantity'] = self.quantity
        serialized_data['price'] = self.price
        serialized_data['amount'] = self.amount
        serialized_data['security_id'] = self.security_id
        serialized_data['ticker_symbol'] = self.ticker
        return serialized_data
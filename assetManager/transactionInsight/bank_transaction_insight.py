class CategoriseTransactions():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history

    def getTransactionHistory(self):
        return self.transaction_history

    def getTotalSpending(self):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0:
                amount = amount + item['amount']
        return amount

    def getMonthlySpending(self,month):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month:
                amount = amount + item['amount']
        return amount

    def getSpendingForCompany(self,company):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['name'] == company:
                amount = amount + item['amount']
        return amount

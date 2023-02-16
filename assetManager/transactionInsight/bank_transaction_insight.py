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

    def getWeeklySpending(self,week,month):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day <= week*7 and item['date'].month == month:
                amount = amount + item['amount']
        return amount

    def getSpendingForCompany(self,company):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['name'] == company:
                amount = amount + item['amount']
        return amount

    def getCategorisedSpending(self):
        spenditurePerCategory = {}
        for item in self.transaction_history:
            if item['amount'] > 0:
                currentValue = spenditurePerCategory.get(item['category'][0]) or 0
                spenditurePerCategory[item['category'][0]] = currentValue + item['amount']
        return spenditurePerCategory

    def getMonthlyTransactions(self,month):
        monthlyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month:
                monthlyTransactions.append(item)
        return monthlyTransactions

    def getWeeklyTransactions(self,week,month):
        weeklyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day <= week*7 and item['date'].month == month:
                weeklyTransactions.append(item)
        return weeklyTransactions

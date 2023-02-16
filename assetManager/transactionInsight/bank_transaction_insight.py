"""
Class of methods to categories, filter and sort bank transactions.
author: Pavan Rana
"""
class CategoriseTransactions():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history

    def getTransactionHistory(self):
        return self.transaction_history

    #TODO add merge sort algorithm to order category spending

    # return that total spending for all transactions
    def getTotalSpending(self):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0:
                amount = amount + item['amount']
        return amount

    # return that total spending for a month, month variable is an integer
    def getMonthlySpending(self,month):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month:
                amount = amount + item['amount']
        return amount

    # return that total spending for a week, week & month variables are an integer
    def getWeeklySpending(self,week,month):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day <= week*7 and item['date'].month == month:
                amount = amount + item['amount']
        return amount

    # return total spending for the company name passed in
    def getSpendingForCompany(self,company):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['name'] == company:
                amount = amount + item['amount']
        return amount

    # return an array of categories of where money was spent as well as total spent
    def getCategorisedSpending(self):
        spenditurePerCategory = {}
        for item in self.transaction_history:
            if item['amount'] > 0:
                currentValue = spenditurePerCategory.get(item['category'][0]) or 0
                spenditurePerCategory[item['category'][0]] = currentValue + item['amount']
        return spenditurePerCategory

    # return an json of transactions within a month, month variable is an integer
    def getMonthlyTransactions(self,month):
        monthlyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month:
                monthlyTransactions.append(item)
        return monthlyTransactions

    # return an json of transactions within a week, week & month variables are an integer
    def getWeeklyTransactions(self,week,month):
        weeklyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day <= week*7 and item['date'].month == month:
                weeklyTransactions.append(item)
        return weeklyTransactions

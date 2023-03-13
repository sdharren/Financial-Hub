"""
Class of methods to categories, filter and sort bank transactions.
author: Pavan Rana
"""
class CategoriseTransactions():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history

    def getTransactionHistory(self):
        return self.transaction_history

    # returns an ordered array of tuples of categories and their spenditure
    def getOrderCategories(self,transactionHistory):
        categories = self.getCategorisedSpending(transactionHistory)
        orderedListOfCategories = sorted(categories)
        orderedDictionaryOfCategories = []
        for item in orderedListOfCategories:
            category = (item,categories.get(item))
            orderedDictionaryOfCategories.append(category)
        return orderedDictionaryOfCategories

    # return that total spending for all transactions
    def getTotalSpending(self):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0:
                amount = amount + item['amount']
        return amount

    def getRangeOfYears(self):
        rangeOfYears = []
        for item in self.transaction_history:
            if len(rangeOfYears) == 0:
                rangeOfYears.append(item['date'].year)
                rangeOfYears.append(item['date'].year)
            elif item['date'].year < rangeOfYears[0]:
                rangeOfYears[0] = item['date'].year
            elif item['date'].year > rangeOfYears[1]:
                rangeOfYears[1] = item['date'].year
        return rangeOfYears

    # return that total spending for a month, month variable is an integer
    def getYearlySpending(self,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].year == year:
                amount = amount + item['amount']
        return amount

    # return that total spending for a month, month variable is an integer
    def getMonthlySpending(self,month,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month and item['date'].year == year:
                amount = amount + item['amount']
        return amount

    # return that total spending for a week, week & month variables are an integer
    def getWeeklySpending(self,week,month,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day//7 == week and item['date'].month == month and item['date'].year == year:
                amount = amount + item['amount']
        return amount

    # return total spending for the company name passed in
    def getSpendingForCompany(self,company):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['name'] == company:
                amount = amount + item['amount']
        return amount

    # return an dictionary of categories of where money was spent as well as total spent
    def getCategorisedSpending(self,transactionHistory):
        spenditurePerCategory = {}
        for item in transactionHistory:
            if item['amount'] > 0:
                currentValue = spenditurePerCategory.get(item['category'][0]) or 0
                spenditurePerCategory[item['category'][0]] = currentValue + item['amount']
        return spenditurePerCategory

    # return an json of transactions within a year, month variable is an integer
    def getYearlyTransactions(self,year):
        yearlyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].year == year:
                yearlyTransactions.append(item)
        return yearlyTransactions

    # return an json of transactions within a month, month variable is an integer
    def getMonthlyTransactions(self,month,year):
        monthlyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].month == month and item['date'].year == year:
                monthlyTransactions.append(item)
        return monthlyTransactions

    # return an json of transactions within a week, week & month variables are an integer
    def getWeeklyTransactions(self,week,month,year):
        weeklyTransactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'].day <= week*7 and item['date'].month == month and item['date'].year == year:
                weeklyTransactions.append(item)
        return weeklyTransactions

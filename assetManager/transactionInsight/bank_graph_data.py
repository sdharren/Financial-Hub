"""
Class of methods to produce data to pass to the frontend to create the graphs
for bank data.
author: Pavan Rana
"""
from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions

class BankGraphData():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history
        self.transactionInsight = CategoriseTransactions(self.transaction_history)

    def monthlySpendingInYear(self,year):
        monthlySpending = []
        for i in range(1,13):
            monthlySpending.append(self.transactionInsight.getMonthlySpending(i,year))
        return monthlySpending

    def weeklySpendingInYear(self,month,year):
        weeklySpending = []
        for i in range(1,6):
            weeklySpending.append(self.transactionInsight.getWeeklySpending(i,month,year))
        return weeklySpending

    def orderedCategorisedMonthlySpending(self,month,year):
        monthlyTransactions = self.transactionInsight.getMonthlyTransactions(month,year)
        return self.transactionInsight.getOrderCategories(monthlyTransactions)

    def orderedCategorisedWeeklySpending(self,week,month,year):
        weeklyTransactions = self.transactionInsight.getWeeklyTransactions(week,month,year)
        return self.transactionInsight.getOrderCategories(weeklyTransactions)

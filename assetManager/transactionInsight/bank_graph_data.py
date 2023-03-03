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
        months = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        for i in range(1,13):
            monthlySpending.append({'name':months[i],'value': self.transactionInsight.getMonthlySpending(i,year)})
        return monthlySpending

    def weeklySpendingInYear(self,month,year):
        weeklySpending = []
        for i in range(1,6):
            weeklySpending.append({'name': "Week " + str(i),'value': self.transactionInsight.getWeeklySpending(i,month,year)})
        return weeklySpending

    def orderedCategorisedMonthlySpending(self,month,year):
        monthlyTransactions = self.transactionInsight.getMonthlyTransactions(month,year)
        return self.transactionInsight.getOrderCategories(monthlyTransactions)

    def orderedCategorisedWeeklySpending(self,week,month,year):
        weeklyTransactions = self.transactionInsight.getWeeklyTransactions(week,month,year)
        return self.transactionInsight.getOrderCategories(weeklyTransactions)

    def getMonth(self,monthName):
        month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
        }   
        return month_dict[monthName]

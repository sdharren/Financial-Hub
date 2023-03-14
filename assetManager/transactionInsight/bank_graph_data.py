"""
Class of methods to produce data to pass to the frontend to create the graphs
for bank data.
author: Pavan Rana
"""
from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions

def format_transactions(transactions):
    reformatted_transactions = []
    for account in transactions:
        try:
            case = {'date':[account['date'].year,account['date'].month,account['date'].day], 'amount':account['amount'], 'category': account['category'], 'name':account['name']}
            reformatted_transactions.append(case)
        except:
            return transactions

    return reformatted_transactions

class BankGraphData():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history
        self.transactionInsight = CategoriseTransactions(format_transactions(transaction_history))

    def yearlySpending(self):
        yearlySpending = []
        rangeOfYears = self.transactionInsight.getRangeOfYears()
        if len(rangeOfYears) != 0:
            for year in range(rangeOfYears[0],rangeOfYears[1]+1):
                yearlySpending.append({'name':str(year),'value': self.transactionInsight.getYearlySpending(year)})
        return yearlySpending

    def monthlySpendingInYear(self,year):
        monthlySpending = []
        months = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        for i in range(1,13):
            monthlySpending.append({'name':months[i]+" "+str(year),'value': self.transactionInsight.getMonthlySpending(i,year)})
        return monthlySpending

    def weeklySpendingInYear(self,date):
        weeklySpending = []
        month, year = date.split()
        year = int(year)
        for i in range(1,6):
            weeklySpending.append({'name': "Week " + str(i),'value': self.transactionInsight.getWeeklySpending(i,self.getMonth(month),year)})
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

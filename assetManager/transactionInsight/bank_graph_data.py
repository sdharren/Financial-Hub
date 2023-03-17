from forex_python.converter import CurrencyRates
from django.conf import settings
import datetime
from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions

"""
Class of methods to produce data to pass to the frontend to create the graphs
for bank data.
author: Pavan Rana
"""


"""
@params: No params

@Description: -Depending on the settings.PLAID_DEVELOPMENT variable, either DEVELOPMENT for today's exhange rates or the SANDBOX for the fixed 2014 exchange rates for testing

@return: input_date, datetime object for returning corresponding exchange rate
"""
def get_currency_converter():
    if settings.PLAID_DEVELOPMENT is False:
        input_date = datetime.datetime(2014, 5, 23, 18, 36, 28, 151012)
    else:
        input_date = datetime.datetime.today()

    return input_date

def check_value_is_none(value_in_dict):
    if(value_in_dict is None):
        return 'Not Provided'
    else:
        return value_in_dict

def handle_case(account):
    input_date = get_currency_converter()
    currency_rates = CurrencyRates()
    converted_amount = round(currency_rates.convert(account['iso_currency_code'], 'GBP', account['amount'],input_date),2)

    if(account['authorized_date'] is None):
        authorized_date = 'Not Provided'
    else:
        authorized_date = [account['authorized_date'].year,account['authorized_date'].month,account['authorized_date'].day]

    if(account['date'] is None):
        date = 'Not Provided'
    else:
        date = [account['date'].year,account['date'].month,account['date'].day]

    merchant = check_value_is_none(account['merchant_name'])
    category = check_value_is_none(account['category'])
    name = check_value_is_none(account['name'])

    case = {'authorized_date':authorized_date,'date':date, 'amount':converted_amount, 'category': category, 'name':name,'iso_currency_code':account['iso_currency_code'], 'merchant_name':merchant}

    return case


def format_transactions(transactions):
    reformatted_transactions = []
    try:
        for account in transactions:
            case = handle_case(account)
            reformatted_transactions.append(case)

        return reformatted_transactions
    except:
        return transactions

class BankGraphData():
    def __init__(self,transaction_history):
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

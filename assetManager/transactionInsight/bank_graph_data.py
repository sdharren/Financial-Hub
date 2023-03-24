from forex_python.converter import CurrencyRates
from django.conf import settings
import datetime
from assetManager.transactionInsight.bank_transaction_insight import CategoriseTransactions
import requests
import warnings
import json

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
        #input_date = datetime.datetime(2014, 5, 23, 18, 36, 28, 151012)
        input_date = datetime.datetime(2014, 5, 23)
    else:
        input_date = datetime.datetime.today()

    return input_date

"""
@params: value_in_dict: dictionary

@Description: -If the value within the dictionary is set to None then it returns the 'Not Provided' otherwise it returns the dictionary

@return: value_in_dict: a dictionary or a string: 'Not Provided'
"""
def check_value_is_none(value_in_dict):
    if(value_in_dict is None):
        return 'Not Provided'
    else:
        return value_in_dict

def handle_case(account,rates):
    converted_amount = round(account['amount'] / rates[account['iso_currency_code']],2)

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

"""
@params: transactions: json

@Description: If the json that is passed into the constructor is in the incorrect format then it gets reformatted otherwise it remains the same

@return: transactions: json or reformatted_transactions: json
"""
def format_transactions(transactions):
    input_date = get_currency_converter()
    url = "https://theforexapi.com/api/{date}?base=GBP&symbols=GBP,USD,JPY,EUR,INR,NOK&rtype=fpy".format(date = input_date.strftime('%Y-%m-%d'))

    response = requests.get(url,verify=False)
    rates = json.loads(response.content.decode('utf-8'))['rates']

    reformatted_transactions = []
    try:
        for account in transactions:
            case = handle_case(account,rates)
            reformatted_transactions.append(case)

        return reformatted_transactions
    except:
        return transactions

"""
Class BankGraphData represents transaction data organized for easy graphing.

Constructor:
    @params: transaction_history, list of dictionaries containing raw transaction data to be categorized and analyzed

    @instance_variables:
        -transactionInsight: CategoriseTransactions object containing the categorized transaction data
"""

class BankGraphData():
    def __init__(self,transaction_history):
        self.transactionInsight = CategoriseTransactions(format_transactions(transaction_history))

    """
    @Description: Calculates the yearly spending for the given `transaction_history`.
        For each year in the range of years, it calls the `get_yearly_spending()` method from `transactionInsight` to get the total spending for that year and appends the year and spending to a list of dictionaries named `yearlySpending`.

    @Return: yearlySpending, a list of dictionaries where each dictionary represents the yearly spending for a year.
        Each dictionary has two keys, 'name' and 'value', where 'name' is the year as a string and 'value' is the yearly spending as a float.
    """
    def yearlySpending(self):
        yearlySpending = []
        rangeOfYears = self.transactionInsight.get_range_of_years()
        if len(rangeOfYears) != 0:
            for year in range(rangeOfYears[0],rangeOfYears[1]+1):
                yearlySpending.append({'name':str(year),'value': self.transactionInsight.get_yearly_spending(year)})
        return yearlySpending

    """
    @params: year, integer value representing the year for which the monthly spending data is needed

    @Description: This method calculates monthly spending data for a particular year. It iterates through each month of the year,
        retrieves monthly spending using the CategoriseTransactions instance's getMonthlySpending method,
        and appends the result to the monthlySpending list. The monthly spending value is rounded to two decimal places.

    @return: monthlySpending, a list of dictionaries, with each dictionary containing 'name' and 'value' keys.
        The 'name' key contains the name of the month and year (e.g. "Jan 2023"), while the 'value' key contains the monthly spending amount.
    """
    def monthlySpendingInYear(self,year):
        monthlySpending = []
        months = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        for i in range(1,13):
            monthlySpending.append({'name':months[i]+" "+str(year),'value': self.transactionInsight.get_monthly_spending(i,year)})
        return monthlySpending

    """
    @params: date, string containing a space-separated month and year, e.g. "Mar 2022"

    @Description: Generates a list of weekly spending data for a given year and month, broken down into 5 weeks.
        Each item in the list contains a dictionary with the keys 'name' (string) and 'value' (float).
        The 'name' field for each week is generated using the week number, and the 'value' field
        is calculated by calling the getWeeklySpending method of the transactionInsight object,
        passing in the week number and the month and year converted to integers.

    @return: weeklySpending, a list of dictionaries containing the name and value for each week's spending in the given month and year.
    """
    def weeklySpendingInYear(self,date):
        weeklySpending = []
        month, year = date.split()
        year = int(year)
        for i in range(1,6):
            weeklySpending.append({'name': "Week " + str(i),'value': self.transactionInsight.get_weekly_spending(i,self.getMonth(month),year)})
        return weeklySpending

    def companySpendingPerSector(self,sector):
        original_list = self.transactionInsight.get_companies_per_sector(sector)
        new_list = []
        for item in original_list:
            if item not in new_list:
                new_list.append(item)
        return new_list

    def orderedCategorisedSpending(self):
        return self.transactionInsight.get_order_categories(self.transactionInsight.transaction_history)

    """
    @params: month (string), year (int)

    @Description: Fetches all transactions in a given month and year
        Orders the transactions by categories and returns the categories and their corresponding spending amounts

    @return: orderedCategories, a list of dictionaries with each dictionary containing a 'name' key (string, representing the category name) and a 'value' key (float, representing the total spending in that category for the given month and year)
    """
    def orderedCategorisedMonthlySpending(self,month,year):
        monthlyTransactions = self.transactionInsight.get_monthly_transactions(month,year)
        return self.transactionInsight.get_order_categories(monthlyTransactions)

    """
    @params: week(int), month (int), year (int)

    @Description: Fetches all transactions in a given month and year
        Orders the transactions by categories and returns the categories and their corresponding spending amounts

    @return: orderedCategories, a list of dictionaries with each dictionary containing a 'name' key (string, representing the category name) and a 'value' key (float, representing the total spending in that category for the given month and year)
    """
    def orderedCategorisedWeeklySpending(self,week,month,year):
        weeklyTransactions = self.transactionInsight.get_weekly_transactions(week,month,year)
        return self.transactionInsight.get_order_categories(weeklyTransactions)

    """
    @params:
        monthName (str): Name of the month in three letter abbreviation (e.g. "Jan")

    @Description:
        Returns the corresponding numeric value of a month given its name in three letter abbreviation.

    @return:
        int: Numeric value of the month (e.g. 1 for "Jan")
    """
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

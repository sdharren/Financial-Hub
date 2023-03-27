"""
Class CategoriseTransactions represents transaction data categorisation, ordering, summation and ranging.

Constructor:
    @params: transaction_history, list of dictionaries containing raw transaction data to be categorized and analyzed

    @instance_variables:
        -transactionInsight: json containing the raw transaction data
"""

class CategoriseTransactions():
    def __init__(self,transaction_history):
        self.transaction_history = transaction_history

    """
    @Description: Returns the transaction history that was passed to the constructor of the BankGraphData class.

    @return: A list of dictionaries representing the transaction history, where each dictionary contains information about a single transaction, including its date, amount, category, and description.
    """
    def get_transaction_history(self):
        return self.transaction_history

    """
    @params: week(int), month (int), year (int)

    @Description: Fetches all transactions in a given week, month, and year.
        Orders the transactions by categories and returns the categories and their corresponding spending amounts.

    @return: orderedCategories, a list of dictionaries with each dictionary containing a 'name' key (string, representing the category name) and a 'value' key (float, representing the total spending in that category for the given week, month, and year)
    """
    def get_order_categories(self,transaction_history):
        categories = self.get_categorised_spending(transaction_history)
        ordered_list_of_categories = sorted(categories.items(), key=lambda x: x[1],reverse=True)
        ordered_dictionary_of_categories = []
        for item in ordered_list_of_categories:
            ordered_dictionary_of_categories.append({'name': item[0],'value': item[1]})
        return ordered_dictionary_of_categories

    """
    @Description: Calculates the total amount spent (excluding deposits) by summing the amount of each transaction in the transaction_history

    @return: amount (float), the total amount spent (excluding deposits)
    """
    def get_total_spending(self):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0:
                amount = amount + item['amount']
        return amount

    """
    @Description: This method fetches the earliest and latest year for which transactions exist in the transaction history.
    It iterates through the transaction history, checks the year for each transaction, and updates the range of years accordingly.

    @return: range_of_years, a list containing two integers representing the earliest and latest year for which transactions exist in the transaction history.
    """
    def get_range_of_years(self):
        range_of_years = []
        for item in self.transaction_history:
            if len(range_of_years) == 0:
                range_of_years.append(item['date'][0])
                range_of_years.append(item['date'][0])
            elif item['date'][0] < range_of_years[0]:
                range_of_years[0] = item['date'][0]
            elif item['date'][0] > range_of_years[1]:
                range_of_years[1] = item['date'][0]
        return range_of_years

    """
    @params: year (int)

    @Description: Calculates the total spending for a given year by iterating over all the transactions in the transaction history.

    @return: amount (float), representing the total spending in the given year.
    """
    def get_yearly_spending(self,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][0] == year:
                amount = amount + item['amount']
        return amount

    """
    @params: month (int), year (int)

    @Description: Calculates the total amount spent in a given month and year, by iterating over all transactions in transaction_history and summing the positive amounts for transactions that occurred in that month and year

    @return: amount (float), representing the total amount spent in the given month and year
    """
    def get_monthly_spending(self,month,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][1] == month and item['date'][0] == year:
                amount = amount + item['amount']
        return amount

    """
    @params: week(int), month(int), year(int)

    @Description: Fetches all transactions in a given week, month, and year
        Returns the total spending for the given week, calculated by summing all positive transaction amounts in the given week

    @return: amount (float), representing the total spending in the given week
    """
    def get_weekly_spending(self,week,month,year):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][2]//7 == week and item['date'][1] == month and item['date'][0] == year:
                amount = amount + item['amount']
        return amount

        """
        @params: company (string)

        @Description: Fetches all transactions for a given company and returns the total spending amount for that company.

        @return: amount (float), representing the total amount spent on transactions with the given company name.
        """
    def get_companies_per_sector(self,sector):
        companies = []
        for item in self.transaction_history:
            if item['category'][0] == sector:
                companies.append({"name": item['name'],"value": self.get_spending_for_company(item['name'])})
        return companies

    # return total spending for the company name passed in
    def get_spending_for_company(self,company):
        amount = 0
        for item in self.transaction_history:
            if item['amount'] > 0 and item['name'] == company:
                amount = amount + item['amount']
        return amount

    """
    @params: transaction_history, a list of dictionaries containing transaction details with keys: 'name' (string, representing the name of the transaction), 'amount' (float, representing the transaction amount), 'category' (list of strings, representing the category/categories that the transaction belongs to), and 'date' (list of integers, representing the year, month and day of the transaction)

    @Description: Categorizes the transactions by category and returns a dictionary with the category names as keys and the corresponding total spending in that category as values.

    @return: spenditure_per_category, a dictionary with category names as keys (strings) and their corresponding total spending as values (floats).
    """
    def get_categorised_spending(self,transaction_history):
        spenditure_per_category = {}
        for item in transaction_history:
            if item['amount'] > 0:
                currentValue = spenditure_per_category.get(item['category'][0]) or 0
                spenditure_per_category[item['category'][0]] = currentValue + item['amount']
        return spenditure_per_category

    """
    @params:
        year (int): The year for which the transactions are to be fetched

    @description:
        Returns a list of all transactions that occurred in the given year, along with their details.
        Only transactions with positive amounts are included in the list.

    @returns:
        A list of dictionaries representing each transaction in the given year
    """
    def get_yearly_transactions(self,year):
        yearly_transactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][0] == year:
                yearly_transactions.append(item)
        return yearly_transactions

    """
    @params:
        - month (int): The month (1-12) to filter transactions by
        - year (int): The year to filter transactions by

    @Description:
        Iterates through all transactions in the transaction history and filters them based on the given month and year. Only transactions with a positive amount are included in the result.

    @return:
        A list of transaction dictionaries that occurred in the given month and year.
    """
    def get_monthly_transactions(self,month,year):
        monthly_transactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][1] == month and item['date'][0] == year:
                monthly_transactions.append(item)
        return monthly_transactions

    """
    @params:
        - week (int): The week to filter transactions by
        - month (int): The month (1-12) to filter transactions by
        - year (int): The year to filter transactions by

    @Description:
        Iterates through all transactions in the transaction history and filters them based on the given week, month and year. Only transactions with a positive amount are included in the result.

    @return:
        A list of transaction dictionaries that occurred in the given week, month and year.
    """
    def get_weekly_transactions(self,week,month,year):
        weekly_transactions = []
        for item in self.transaction_history:
            if item['amount'] > 0 and item['date'][2] <= week*7 and item['date'][1] == month and item['date'][0] == year:
                weekly_transactions.append(item)
        return weekly_transactions

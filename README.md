![FINSC (1200 × 630 px)](https://user-images.githubusercontent.com/123044814/228573703-d980d2af-e1b6-4050-a5ef-d86d30937d63.png)
# 🏦Financial-Hub - FinScope

## 5CCS2SEG Major Group Project - Software Savant's repository for a financial hub to track personal financial assets

## Contributors
- ABHISHEK CHIMBILI - K21014878
- AUGUSTO FAVERO - K21059800
- SERGEI MINAKOV - K21040139
- GUILHERME (Gui) NATARIO RIO-TINTO - K21087441
- DHARREN SANTHALINGAM - K21097488
- PAVAN RANA - K21059898
- MATHEW TRAN - K21074020

# Reference List
Below is a list of all the documentations used by the team to build the back-end API querying functionality:
- [PLAID DOCUMENTATION](https://plaid.com/docs/) -> used for querying bank related data including balances and transactions and investment data for supported institutions

- [YFinance DOCUMENTATION](https://github.com/ranaroussi/yfinance) -> used for gathering investement data along with PLAID

- [BlockCypher DOCUMENTATION](https://www.blockcypher.com/dev/bitcoin/#introduction) -> used to query crypto currency data for Bitcoin and Ethereum

- [ForexPython DOCUMENTATION](https://pypi.org/project/forex-python/) -> used to gather the most recent exchange rates to ensure all data is uniquely quantified using GBP '£'

- [CoinGecko DOCUMENTATION](https://www.coingecko.com/en/api/documentation) -> used to gather the most recent exchange rates for Bitcoin and Ethereum to GBP '£'

# URL LOCATION FOR FINSCOPE ON HEROKU
[FinScope](https://financial-hub.herokuapp.com)

# Currency Client Requirement
- FinScope supports 33 currencies and if linked accounts or transactions are made in currencies that are not supported they are filtered out of the application. If a client only has the unsupported currencies for accounts and transactions then nothing will be displayed to the user
- Stocks data is to represented in USD
- Transactions are to be represented in GBP
- Currency pie chart for banks formats a proportioned pie chart for all different currencies present in all linked accounts using GBP as the uniform currency for conversion and proportioning

## Known bugs and limitations
One known limitation is that on the deployed version of the application entering the url directly in the web browser or refreshing the application (Control + R) will cause an error, this does not happen on the locally deployed version, for this reason avoid typing urls directly use the application as is.
Limitation - upon linking the very first account (bank or brokerage), the application takes up to a minute before the user is redirected to the dashboard. This is because the back-end has to query all the data from Plaid and cache it. This limitation is not present in any other situation.

# 👋Welcome to Financial-Hub
Our application is designed to provide users with a comprehensive overview of their financial status, including investments, general spending, and cryptocurrency assets such as Bitcoin and Ethereum. We have integrated several APIs, including Plaid, BlockCypher, ForexPython, and YFinance, to enable users to link a range of financial institutions and crypto wallets, view their financial data in various types of charts, and gain valuable insights into their finances.

Our team has constructed a REST Framework from scratch to link the backend view functionalities and database in Django to the React frontend using custom endpoints and efficient design principles. We have optimized the application's rendering and display of financial data, ensuring a seamless user experience. The consumption of the REST API in React follows SOLID design principles, using custom hooks and props to handle request creation, query the API and handle the result, as well as return the data. Every one of our dashboard components has had the logic refactored into custom hooks, following the single responsibility principle.

To improve the performance of our application, we have implemented a caching system that guarantees quick responses to user requests. Our view functions are designed to handle any issues that may arise with the caching system, and we have included backup options to retrieve data from the various APIs in case of errors.

We are confident that our Financial-Hub web application will provide you with the tools you need to manage your finances effectively

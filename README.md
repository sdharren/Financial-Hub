# Financial-Hub
5CCS2SEG Major Group Project - Software Savant's repository for a financial hub to track personal financial assets

#Welcome to [NAME OF PROJECT]
Thank you for choosing our Financial-Hub Django and React web application to track your personal financial assets.

Our application is designed to provide users with a comprehensive overview of their financial status, including investments, general spending, and cryptocurrency assets such as Bitcoin and Ethereum. We have integrated several APIs, including Plaid, BlockCypher, ForexPython, and YFinance, to enable users to link a range of financial institutions and crypto wallets, view their financial data in various types of charts, and gain valuable insights into their finances.

Our team has constructed a REST Framework from scratch to link the backend view functionalities and database in Django to the React frontend using custom endpoints and efficient design principles. We have optimized the application's rendering and display of financial data, ensuring a seamless user experience.

To improve the performance of our application, we have implemented a caching system that guarantees quick responses to user requests. Our view functions are designed to handle any issues that may arise with the caching system, and we have included backup options to retrieve data from the various APIs in case of errors.

We are confident that our Financial-Hub web application will provide you with the tools you need to manage your finances effectively. Thank You for choosing to use [NAME OF PROJECT]

#Instructions For Local repository And Testing
Git pull our repository https://github.com/sdharren/Financial-Hub.git

Cd into Financial-Hub

Set Up and activate a virtual environment within the Financial-Hub folder named venv, myenv e.g.

Now its time to install all the relevant requirements
pip install -r requirements.txt

Now that requirements are installed make sure to make migrations for the database
python manage.py migrate

Now the user has the application set up for the backend, if they wish to test the view functionalities in the backend they can do so using the command
python manage.py test

IMPORTANT NOTE: The tests in the backend make a substantial number of calls to the various APIs, meaning that if the test are called too many times in a row this could cause a NUMBER_OF_CALLS exceed error from the various APIs, although these exceptions would be caught by the application when running, due to the extensive number of calls it is required that testing the application should not be done in short frequencies. The test suite on average takes 10 minutes to run all tests

Once tested the user and satisfied with the backend functionality and you may wish to run a local version of the application follow the below steps

#Local Deployment of the application [Project Testers]
Assuming you have the team's submitted zip file version of the project there is one notable difference I ask to verify
Go to settings.py in financeHub, please ensure that only on the local version of the application the variable PLAID_DEVELOPMENT is set to false. The deployed version of the application on Heroku will have this variable set to True, but for the next instructions please ensure on your local repo that this variable is False.

You may now seed the database with a fake user, email: 'johnnydoe@example.org', password: 'Password123' with the command:
python manage.py seed

To unseed the database you may run:
python manage.py unseed

The seeded user has created along with it investment, bank related and crypto dummy data to visualise how the graphs would work and look

Now to deploy the application [Dharren enter instructions here]

Once the above instructions are fulfilled the application should open on the default browser used on the machine running the application

Enter the details shown above and play around with the application

When done we suggest logging out to get a better experience with the caching system but it is not strictly required but recommended

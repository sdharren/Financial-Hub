# 🏦Financial-Hub - 5CCS2SEG Major Group Project - Software Savant's repository for a financial hub to track personal financial assets

# 👋Welcome to [NAME OF PROJECT]
Thank you for choosing our Financial-Hub Django and React web application to track your personal financial assets.

Our application is designed to provide users with a comprehensive overview of their financial status, including investments, general spending, and cryptocurrency assets such as Bitcoin and Ethereum. We have integrated several APIs, including Plaid, BlockCypher, ForexPython, and YFinance, to enable users to link a range of financial institutions and crypto wallets, view their financial data in various types of charts, and gain valuable insights into their finances.

Our team has constructed a REST Framework from scratch to link the backend view functionalities and database in Django to the React frontend using custom endpoints and efficient design principles. We have optimized the application's rendering and display of financial data, ensuring a seamless user experience. The consumption of the REST API in React follows SOLID design principles, using custom hooks and props to handle request creation, query the API and handle the result, as well as return the data. Every one of our dashboard components has had the logic refactored into custom hooks, following the single responsibility principle.

To improve the performance of our application, we have implemented a caching system that guarantees quick responses to user requests. Our view functions are designed to handle any issues that may arise with the caching system, and we have included backup options to retrieve data from the various APIs in case of errors.

We are confident that our Financial-Hub web application will provide you with the tools you need to manage your finances effectively. Thank you for choosing to use [NAME OF PROJECT].

## 💻Instructions For Local Repository And Testing

1. Git pull our repository:
```
git clone https://github.com/sdharren/Financial-Hub.git
```

2. Open Financial-Hub folder in terminal
```
C:users/ cd./Financial-Hub
```

3. Assuming virtualenv is already installed on your machine Set up and activate a virtual environment within the Financial-Hub folder. Click this link to view steps depending on machine [link]

4. Now install all the relevant requirements using:
```
pip3 install -r requirements.txt
```

5. Make sure to make migrations for the database using:
```
python3 manage.py migrate
```

6. To test the view functionalities in the backend, use the command:
```
python3 manage.py test
```

7. IMPORTANT NOTE: The tests in the backend make a substantial number of calls to the various APIs. If the tests are called too many times in a row, this could cause a NUMBER_OF_CALLS exceed error from the various APIs. Although these exceptions would be caught by the application when running, due to the extensive number of calls, it is required that testing the application should not be done in short frequencies. The test suite on average takes 10 minutes to run all tests.

## 📈Local Deployment of the Application [Project Testers]
Assuming you have the team's submitted zip file version of the project, there is one notable difference we ask to verify. Go to **settings.py** in financeHub and please ensure that only on the local version of the application the variable **PLAID_DEVELOPMENT** is set to **False**.

***The deployed version of the application on Heroku will have this variable set to True, but for the next instructions, please ensure on your local repo that this variable is False.***

1. You may now seed the database with a fake user, email: **'johnnydoe@example.org'**, password: **'Password123'** with the command:
```
python manage.py seed
```

2. To unseed the database, you may run:
```
python manage.py unseed
```

3. The seed function along with a user has created investment, bank-related, and crypto dummy data to visualize how the graphs would work and look.

4. In the terminal currently open run the command:
```
python manage.py runserver
```

5. Open new terminal window
   change directory into Financial-Hub:
   ```
   cd ./Financial-Hub
   ```

   activate virtual environment once in Financial-Hub

   change directory into **react-app**:
   ```
   cd ./react-app
   ```

6. Install npm if already not installed already:
```
npm install
```

7. There are two options to run the application.
First option: to run production server which is for normal use as production server is more optimised (RECOMMENDED):
```
npm build
```

-The above command only to be repeatedly run if changes are made to the code base

```
serve -s build
```

8. Option 2 run development: react strict mode is turned off therefore there should not be duplicate calls (NOT RECOMMENDED):

```
npm start
```

9. Once the above instructions are fulfilled, the application should open on the default browser used on the machine running the application.

10. Enter the details shown above and play around with the application.

11. When done testing and using the application, we suggest **logging out**

# Personal Finance Management Application
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/load-image-1-1.jpg)

## Group Members
- Karthika Ramachandran
- Shan Lu (Emma)
- Mohammad Zahur
- Kainat Ahmed
- Sujandar Mahesan

## About the project
The Personal Finance Management Application is a web-based tool that allows users to manage their personal finance, track transactions, and monitor net worth over time. It provides features to add the individual transactions, and produce visualizations of spending breakdowns and income vs. expenses over time.

## Datasets
* [personal_transactions](https://github.com/Emmalu868/Capstone-Project/blob/main/Resources/personal_transactions.csv) - [Kaggle](https://www.kaggle.com/datasets/bukolafatunde/personal-finance?resource=download&select=personal_transactions.csv)
* [personal_finance_data](https://github.com/Emmalu868/Capstone-Project/blob/main/Resources/personal_finance_data.csv) - [Kaggle](https://www.kaggle.com/datasets/abhilashayagyaseni/personal-finance-dataset?resource=download)

## Data Collection and Preparation
Data cleaning is a crucial step in the Personal Finance Management Application project. In this step we focused on ensuring the datasets are accurate, consistent, and ready for analysis. The data cleaning process involved several key steps:

- Handling Missing Values: Addressing missing data points in the datasets is essential to prevent bias and errors in the analysis. Various techniques, such as imputation or removal of rows/columns with missing values, were applied to handle this issue.

- Removing Duplicates: Duplicates in the datasets could lead to erroneous results. The data cleaning process involves identifying and eliminating any duplicate entries to maintain data integrity.

- Data Type Conversion: Converting data to appropriate data types is necessary for accurate calculations and visualizations. During data cleaning, appropriate data types were assigned to each column.

- Data Integration: Merging data from different sources is an important aspect of this project. Data from the personal_transactions and personal_finance_data datasets were integrated, combining relevant information into a unified dataset.

- Handling Inconsistent Categorization: Addressing inconsistencies in categorization and description fields ensures that the analysis and visualizations are meaningful. Standardizing category names and descriptions were part of the data cleaning process.


## Development
### A. Personal Transactions Dashboard (Streamlit) - [personal_transactions.py](https://github.com/Emmalu868/Capstone-Project/blob/main/personal_transactions.py)
**Step 1:** Install necessary packages<br> 
**Step 2:** Prepare the data<br>
**Step 3:** Create the Streamlit app<br>
**Step 4:** Load and process the data<br>
**Step 5:** Create the Streamlit app layout<br>
**Step 6:** Run the Streamlit app by using the commannd `streamlit run personal_transactions.py`

#### Transaction Data
Displays the raw transaction data obtained from a given dataset.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/1.png)

#### Monthly Summary
Displays a summary of monthly transactions, including total credits, total debits, and a pie chart showing the proportion of credits and debits.

##### Summary of Credit Transactions
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/sumcred.png)

##### Summary of Debit Transactions
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/sumdeb.png)

##### Proportion of Credit and Debit Transactions
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/pie.png)

#### Spending Categories Breakdown
Displays a bar chart to visualize spending breakdown by different categories such as groceries, entertainment, utilities, etc., to see where most of the money is going.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/specat1.png)
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/specat2.png)

#### Transaction Timeline
Displays a line plot of total spending over time to track financial progress and identify patterns in spending and saving habits.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/transtime.png)

#### Income vs. Expenses
Displays a comparison of monthly income against monthly expenses to understand how much one is saving or overspending each month.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/invex.png)

#### Credit Card Usage Analysis
Displays credit card statistics, a line chart showing credit card spending over time and a bar chart showing credit card spending by merchant. This helps gain insights into how the credit card is being used, where it is being used, what types of purchases are being made, and other relevant metrics.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/ccusage.png)
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/ccusage1.png)

#### Top Merchants Analysis
Displays the top merchants which helps identify where one spends the most and analyze spending behavior with each merchant.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/personal_transactions/topmer.png)


### B. Personal Finance Data Analysis and Dashboard
**Step 1:** Install necessary packages <br>
##### e.g. `pathlib`, `numpy`, `pandas`, `matplotlib.pyplot`, `seaborn`, `streamlit`, `plotly.express`, `plotly.subplots`, `plotly.graph_objects`
**Step 2:** Prepare the data <br>
**Step 3:** Create the Streamlit app<br>
**Step 4:** Load and process the data<br>
**Step 5:** Create the Streamlit app layout<br>
**Step 6:** Run the Streamlit app by using the commannd `streamlit run B_finance_data.py.py`

#### Transaction Data
Displays the raw transaction data obtained from a given dataset.<br>
<br>
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/B_raw_data.png)

**Debit Analysis**

![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/B_category_analysis.png)
###### Top 3 Amount Spend: 
- 54,810: Household
- 28,887: Other
- 24,607: Food

###### Top 3 Transaction Types:
- Food: 114 
- Transportation: 26
- Other: 21

![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/B_description_analysis.png)
###### Description Analysis:
- Stuffs, Arrear and reval fee, To Kumara are the top 3 description types

**Credit Analysis**
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/B_cr_category_analysis.png)
###### Salary is the primary income resource of 66,910. which weighs 94.6% of the overall income.
###### Other has the most transactions of 29 times, at 67.4%, and followed by Salary 19 times, at 27.88%.


### C. Finance Tracker (Flask)

#### Homepage 
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/homepage.png)

- The homepage presents an intuitively designed web application user interface, facilitating users in entering essential transaction details, such as date of item purchase, product description, amount, product category for grouping, and a type option to differentiate between debit (income) and credit (expense). Additionally, users have the capability to upload their historical financial data by utilizing the "Choose File" and "Upload File" features. Moreover, the platform offers a net worth tracking option, enabling users to monitor their financial progress over time.


#### Transactions
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/trans.png)

- Upon inputting a transaction via the homepage, the system will promptly post and record it under the "Transaction" tab. Subsequently, users are granted the ability to apply filters to their transactions, permitting sorting by date range and purchase category for enhanced transaction management.


#### Reports Tab
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/report.png)

- Upon selecting the "Reports" tab, users gain access to three comprehensive visual reports designed to facilitate a deeper understanding of their financial management. These reports offer valuable insights into their financial status and aid in making informed decisions.


#### Net Worth Tab
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/report.png)

- The Net Worth tab serves as a user-friendly and efficient platform for promptly visualizing and managing the inputted net worth data. Through this tab, users are provided with a comprehensive overview of their net worth, empowering them to gain valuable insights into their financial standing and progress. The Net Worth tab offers a practical function to delete net worth entries when necessary. This feature ensures that users maintain accurate and up-to-date records, enabling them to maintain the integrity and reliability of their financial data.


#### Spending Breakdown Report
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/report1.png)

- The Spending Breakdown Report allows users to visually analyze their spending budget through a meticulously organized pie chart, meticulously divided into categories. This enables users to readily identify patterns and discern their spending habits with ease.


#### Income vs. Expense Report
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/report2.png)

- The Income vs. Expense Report offers users a bar chart visualization of their spending habits, categorized based on a specified date range. By inputting a specific date range, the program efficiently segregates and displays the income and expense transactions inputted by the user, providing a clear overview of their financial activity.


#### Net Worth Over Time Report
![](https://github.com/Emmalu868/Capstone-Project/blob/main/Images/report3.png)

- The Net Worth Over Time Report provides users with a dynamic visualization of their financial trajectory and net worth evolution. This insightful report leverages the meticulously inputted financial data to generate a comprehensive line graph, which graphically illustrates the fluctuations in net worth over a defined time span. As the graph depicts the variations in net worth, users can observe the impact of their financial decisions, investments, and income changes over time. This empowers them to make informed adjustments to their financial strategies and effectively plan for the future.


## Challenges 
The Personal Finance Management Application encountered several challenges during its development. Some of the challenges faced by the team includes:

- Data Cleaning and Preparation: Ensuring the accuracy and consistency of data from external datasets required thorough data cleaning and preparation techniques

- Data Availability: Finding suitable datasets that matches the requirements of our analysis and specification was difficult.

- Performance and Scalability: As the number of users and transactions grows, the application's performance and scalability become crucial. Ensuring the application can handle a large volume of data and user requests efficiently would be a challenge.

- Data Consistency: Ensuring data consistency between the database and user interface and handling concurrent data updates can be challenging.

- Despite these challenges, the team successfully developed the Personal Finance Management Application that provides valuable insights into their finances and empowering them to make informed financial decisions.



  

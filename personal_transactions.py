# Personal Transactions Analysis

################################################################################

# Imports
import pandas as pd
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

################################################################################

# Load personal_transactions.csv file
def load_data():

    # Using the read_csv function and Path module, create a DataFrame by importing personal_transactions.csv file
    personal_transactions = pd.read_csv(Path("Resources/personal_transactions.csv"))
    personal_transactions['Date'] = pd.to_datetime(personal_transactions['Date'])
    return personal_transactions

# Load the data
personal_transactions = load_data()

################################################################################

# Streamlit Code

################################################################################

st.markdown('# Personal Transactions Analysis')
 
# Display the raw data if desired
if st.checkbox('Show Raw Data'):
    st.write(personal_transactions)

################################################################################

# 1 - Monthly Summary
st.markdown('## Monthly Summary')
 
# Group transactions by 'Transaction Type' and 'month'    
grouped_data = personal_transactions.groupby([pd.Grouper(key='Date', freq='M'), 'Transaction Type']).agg(
    Total_Transactions=('Description', 'count'),
    Total_Amount=('Amount', 'sum')
).reset_index()
    
# Create a plot for each 'Transaction Type' (credit or debit)
for transaction_type in grouped_data['Transaction Type'].unique():
    st.markdown(f'### Summary of {transaction_type} Transactions')
        
    filtered_data = grouped_data[grouped_data['Transaction Type'] == transaction_type]
        
    # Display the summary table
    st.dataframe(filtered_data)
        
    # Create a bar plot to visualize the total amount by month for each 'Transaction Type'
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data['Date'], filtered_data['Total_Amount'])
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.title(f'Total Amount of {transaction_type} Transactions by Month')
    plt.xticks(rotation=45)
    st.pyplot(plt)
        
# Create a pie chart to visualize the proportion of credit and debit transactions
fig = px.pie(grouped_data, values='Total_Amount', names='Transaction Type',
title='Proportion of Credit and Debit Transactions')
    
st.plotly_chart(fig)

################################################################################

# 2 - Spending categories Breakdown
st.markdown('## Spending Categories Breakdown')

spending_df = personal_transactions[(personal_transactions['Transaction Type'] == 'debit') & (personal_transactions['Description'] != 'Credit Card Payment')]

# Create a bar chart to show the spending breakdown by category
fig = px.bar(
    spending_df,
    x='Category',
    y='Amount',
    title='Spending Breakdown by Category',
    labels={'Amount': 'Total Amount'},
    color='Category',
    hover_data=['Date', 'Amount']
)
    
# Customize the layout of the chart 
fig.update_layout(
    xaxis_title='Category',
    yaxis_title='Total Amount',
    xaxis_tickangle=-45,
    showlegend=False
)
    
# Display the chart
st.plotly_chart(fig)
    
# Display the table to view detailed transaction data
st.dataframe(spending_df)
    
################################################################################

# 3 - Transaction Timeline
st.markdown('## Transaction Timeline')

# Create a line chart to show the transaction timeline
fig_timeline = px.line(
    personal_transactions,
    x='Date',
    y='Amount',
    title='Transaction Timeline',
    labels={'Amount': 'Total Amount'},
)

# Customize the layout of the chart 
fig_timeline.update_layout(
    xaxis_title='Date',
    yaxis_title='Total Amount',
)

# Display the chart
st.plotly_chart(fig_timeline)

################################################################################

# 4 - Income vs. Expenses
st.markdown('## Income vs. Expenses')

# Create dataframes to include income and expenses 
income_df = personal_transactions[personal_transactions['Transaction Type'] == 'credit']
expenses_df = personal_transactions[personal_transactions['Transaction Type'] == 'debit']

income_vs_expenses = pd.DataFrame({
    'Date': personal_transactions['Date'].unique(),
    'Income': income_df.groupby('Date')['Amount'].sum(),
    'Expenses': expenses_df.groupby('Date')['Amount'].sum().abs(),
})

# Create a bar chart to show income vs expenses
fig_income_expenses = px.bar(
    income_vs_expenses,
    x='Date',
    y=['Income', 'Expenses'],
    title='Income vs. Expenses',
    labels={'value': 'Total Amount', 'variable': 'Category'},
    barmode='group',
)

# Customize the layout of the chart
fig_income_expenses.update_layout(
    xaxis_title='Date',
    yaxis_title='Total Amount',
)

# Display the chart
st.plotly_chart(fig_income_expenses)

################################################################################

# 5 - Credit Card Usage Analysis
st.markdown('## Credit Card Usage Analysis')

# Create dataframes to include credit_card_transactions and non_credit_card_transactions 
credit_card_transactions = personal_transactions[(personal_transactions['Account Name'] == 'Platinum Card') | (personal_transactions['Account Name'] == 'Silver Card')]

# Display basic statistics of the data
st.markdown("### Credit Card Usage Statistics")
st.write(credit_card_transactions.describe())

# Display a line chart to show the trend of credit card spending over time
st.markdown("### Credit Card Spending Over Time")

fig, ax = plt.subplots()
credit_card_transactions.set_index('Date').resample('D')['Amount'].sum().plot(ax=ax)
plt.xlabel("Date")
plt.ylabel("Total Spending")
st.pyplot(fig)

# Display a bar chart to show credit card spending distribution by merchant
st.markdown("### Credit Card Spending by Merchant")

merchant_spending = credit_card_transactions.groupby('Description')['Amount'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 15))
ax.barh(merchant_spending.index, merchant_spending.values)
plt.xlabel("Total Spending")
plt.ylabel("Merchant")
st.pyplot(fig)

################################################################################

# 6 - Top Merchants Analysis
st.markdown('## Top Merchants Analysis')

# Calculate the top merchants and their total transactions
top_merchants = personal_transactions['Description'].value_counts().head(10)
top_merchants = pd.DataFrame({'Merchant': top_merchants.index, 'Total Transactions': top_merchants.values})

# Display the top merchants and their total transactions
st.markdown('#### Top 10 Merchants and Total Transactions')
st.dataframe(top_merchants)

# Plot a bar chart for the top merchants
st.markdown('#### Top 10 Merchants Bar Chart')
st.bar_chart(top_merchants.set_index('Merchant'))

################################################################################

# Running the streamlit app

# 1. In the terminal, navigate to the project folder where you've coded.

# 2. In the terminal, run the Streamlit application by using `streamlit run personal_transactions.py`.


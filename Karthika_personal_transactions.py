# Personal Transactions Analysis

################################################################################

# Imports
import pandas as pd
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

################################################################################

# Load personal_transactions.csv file
def load_data():

    # Using the read_csv function and Path module, create a DataFrame by importing personal_transactions.csv file
    personal_transactions = pd.read_csv(Path("personal_transactions.csv"))
    personal_transactions['Date'] = pd.to_datetime(personal_transactions['Date'])
    return personal_transactions

# Load the data
personal_transactions = load_data()

################################################################################

# Streamlit Code
def main():
    st.markdown("# Personal Transactions Analysis")
    
    # Display the raw data if desired
    if st.checkbox('Show Raw Data'):
        st.write(personal_transactions)
    
    st.markdown("## Monthly Summary")
        
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
    
if __name__ == '__main__':
    main()


################################################################################

# Personal Finance Data Analysis

################################################################################

# Imports
import numpy as np # linear algebra
import pandas as pd
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from plotly.subplots import make_subplots
import plotly.graph_objects as go
################################################################################
# Load personal_finance_data.csv file
def load_data():

    # Using the read_csv function and Path module, create a DataFrame by importing personal_finance.csv file
    personal_finance = pd.read_csv(Path("Resources/personal_finance_data.csv"))
    personal_finance['Date / Time'] = pd.to_datetime(personal_finance['Date / Time'])
    return personal_finance

# Load the data
personal_finance = load_data()

################################################################################
# Streamlit Code
def main():
    st.markdown("# Personal Finance Data Analysis")
    
    # Display the raw data if desired
    if st.checkbox('Show Raw Data'):
        st.dataframe(personal_finance)
    
    st.markdown("## Debit Analysis ")
    personal_finance.rename(columns={"Sub category": "Description","Debit/Credit":"Amount"},inplace=True)
    personal_finance.index.names = ['Date']

# Create a function that operates on the new row called "Transaction Type", that defines Debit/Credit based on Income/Expense
    def f(row):
        if row['Income/Expense'] == "Income": 
            val = "Credit"
        else:
            val = "Debit"
        return val

    personal_finance['Transaction Type'] = personal_finance.apply(f, axis=1)

    #Debit analysis
    debits = personal_finance[personal_finance["Transaction Type"] == 'Debit']
    
    def count_sum(personal_finance ,column: str, plot = "Pie"):
        by_column = personal_finance\
                .groupby(column)\
                .agg({"Transaction Type": "count", "Amount": "sum"})\
                .reset_index()
        by_column.columns = [column, "Transaction Type", "Amount"]
    
        labels = by_column[column]

        fig = None
    
        if plot == 'Pie':
            fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Amount', 'Transaction Type'])
            fig.add_trace(
                go.Pie(
                    labels=labels,
                    values=by_column["Amount"],
                    name="Amount"
                ),
            1, 1)
            fig.add_trace(
                go.Pie(
                    labels=labels,
                    values=by_column["Transaction Type"],
                    name="Transaction Type"
                ),
            1, 2)
        elif plot == 'Scatter':
            fig = make_subplots(1, 2,
                        subplot_titles=['Amount', 'Transaction Type'])
            fig.add_trace(
                go.Scatter(
                    x=labels,
                    y=by_column["Amount"],
                    name="Amount"
                ),
            1, 1)
            fig.add_trace(
                go.Scatter(
                    x=labels,
                    y=by_column["Transaction Type"],
                    name="Transaction Type"
                ),
            1, 2)
        

        fig.update_layout(title_text=f"{column} Analysis")
        # fig.show()
    
        return by_column, fig
    
    pfd_by_cat, fig = count_sum(debits, "Category")
    st.dataframe(pfd_by_cat)
    st.plotly_chart(fig)
    st.markdown("#### Top 3 Amount Spend: ")
    st.markdown("##### $54,810: Household")
    st.markdown("##### $28,887: Other")
    st.markdown("##### $24,607: Food ")     
    
    st.markdown("#### Top 3 Transaction Types: ")
    st.markdown("##### Food: 114")
    st.markdown("##### Transportation: 26")
    st.markdown("##### Other: 21 ")  
    
    pfd_by_payment_way, fig = count_sum(debits, "Description")
    st.dataframe(pfd_by_payment_way)
    st.plotly_chart(fig)
    st.markdown("#### Description Analysis:")
    st.markdown("##### Stuffs, Arrear and reval fee, To Kumara are the top 3 description types ")
    
    #Credit analysis
    credits = personal_finance[personal_finance["Transaction Type"] == 'Debit']
    pfd_cr_by_cat, fig = count_sum(credits, "Category")
    st.dataframe(pfd_cr_by_cat)
    st.plotly_chart(fig)
    
    st.markdown("#### Credit Analysis")
    st.markdown("##### Salary is the primary income resource of $66,910. which weighs 94.6% of the overall income. ")
    st.markdown("##### Other has the most transactions of 29 times, at 67.4%, and followed by Salary 19 times, at 27.88%.")
    
    
if __name__ == '__main__':
    main()


################################################################################

# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import glob

# Function to load all CSV files from a directory
def load_csvs(directory):
    all_files = glob.glob(directory + "/*.csv")
    lst = []

    for filename in all_files:
        df = pd.read_csv(filename)
        start_date = datetime.strptime(str(df['YEAR_AND_MONTH'][0]), '%Y%m')
        df['Datetime'] = [start_date + timedelta(minutes=5*i) for i in range(len(df))]
        lst.append(df)

    combined_df = pd.concat(lst, axis=0, ignore_index=True)
    return combined_df

# Title
st.title("Cryptocurrency Market Graph")

# Upload CSV file
uploaded_directory = st.text_input("Enter the directory path containing CSV files:")
if uploaded_directory:
    try:
        data = load_csvs(uploaded_directory)
        
        # Display raw data (optional)
        if st.checkbox("Show raw data"):
            st.write(data)

        # Plotting the candlestick chart
        st.subheader("Candlestick Chart (5-minute intervals)")
        
        # Create a plotly candlestick chart
        fig = go.Figure(data=[go.Candlestick(x=data['Datetime'],
                                             open=data['OPEN'],
                                             high=data['HIGH'],
                                             low=data['LOW'],
                                             close=data['CLOSE'])])

        # Layout adjustments
        fig.update_layout(title='Cryptocurrency Market Data',
                          xaxis_title='Datetime',
                          yaxis_title='Price',
                          xaxis_rangeslider_visible=True)
        
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"An error occurred: {e}")


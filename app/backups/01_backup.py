# pages/01_data_exploration.py
import streamlit as st
import plotly.express as px
import pandas as pd

def create_visualization(df, query):
    if 'histogram' in query.lower():
        column = query.lower().split('histogram of ')[1].split(' ')[0]
        if column in df.columns:
            fig = px.histogram(df, x=column, nbins=50, color_discrete_sequence=['indianred'])
            fig.update_layout(title=f'Distribution of {column}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"The '{column}' column does not exist in the dataset.")
    elif 'scatter plot' in query.lower():
        columns = query.lower().split('scatter plot of ')[1].split(' and ')
        if len(columns) == 2 and all(col in df.columns for col in columns):
            fig = px.scatter(df, x=columns[0], y=columns[1], color_discrete_sequence=['blue'])
            fig.update_layout(title=f'Scatter Plot of {columns[0]} vs {columns[1]}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Invalid columns specified for the scatter plot.")
    elif 'bar chart' in query.lower():
        column = query.lower().split('bar chart of ')[1].split(' ')[0]
        if column in df.columns:
            fig = px.bar(df, x=column, color_discrete_sequence=['green'])
            fig.update_layout(title=f'Bar Chart of {column}')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"The '{column}' column does not exist in the dataset.")
    else:
        st.warning("Unsupported visualization type. Please try histogram, scatter plot, or bar chart.")

def app():
    st.title("Data Exploration and Visualization")
    
    if 'df' not in st.session_state:
        st.error("Data not loaded. Please load data on the main page.")
        return

    df = st.session_state['df']

    query = st.text_input("Enter your visualization query (e.g., 'histogram of CumOil12Month', 'scatter plot of LateralLength_FT and CumOil12Month', 'bar chart of Operator')")
    if query:
        create_visualization(df, query)
# pages/02_data_preprocessing.py
from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO
import sys

def app():

    # display_master_conversation()

    st.title("Data Preprocessing")

    default_preprocessing_steps = """
    1. Handle missing values: Drop or impute missing values depending on their quantity and the importance of the variable.
    2. Normalize data: Scale numeric features to a common scale if your model is sensitive to the magnitude of features.
    3. Encode categorical variables: Convert categorical variables into numeric codes or one-hot encoding.
    4. Feature selection: Remove irrelevant or redundant features to reduce the dimensionality of the data.
    5. Data transformation: Apply transformations like log, exponential, etc., to change the distribution of the data.
    6. Outlier detection: Identify and handle outliers in the data that might skew the analysis.
    """

    st.write("Below are some common data preprocessing steps to consider:")
    st.text(default_preprocessing_steps)

    context = f"""
    The dataframe is called df.
    Give me the code in one block.
    """

    if prompt := st.chat_input("Enter Query about preprocessing the data"):
        st.session_state.messages.append({"role": "user", "content": prompt + "\n\n" + context})

        with st.chat_message("assistant"):
            if prompt.lower().startswith("run code:"):
                # Extract the code from the user prompt
                code = prompt[len("run code:"):].strip()
                try:
                    globals()['df'] = st.session_state['df']
    
                    exec(code, globals())
                    
                    st.session_state['df'] =  globals()['df']
                    response = "Code executed successfully."
                   
                    st.dataframe(st.session_state['df'])

                except Exception as e:
                    response = f"Error executing code: {str(e)}"
            else:
                response = st.session_state.client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages,
                    temperature=0.5,
                ).choices[0].message.content.strip()

            st.session_state.messages.append({"role": "assistant", "content": response})
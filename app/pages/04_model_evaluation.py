# pages/04_model_evaluation.py
from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO
import sys
import joblib
import os

def app():

    # display_master_conversation()

    # current_file_path = os.path.abspath(__file__)
    # # Get the directory of the current file
    # current_directory = os.path.dirname(current_file_path)
    # model_path = os.path.join(current_directory, 'random_forest_model.pkl')

    # st.session_state['trained_model'] = joblib.load(model_path, mmap_mode='r')

    st.title("Model Evaluation")

    context = f"""
    The dataframe is called df.
    Give me the code in one block.
    """

    if prompt := st.chat_input("Enter Query about evaluating the model"):
        st.session_state.messages.append({"role": "user", "content": prompt + "\n\n" + context})

        with st.chat_message("assistant"):
            if prompt.lower().startswith("run code:"):
                # Extract the code from the user prompt
                code = prompt[len("run code:"):].strip()
                try:
                    globals()['df'] = st.session_state['df']
                    globals()['trained_model'] = st.session_state['trained_model']
    
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
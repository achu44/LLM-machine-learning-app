from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO
import sys
import re

def app():

    st.title("Testing Automatic Execution of Code")
    st.subheader("Copy of Page 5 Data Exploration Using GPT")

    if st.button("Clear Charts"):
        st.session_state['charts'] = []

    st.subheader("Displaying the DataFrame:")
    st.dataframe(st.session_state['df'])

    if 'charts' not in st.session_state:
        st.session_state['charts'] = []

    # Context for GPT
    context = """
    When generating code for data exploration and visualization, please follow these guidelines:
    - Use the Plotly library for creating interactive visualizations.
    - Display the generated plots using the `st.plotly_chart()` function provided by Streamlit.
    - Ensure that the necessary libraries (plotly.express and streamlit) are imported.
    - Use the provided DataFrame `df` for data exploration and plotting.
    - The dataframe is called df.
    - Give me the code in one block.
    - Put code between two <code> like this: <code> this is some code </code>
    """

    # User input for GPT prompt
    if prompt := st.chat_input("Enter Query about Data Exploration"):
        st.session_state.messages.append({"role": "user", "content": context + "\n\n" + prompt})

        with st.chat_message("assistant"):
            if prompt.lower().startswith("run code:"):
                # Extract the code from the user prompt
                code = prompt[len("run code:"):].strip()

                try:
                    globals()['df'] = st.session_state['df']
                    # Execute the generated code
                    exec(code, globals())  # Ensure to use globals() if needed for the scope
                    st.session_state['df'] =  globals()['df']

                    if 'fig' in globals():
                        st.session_state['charts'].append(globals()['fig'])
                        response = "Chart added successfully."
                    else:
                        response = "Code executed successfully."
                except Exception as e:
                    response = f"Error executing code: {str(e)}"
            else:
                response = st.session_state.client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state.messages,
                    temperature=0.5,
                ).choices[0].message.content.strip()
                code_block = re.search(r'<code>(.*?)</code>', response, re.DOTALL)
                if code_block:
                    code = code_block.group(1).strip()
                    # Execute the extracted code
                    globals()['df'] = st.session_state['df']
                    exec(code, globals())
                    st.session_state['df'] =  globals()['df']
                    if 'fig' in globals():
                        st.session_state['charts'].append(globals()['fig'])
                        response = "Chart added successfully."
                    else:
                        response = "Code executed successfully, but no chart was returned."

            st.session_state.messages.append({"role": "assistant", "content": response})
    if st.session_state['charts']:
        st.subheader('All Charts:')
        for chart in st.session_state['charts']:
            st.plotly_chart(chart, use_container_width=True)
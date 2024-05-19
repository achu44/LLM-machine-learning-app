# pages/03_train_models.py
from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO
import sys

class OutputCapture(object):
    def __init__(self):
        self.output = ""

    def write(self, string):
        self.output += string

    def flush(self):
        pass

output_capture = OutputCapture()

def app():

    # display_master_conversation()

    st.title("Train Machine Learning Models")

    model_var_name = st.text_input("Enter the model variable name", "rf_classifier")

    context = f"""
    The dataframe is called df.
    Give me the code in one block.
    """

    if prompt := st.chat_input("Enter Query about Training the Model"):
        st.session_state.messages.append({"role": "user", "content": prompt + "\n\n" + context})

        with st.chat_message("assistant"):
            if prompt.lower().startswith("train model:"):
                if not model_var_name.strip():
                    response = "Please enter a valid model variable name before proceeding."
                elif not model_var_name.isidentifier():
                    response = "The model variable name must be a valid Python identifier."
                else:
                    st.session_state.messages.append({"role": "user", "content": f"Use {model_var_name} as the model name when initializing the classifier."})
                    response = st.session_state.client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=st.session_state.messages,
                        temperature=0.5,
                    ).choices[0].message.content.strip()
            elif prompt.lower().startswith("run code:"):
                # Extract the code from the user prompt
                code = prompt[len("run code:"):].strip()
                try:
                    globals()['df'] = st.session_state['df']
                    if 'fit' in code:
                        original_stdout = sys.stdout
                        sys.stdout = output_capture
                    exec(code, globals())
                    if 'fit' in code:
                        sys.stdout = original_stdout
                    if 'fit' in code:
                        st.session_state['trained_model_name'] = model_var_name
                        st.session_state['trained_model'] = globals()[model_var_name]
                    st.session_state['df'] =  globals()['df']
                    response = "Code executed successfully."
                    if 'fit' in code:
                        st.subheader("Training Progress")
                        st.text(output_capture.output)
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
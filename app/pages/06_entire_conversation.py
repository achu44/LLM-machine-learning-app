from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import StringIO
import sys

def app():

    st.title("Entire Conversation:")

    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
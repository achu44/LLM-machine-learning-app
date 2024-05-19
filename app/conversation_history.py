# conversation_history.py
import streamlit as st

def display_master_conversation():
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">The below is the Master conversation history</p>', unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
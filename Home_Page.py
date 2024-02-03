import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os


st.set_page_config(page_title="Gen-e",page_icon="🤖")
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


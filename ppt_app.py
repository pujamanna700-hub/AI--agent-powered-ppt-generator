#===========load module =============
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
import numpy as np
import streamlit as st

GOOGLE_KEY = st.sidebar.text_input("GOOGLE-API",type = "password")
GROQ_KEY =  st.sidebar.text_input("GROQ-API,type = "password")
TAVILY_KEY =  st.sidebar.text_input("TAVILY-API,type = "password")

os.environ["GOOGLE_API_KEY"] = GOOGLE_KEY
os.environ["GROQ_API_KEY"] = GROQ_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_KEY

ALL_API=[GOOGLE_KEY,GROQ_KEY,TAVILY_KEY]

if not all(ALL_API):





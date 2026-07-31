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

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE-API",type = "password")
GROQ_API_KEY =  st.sidebar.text_input("GROQ-API",type = "password")
TAVILY_API_KEY =  st.sidebar.text_input("TAVILY-API",type = "password")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

ALL_API=[GOOGLE_KEY,GROQ_KEY,TAVILY_KEY]

if not all(ALL_API):
  st.sidebar.error("PASS API-KEYS")
elif all(ALL_API):
    # Step 1: Model Call
  model=ChatGoogleGenerativeAI(
      model = "gemini-3.5-flash-lite", google_api_key = GOOGLE_API_KEY )
  st.sidebar.success("API KEYS LOADED SUCCESSFULLY")
elif any(ALL_API):
  st.sidebar.info("MUST PASS ALL API KEYS")

else:
  st.info("loaded")

  

#========frontend===========
st.title("AI-AGENT-powered ppt generator")
user_query = st.text_area("write your ppt topic or prompt:")

#==============assets===========
#tool 1

def search_latest_info(query):
  """this function search latest
  news or content from website
  using tavily, helpful to check
  trending content"""

  client = TavilyClient(api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response

#tool2
def generate_image(img_prompt):
  """this function is used to generate image
  using free api, with given
  img_prompt using pollination"""

  url = f"https://image.pollinations.ai/{img_prompt}"
  #file handling
  import requests as r
  content = r.get(url).content
  with open(f"Image.jpeg",'wb') as f:
    f.write(content)

  from PIL import Image
  return Image.open(f"Image.jpeg")
# WITH TABS
tabl, tab2, tab3 st.tabs(["GENERATE IMAGE",
                         "CHECK LATEST NEWS"
                          "GENERATE PPT"
                          ])

def prompt_generator(model,query):
  prompt =f"""your task is to give detailed prompt instruction
  for given,
  prompt:
  you are a professional ppt generator, where user will give
  the query and based on that,
  you have to generate dynamic,html output based
  ppt with advanced CSS and dynamic UI AND ux with
  ppt toggle button, baseed on query take image reference
  to generate  and embed the same in ppt ,using

  Image ref: url = https://images.unsplash.com/photo, 
  or url = https://image.pollinations.ai/, 
  make sure img src must be valid, and image must be
  present inside html, Generate with image caption, and no markdowns
  user query given below:{query}
  """

  response = model.invoke(prompt)
  final_prompt = response.content[-1]['text']

  with open("ppt_prompt.txt",'w') as f:
    f.write(final_prompt)
  return final_prompt

if all(ALL_API) and user_query:
      agent= create_agent(
        model= model,
        tools=[search_latest_info,
               generate_image]
      )
    
    #=========display agent===========
    #st.sidebar.image(agent)
    #=========with tabs===============
    with tab1:
      st.header("generate image give prompt")
      if st.button("click to generate:",key="generate image button"):
        with st.spinner("running agent"):
          data = f" https://image.pollinations.ai/{user_query}"
          time.sleep(3)
          st.image(data)
          st.image("Image.jpeg")
    
    with tab2:
      st.header("check latest news")
      if st.button("Fetch news: ",key = "news_button"):
        with st.spinner ("Running Agent.."):
        
          prompt = """Give latest news India or world news related to tech, business, jobs, or user requested Output
          In Proper HTML News Templates""" + user_query
          response = agent.invoke({'messages': [{'role': "user","content":prompt}]})
          code = response['messages') (-1).content[-1]['text']
          st.html(code, width="stretch",
                  unsafe_allow_javascript=True)
    
    with tab3:
      st.header("Create PPT")
      if st.button("Click to generate: ", key="generate ppt button"):
        with st.spinner ("Running Agent.."):
          final_prompt = prompt_generator (model, user_query)
          
          response agent.invoke({'messages': [{'role':"user","content":final_prompt}]})
          
          code = response['messages') (-1).content[-1]['text']
          
          st.html(code, width="stretch",unsafe_allow_javascript=True)
          
          if st.download_button(label = "DOWNLOAD PPT",data = code,file_name = 'ppt.html',mime = 'text/html'):
          
            st.success("PPT Downloaded Successfully!!")
    
    
    

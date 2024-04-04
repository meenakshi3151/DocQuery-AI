import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from pandasai import SmartDataframe
from pandasai.llm import GooglePalm

load_dotenv()

api = os.getenv('API_KEY')

# Function for pandas ai to query a csv file
def chat_with_csv(data,prompt):
   llm = GooglePalm(api_key = api)
   df = SmartDataframe(data,config={"llm":llm})
   result = df.chat(prompt)
   print(result)
   return result


st.set_page_config(layout="wide")

st.title("ChatCSV powered by LLM")

input_csv = st.file_uploader("Upload your CSV file",type=['csv'])

if input_csv is not None:
   col1,col2 = st.columns([1,1])

   with col1:
      st.info("CSV uploaded successfully")
      data = pd.read_csv(input_csv)
      st.dataframe(data)
    
   with col2:
      st.info("Chat with your CSV")

      input_text = st.text_area("Enter your query")
      if input_text is not None:
         if st.button("Ask"):
            st.info("Your query:"+input_text)
            result = chat_with_csv(data,input_text)
            st.success(result)
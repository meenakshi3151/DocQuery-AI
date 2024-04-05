import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from pandasai import SmartDataframe
from pandasai.llm import GooglePalm

import google.generativeai as genai

from PyPDF2 import PdfReader  
load_dotenv()
genai.configure(api_key=os.environ['API_KEY'])

api = os.getenv('API_KEY')
model = genai.GenerativeModel('gemini-pro')

# Function for pandas ai to query a csv file
def chat_with_pdf(text, prompt):

    response = model.generate_content(prompt+" The pdf document text is given as: "+text)
    print(response.text)
    return response.text
def chat_with_csv(data,prompt):
   llm = GooglePalm(api_key = api)
   df = SmartDataframe(data,config={"llm":llm})
   result = df.chat(prompt)
   print(result)
   return result


st.set_page_config(layout="wide")

st.title("ChatWithFiles powered by LLM")

input_csv = st.file_uploader("Upload your CSV file",type=['csv'])

if input_csv is not None:
   col1,col2 = st.columns([1,1])

   with col1:
      st.info("CSV uploaded successfully")
      data = pd.read_csv(input_csv)
      st.dataframe(data)
    
   with col2:
    st.info("Chat with your CSV")
    input_text = st.text_area("Enter your query")  # check why 1st word not coming
    if input_text is not None:
        col1, col2 = st.columns([1,4])  # Create two columns
        if col1.button("Ask Query"):
            st.info("Your query:" + " " + input_text)
            result = chat_with_csv(data, input_text)
            st.success(result)
        if col2.button("Plot Graph"):
            st.info("Your query:" + " " + input_text)
            result = chat_with_csv(data, input_text)
            st.image('exports/charts/temp_chart.png')


def extract_text_from_pdf(pdf_file):
    text = ""
   #  print("hello")
    with pdf_file as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()

    return text


input_pdf = st.file_uploader("Upload your PDF file ", type=['pdf'])
# print("hi")
if input_pdf is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("PDF uploaded successfully")
        text = extract_text_from_pdf(input_pdf)
        st.text_area("PDF Text", text, height=500)
    with col2:
        st.info("Chat with your PDF")
        input_text = st.text_area("Enter your query")
        if input_text is not None:
            if st.button("Ask Query"):
                st.info("Your query: {}".format(input_text))
                result = chat_with_pdf(text, input_text)
                st.success(result)
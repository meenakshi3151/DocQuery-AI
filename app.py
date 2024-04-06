import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from pandasai import SmartDatalake
from pandasai.llm import GooglePalm

import google.generativeai as genai

from PyPDF2 import PdfReader  
load_dotenv()
genai.configure(api_key=os.environ['API_KEY'])

api = os.getenv('API_KEY')
model = genai.GenerativeModel('gemini-pro')

# Function for pandas ai to query a csv file
def chat_with_pdf(text, prompt):
    pdf_text = ""
    for data in text: 
        pdf_text += data
    response = model.generate_content(prompt+" The pdf document text is given as: "+pdf_text)
    print(response.text)
    return response.text

def chat_with_csv(data,prompt):
   llm = GooglePalm(api_key = api)
   df = SmartDatalake(data,config={"llm":llm})
   result = df.chat(prompt)
   print(result)
   return result


st.set_page_config(layout="wide")

st.title("ChatWithFiles powered by LLM")

all_csv = st.file_uploader("Upload your CSV file",type=['csv'], accept_multiple_files=True)

if all_csv:
   selected_file = st.selectbox("Select a CSV file", [file.name for file in all_csv])
   selected_index = [file.name for file in all_csv].index(selected_file)
   col1,col2 = st.columns([1,1])

   with col1:
      st.info("CSV uploaded successfully")
      data = []
      for file in all_csv: 
          data.append(pd.read_csv(file))
      st.dataframe(data[selected_index])
    
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
            result = chat_with_csv(data[selected_index], input_text)
            st.image('exports/charts/temp_chart.png')


def extract_text_from_pdf(pdf_file):
    text = ""
    with pdf_file as file:
        reader = PdfReader(file)
        for page in reader.pages:
            st = page.extract_text()
            text += st
    return text


input_pdf = st.file_uploader("Upload your PDF file ", type=['pdf'], accept_multiple_files=True)
# print("hi")
if input_pdf:
    selected_file = st.selectbox("Select a CSV file", [file.name for file in input_pdf])
    selected_index = [file.name for file in input_pdf].index(selected_file)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("PDF uploaded successfully")
        text = []
        for file in input_pdf: 
            text.append(extract_text_from_pdf(file))
        
        st.text_area("PDF Text", text[selected_index], height=500)
    with col2:
        st.info("Chat with your PDF")
        input_text = st.text_area("Enter your query")
        if input_text is not None:
            if st.button("Ask Query"):
                st.info("Your query: {}".format(input_text))
                result = chat_with_pdf(text, input_text)
                st.success(result)
import streamlit as st
import pandas as pd
from llama_index.indices.struct_store import GPTPandasIndex
import os
import re
import json

st.markdown("""
          <style>
          footer {visibility: hidden;}
          </style>""", unsafe_allow_html=True)

with st.sidebar:
       #os.environ['OPENAI_API_KEY'] = st.text_input('Your OpenAI API KEY', type="password")
       OPENAI_API_KEY  = st.text_input('Your OpenAI API KEY', type="password")

pattern = r"\bgraph\b"

st.title("Data Agent SCD")

file = st.file_uploader("Upload csv file", type=["csv"])

if file:
    df = pd.read_csv(file)
    index = GPTPandasIndex(
        df=df,
    )
    query_engine = index.as_query_engine(
        verbose=True
    )
    text = st.text_input("Enter your query:")

    if text:
        if re.search(pattern, text):
            query = text.replace("create a graph of", "")
            query = query + " in json of only required columns"
            response = query_engine.query(query)
            response = str(response)
            data = json.loads(response)
            graph = pd.DataFrame(data)

            st.markdown("<b>Response:</b>", unsafe_allow_html=True)
            st.bar_chart(graph)
        else:
            response = query_engine.query(text)
            st.markdown("<b>Response:</b>", unsafe_allow_html=True)
            st.text(response)


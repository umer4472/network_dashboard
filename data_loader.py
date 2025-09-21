import streamlit as st
import pandas as pd
import requests
import os

@st.cache_data
def load_data():
    url = os.getenv("API_URL", "http://localhost:8000/data")
    resp = requests.get(url)
    data = resp.json()
    df = pd.DataFrame(data)
    return df

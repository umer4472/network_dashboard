import streamlit as st
import pandas as pd
import os

def load_data(file_name="data.xlsx"):
    """
    Load Excel data. Works both locally and on Streamlit Cloud.
    If file is not found locally, Streamlit will prompt for upload.
    """
    if os.path.exists(file_name):
        # Local environment
        df = pd.read_excel(file_name)
    else:
        # Streamlit Cloud or missing file
        uploaded_file = st.file_uploader(f"Upload {file_name}", type="xlsx")
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
        else:
            st.stop()  # Stop execution until the file is uploaded
    return df

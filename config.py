import streamlit as st

def set_page_config():
    st.set_page_config(
        layout="wide",
        page_title="Network Availability Dashboard"
    )

def inject_css():
    st.markdown(
        """
        <style>
        .sticky-header {
            position: fixed;
            top: 0;
            z-index: 100;
            background-color: white;
            width: 100%;
            padding: 10px 20px;
            border-bottom: 1px solid #ddd;
        }
        .block-container {
            padding-top: 120px; /* Push main content below sticky header */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

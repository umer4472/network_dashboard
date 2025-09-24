import streamlit as st
from config import set_page_config, inject_css
from data_loader import load_data
from filters import filters
from plot_utils import plot_all_together

# ------------------------
# Setup
# ------------------------
set_page_config()
inject_css()

col1, col2 = st.columns([1, 6])
with col1:
    st.image("mobily_logo.png", width=80)
with col2:
    st.title("Network Availability Dashboard")
# ------------------------
# Load data
# ------------------------
df = load_data()

# ------------------------
# Filters
# ------------------------
filtered_df = filters(df)

# ------------------------
# Plots
# ------------------------

plot_all_together(filtered_df)

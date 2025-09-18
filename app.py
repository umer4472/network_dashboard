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

#!/bin/bash
# start.sh

# Start FastAPI in background
uvicorn api:app --host 0.0.0.0 --port 8000 --reload &

# Start Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

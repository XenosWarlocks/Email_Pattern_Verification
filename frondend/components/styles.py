# frontend/components/styles.py
import streamlit as st
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))

def set_custom_style():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .upload-box {
            border: 2px dashed #4CAF50;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }
        .upload-box:hover {
            border-color: #45a049;
            background-color: #f0f2f0;
        }
        .status-box {
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

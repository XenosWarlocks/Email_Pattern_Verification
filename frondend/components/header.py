# frontend/components/header.py
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))
import streamlit as st

def render_header():
    st.markdown("""
        <style>
        .header {
            padding: 1.5rem;
            background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        </style>
        <div class="header">
            <div class="header-content">
                <h1>✉️ Email Pattern Verifier</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)
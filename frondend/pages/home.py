# frontend/pages/home.py
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))
import streamlit as st

def main():
    # Hero section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 2rem;'>
                <h2>Verify Email Patterns at Scale</h2>
                <p>Fast, accurate, and reliable email pattern verification for businesses</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.button("🚀 Get Started", use_container_width=True, type="primary")
    
    # Features section
    st.markdown("---")
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h3>🚀 Bulk Processing</h3>
                <p>Verify thousands of email patterns in minutes with our optimized processing engine.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h3>🎯 High Accuracy</h3>
                <p>Advanced pattern matching algorithms ensure precise and reliable results.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h3>📊 Detailed Analytics</h3>
                <p>Get comprehensive insights with our detailed verification reports.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("## 🔍 How It Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            1. **Upload Your Data**
            - Excel file with names and patterns
            - Bulk upload support
            - Flexible format options
        """)
    
    with col2:
        st.markdown("""
            2. **Process & Verify**
            - Advanced pattern matching
            - Real-time processing
            - Error checking
        """)
    
    with col3:
        st.markdown("""
            3. **Get Results**
            - Detailed reports
            - Export options
            - Analytics dashboard
        """)
# frontend/components/sidebar.py
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))
import requests
import streamlit as st

def check_api_health():
    try:
        response = requests.get(f"{st.session_state.API_URL}/api/health")
        return response.status_code == 200
    except:
        return False

def render_sidebar():
    with st.sidebar:
        st.image("https://via.placeholder.com/150?text=Logo", width=150)
        
        # Navigation
        st.markdown("## Navigation")
        pages = {
            "🏠 Home": "home",
            "✉️ Email Verifier": "verify",
            "💰 Pricing": "pricing",
            "📊 Dashboard": "dashboard"
        }
        
        for label, page in pages.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
        
        # API Status
        st.markdown("---")
        st.markdown("### System Status")
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected", icon="✅")
        else:
            st.error("❌ API Disconnected", icon="❌")

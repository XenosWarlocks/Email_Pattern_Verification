# # frontend/streamlit_app.py
# import streamlit as st
# import pandas as pd
# import requests
# from io import BytesIO
# import time

# # Configuration
# API_URL = "http://localhost:5000"

# def set_custom_style():
#     st.markdown("""
#         <style>
#         .main {
#             padding: 2rem;
#         }
#         .stButton>button {
#             width: 100%;
#         }
#         .upload-box {
#             border: 2px dashed #4CAF50;
#             border-radius: 10px;
#             padding: 2rem;
#             text-align: center;
#             margin: 1rem 0;
#         }
#         .status-box {
#             padding: 1rem;
#             border-radius: 5px;
#             margin: 1rem 0;
#         }
#         </style>
#     """, unsafe_allow_html=True)

# def main():
#     # Page configuration
#     st.set_page_config(
#         page_title="Email Pattern Verifier",
#         page_icon="✉️",
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
    
#     set_custom_style()
    
#     # Sidebar
#     with st.sidebar:
#         st.image("https://via.placeholder.com/150?text=Logo", width=150)
#         st.markdown("## Quick Links")
#         if st.button("📚 Documentation"):
#             st.markdown("[View Documentation](https://docs.example.com)")
#         if st.button("❓ FAQ"):
#             st.markdown("[View FAQ](https://faq.example.com)")
        
#         # API Status
#         st.markdown("---")
#         st.markdown("### System Status")
#         api_status = check_api_health()
#         if api_status:
#             st.success("✅ API Connected", icon="✅")
#         else:
#             st.error("❌ API Disconnected", icon="❌")
#             st.stop()
    
#     # Main content
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.markdown(
#             "<h1 style='text-align: center;'>✉️ Email Pattern Verifier</h1>", 
#             unsafe_allow_html=True
#         )
#         st.markdown(
#             "<p style='text-align: center;'>Upload your Excel file to verify email patterns</p>", 
#             unsafe_allow_html=True
#         )
    
#     # File upload section
#     st.markdown("---")
#     upload_col1, upload_col2, upload_col3 = st.columns([1, 2, 1])
#     with upload_col2:
#         st.markdown(
#             """
#             <div class='upload-box'>
#                 <h3>📤 Upload Excel File</h3>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
#         uploaded_file = st.file_uploader(
#             "Choose an Excel file (.xlsx)",
#             type="xlsx",
#             help="File must contain: 'Full Name', 'Company URL', and 'Pattern' columns"
#         )
    
#     if uploaded_file:
#         # File details
#         st.markdown("### 📋 File Details")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.info(f"📄 Filename: {uploaded_file.name}")
#         with col2:
#             st.info(f"📦 Size: {uploaded_file.size / 1024:.2f} KB")
        
#         # Preview data
#         try:
#             df = pd.read_excel(uploaded_file)
#             with st.expander("👀 Preview Upload Data", expanded=True):
#                 st.dataframe(
#                     df.head(),
#                     use_container_width=True,
#                     hide_index=True
#                 )
#         except Exception as e:
#             st.error("❌ Error reading file. Please ensure it's a valid Excel file.")
#             st.stop()
        
#         # Process button
#         if st.button("🚀 Process File", type="primary", use_container_width=True):
#             with st.spinner("🔄 Processing your file..."):
#                 # Create progress tracking
#                 progress_placeholder = st.empty()
#                 progress_bar = st.progress(0)
#                 status_text = st.empty()
                
#                 # Simulate progress for better UX
#                 for i in range(5):
#                     progress_placeholder.metric(
#                         "Processing Status", 
#                         f"{i*20}%", 
#                         "In Progress"
#                     )
#                     progress_bar.progress(i * 20)
#                     status_text.info(f"Step {i+1}/5: {'Uploading'if i==0 else 'Processing'if i<4 else 'Finalizing'}...")
#                     time.sleep(0.5)
                
#                 try:
#                     # Send file to API
#                     files = {'file': ('input.xlsx', uploaded_file.getvalue())}
#                     response = requests.post(f"{API_URL}/api/upload", files=files)
                    
#                     if response.status_code == 200:
#                         progress_bar.progress(100)
#                         progress_placeholder.metric(
#                             "Processing Status", 
#                             "100%", 
#                             "Complete!"
#                         )
#                         status_text.success("✅ Processing complete!")
                        
#                         # Download section
#                         st.markdown("### 📥 Download Results")
#                         col1, col2 = st.columns([2, 1])
#                         with col1:
#                             st.download_button(
#                                 label="⬇️ Download Processed File",
#                                 data=response.content,
#                                 file_name="Verified_Email_Patterns.xlsx",
#                                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                                 use_container_width=True
#                             )
                        
#                         # Display results preview
#                         with st.expander("📊 Results Preview", expanded=True):
#                             result_df = pd.read_excel(BytesIO(response.content))
#                             st.dataframe(
#                                 result_df.head(),
#                                 use_container_width=True,
#                                 hide_index=True
#                             )
#                     else:
#                         st.error(f"❌ Processing failed: {response.json().get('error', 'Unknown error')}")
                
#                 except Exception as e:
#                     st.error(f"❌ An error occurred: {str(e)}")
                
#                 # Display logs
#                 display_logs()
    
#     # Help section
#     with st.expander("💡 How to Use", expanded=False):
#         st.markdown("""
#         ### Quick Start Guide
        
#         1. **Prepare Your Excel File** 📑
#            - Required columns:
#              - `Full Name`
#              - `Company URL`
#              - `Pattern`
        
#         2. **Upload Your File** 📤
#            - Click 'Browse files' or drag and drop
#            - Supported format: `.xlsx`
        
#         3. **Process and Download** 🔄
#            - Click 'Process File'
#            - Wait for processing
#            - Download results
        
#         ### Pattern Examples
#         | Pattern | Example |
#         |---------|---------|
#         | `{first}.{last}` | john.doe |
#         | `{f}{last}` | jdoe |
#         | `{first}_{last}` | john_doe |
#         """)

# def check_api_health():
#     try:
#         response = requests.get(f"{API_URL}/api/health")
#         return response.status_code == 200
#     except:
#         return False

# def display_logs():
#     try:
#         response = requests.get(f"{API_URL}/api/logs")
#         if response.status_code == 200:
#             logs = response.json().get('logs', '')
#             if logs:
#                 with st.expander("📋 Processing Logs", expanded=True):
#                     st.code(logs, language="text")
#     except Exception as e:
#         st.warning("⚠️ Unable to fetch logs")

# if __name__ == "__main__":
#     main()

############################################################################
# frontend/streamlit_app.py

import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))

import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import time
from components.header import render_header
from components.footer import render_footer
from components.sidebar import render_sidebar
from components.styles import set_custom_style
from pages import home, pricing, dashboard

# Configuration
if 'API_URL' not in st.session_state:
    st.session_state.API_URL = "http://localhost:5000"

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

def verify_page():
    st.markdown("## Email Pattern Verification")
    
    # File upload section
    upload_col1, upload_col2, upload_col3 = st.columns([1, 2, 1])
    with upload_col2:
        st.markdown(
            """
            <div class='upload-box'>
                <h3>📤 Upload Excel File</h3>
                <p>Drag and drop or click to upload</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Choose an Excel file (.xlsx)",
            type="xlsx",
            help="File must contain: 'Full Name', 'Company URL', and 'Pattern' columns"
        )
    
    if uploaded_file:
        process_uploaded_file(uploaded_file)

def process_uploaded_file(uploaded_file):
    # File details
    st.markdown("### 📋 File Details")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📄 Filename: {uploaded_file.name}")
    with col2:
        st.info(f"📦 Size: {uploaded_file.size / 1024:.2f} KB")
    
    # Preview data
    try:
        df = pd.read_excel(uploaded_file)
        with st.expander("👀 Preview Upload Data", expanded=True):
            st.dataframe(
                df.head(),
                use_container_width=True,
                hide_index=True
            )
    except Exception as e:
        st.error("❌ Error reading file. Please ensure it's a valid Excel file.")
        return
    
    # Process button
    if st.button("🚀 Process File", type="primary", use_container_width=True):
        process_file(uploaded_file)

def process_file(uploaded_file):
    with st.spinner("🔄 Processing your file..."):
        progress_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(5):
            progress_placeholder.metric(
                "Processing Status", 
                f"{i*20}%", 
                "In Progress"
            )
            progress_bar.progress(i * 20)
            status_text.info(f"Step {i+1}/5: {'Uploading'if i==0 else 'Processing'if i<4 else 'Finalizing'}...")
            time.sleep(0.5)
        
        try:
            files = {'file': ('input.xlsx', uploaded_file.getvalue())}
            response = requests.post(f"{st.session_state.API_URL}/api/upload", files=files)
            
            handle_api_response(response, progress_bar, progress_placeholder, status_text)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
        
        display_logs()

def handle_api_response(response, progress_bar, progress_placeholder, status_text):
    if response.status_code == 200:
        progress_bar.progress(100)
        progress_placeholder.metric(
            "Processing Status", 
            "100%", 
            "Complete!"
        )
        status_text.success("✅ Processing complete!")
        
        display_download_section(response.content)
    else:
        st.error(f"❌ Processing failed: {response.json().get('error', 'Unknown error')}")

def display_download_section(content):
    st.markdown("### 📥 Download Results")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.download_button(
            label="⬇️ Download Processed File",
            data=content,
            file_name="Verified_Email_Patterns.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with st.expander("📊 Results Preview", expanded=True):
        result_df = pd.read_excel(BytesIO(content))
        st.dataframe(
            result_df.head(),
            use_container_width=True,
            hide_index=True
        )

def display_logs():
    try:
        response = requests.get(f"{st.session_state.API_URL}/api/logs")
        if response.status_code == 200:
            logs = response.json().get('logs', '')
            if logs:
                with st.expander("📋 Processing Logs", expanded=True):
                    st.code(logs, language="text")
    except Exception as e:
        st.warning("⚠️ Unable to fetch logs")

def main():
    st.set_page_config(
        page_title="Email Pattern Verifier",
        page_icon="✉️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_custom_style()
    render_sidebar()
    render_header()
    
    # Route to appropriate page
    pages = {
        "home": home.main,
        "verify": verify_page,
        "pricing": pricing.main,
        "dashboard": dashboard.main
    }
    
    current_page = st.session_state.get('current_page', 'home')
    pages[current_page]()
    
    render_footer()

if __name__ == "__main__":
    main()
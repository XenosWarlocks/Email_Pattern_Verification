# # components/footer.py
# import streamlit as st

# def render_footer():
#     st.markdown("---")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("### Company")
#         st.markdown("- [About Us](https://example.com/about)")
#         st.markdown("- [Contact](https://example.com/contact)")
#         st.markdown("- [Blog](https://example.com/blog)")
    
#     with col2:
#         st.markdown("### Support")
#         st.markdown("- [Documentation](https://example.com/docs)")
#         st.markdown("- [API Status](https://example.com/status)")
#         st.markdown("- [Help Center](https://example.com/help)")
    
#     with col3:
#         st.markdown("### Legal")
#         st.markdown("- [Terms of Service](https://example.com/terms)")
#         st.markdown("- [Privacy Policy](https://example.com/privacy)")
#         st.markdown("- [Cookie Policy](https://example.com/cookies)")
    
#     st.markdown(
#         "<div style='text-align: center; margin-top: 2rem;'>"
#         "© 2025 Email Pattern Verifier. All rights reserved."
#         "</div>",
#         unsafe_allow_html=True
#     )
# frontend/components/footer.py
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))
import streamlit as st

def render_footer():
    st.markdown("---")
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f8f9fa;
            padding: 1rem;
            text-align: center;
            font-size: 0.8rem;
            border-top: 1px solid #ddd;
        }
        </style>
        <div class='footer'>
            © 2025 Email Pattern Verifier | 
            <a href="https://example.com/privacy">Privacy Policy</a> | 
            <a href="https://example.com/terms">Terms of Service</a>
        </div>
    """, unsafe_allow_html=True)
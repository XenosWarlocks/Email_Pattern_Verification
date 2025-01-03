# pages/payment.py
import streamlit as st
import time
from pathlib import Path
import sys
# frontend_path = Path(__file__).parent.parent
# sys.path.append(str(frontend_path))

# # Must be the first Streamlit command
# st.set_page_config(page_title="Payment - Email Verifier", layout="wide")

def display_order_summary(plan_data):
    st.markdown("### Order Summary")
    st.info(f"""
        **Plan:** {plan_data['plan'].title()} Plan\n
        **Billing Period:** {plan_data['billing']}\n
        **Total Amount:** ${plan_data['price']:.2f}
    """)

def handle_payment_success():
    # Show success message
    st.success("Payment successful! You will receive a confirmation email shortly.")
    st.balloons()
    
    # Clear the selected plan from session state
    st.session_state.selected_plan = None
    
    # Success message container
    st.info("""
        ### 🎉 Welcome aboard!
        Your account has been activated and you can start using our services right away.
        Check your email for login credentials and next steps.
    """)
    
    if st.button("Go to Dashboard"):
        st.switch_page("pages/dashboard.py")

def main():
    # Check if we have a selected plan
    if 'selected_plan' not in st.session_state or not st.session_state.selected_plan:
        st.error("No plan selected. Please choose a plan first.")
        if st.button("Return to Pricing"):
            st.switch_page("pages/pricing.py")
        st.stop()

    plan_data = st.session_state.selected_plan

    # Payment form
    st.title("Complete Your Purchase")

    # Order summary
    display_order_summary(plan_data)

    # Payment form
    with st.form("payment_form"):
        # Billing information
        st.subheader("Billing Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        email = st.text_input("Email Address")
        
        # Payment information
        st.subheader("Payment Information")
        card_number = st.text_input("Card Number")
        col1, col2, col3 = st.columns(3)
        with col1:
            expiry = st.text_input("Expiry (MM/YY)")
        with col2:
            cvv = st.text_input("CVV", type="password")
        with col3:
            zip_code = st.text_input("ZIP Code")
        
        # Terms and conditions
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        # Submit button
        submitted = st.form_submit_button("Complete Purchase", type="primary")
        
        if submitted:
            if not terms:
                st.error("Please agree to the Terms of Service and Privacy Policy")
                st.stop()
                
            # Show processing message
            with st.spinner("Processing your payment..."):
                time.sleep(2)  # Simulate payment processing
            
            handle_payment_success()

if __name__ == "__main__":
    main()
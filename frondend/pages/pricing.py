# pages/pricing.py
import streamlit as st
from pathlib import Path
import sys
# frontend_path = Path(__file__).parent.parent
# sys.path.append(str(frontend_path))

# # Must be the first Streamlit command
# st.set_page_config(page_title="Pricing - Email Verifier", layout="wide")

def load_pricing_data():
    """Load pricing plans data"""
    return {
        "starter": {
            "name": "Starter",
            "price": 49,
            "features": [
                "Up to 1,000 verifications/month",
                "Basic API access",
                "Email support",
                "Standard processing speed",
                "Basic analytics"
            ],
            "highlight_features": ["1,000 verifications/month"],
        },
        "professional": {
            "name": "Professional",
            "price": 99,
            "features": [
                "Up to 10,000 verifications/month",
                "Full API access",
                "Priority support",
                "Enhanced processing speed",
                "Advanced analytics"
            ],
            "highlight_features": ["10,000 verifications/month", "Priority support"],
            "popular": True
        },
        "enterprise": {
            "name": "Enterprise",
            "price": 249,
            "features": [
                "Unlimited verifications",
                "Custom API solutions",
                "24/7 dedicated support",
                "Maximum processing speed",
                "Custom analytics"
            ],
            "highlight_features": ["Unlimited verifications", "24/7 support"],
        }
    }

def display_plan_card(plan_data):
    st.markdown(f"### {plan_data['name']}")
    
    # Price display
    st.markdown(f"#### ${plan_data['price']}/month")
    
    # Popular badge if applicable
    if plan_data.get("popular"):
        st.markdown("🌟 **Most Popular**")
    
    # Features
    for feature in plan_data['features']:
        if feature in plan_data['highlight_features']:
            st.markdown(f"**✨ {feature}**")
        else:
            st.markdown(f"✓ {feature}")

def main():
    # Initialize session state for selected plan
    if 'selected_plan' not in st.session_state:
        st.session_state.selected_plan = None

    # Header
    st.title("Choose Your Plan")
    st.markdown("---")

    # Load pricing data
    pricing_data = load_pricing_data()

    # Main content layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Display pricing cards in tabs
        tabs = st.tabs([plan_data["name"] for plan_data in pricing_data.values()])
        for tab, (plan_id, plan_data) in zip(tabs, pricing_data.items()):
            with tab:
                display_plan_card(plan_data)

    with col2:
        # Plan selection container
        st.markdown("### Select Your Plan")
        
        # Plan dropdown
        selected_plan = st.selectbox(
            "Choose a plan:",
            options=list(pricing_data.keys()),
            format_func=lambda x: f"{pricing_data[x]['name']} (${pricing_data[x]['price']}/month)"
        )
        
        # Billing period selection
        billing_period = st.selectbox(
            "Billing period:",
            options=["Monthly", "Annual (Save 20%)"],
        )
        
        # Calculate total price
        base_price = pricing_data[selected_plan]["price"]
        total_price = base_price * 12 * 0.8 if "Annual" in billing_period else base_price
        
        # Display total
        st.markdown("### Total Price")
        st.markdown(f"### ${total_price:.2f} {'/ year' if 'Annual' in billing_period else '/ month'}")
        
        # Proceed to payment button
        if st.button("Proceed to Payment", type="primary"):
            st.session_state.selected_plan = {
                "plan": selected_plan,
                "billing": billing_period,
                "price": total_price
            }
            st.switch_page("pages/payment.py")

    # FAQ Section
    st.markdown("---")
    st.markdown("## Frequently Asked Questions")

    faqs = {
        "What's included in the verification count?": """
            - Each email pattern checked counts as one verification
            - Bulk uploads are counted per email
            - Failed verifications are not counted
            - Test verifications are free
        """,
        "Can I change plans anytime?": """
            Yes! You can upgrade or downgrade your plan at any time:
            - Upgrades take effect immediately
            - Downgrades take effect at the end of billing cycle
            - Unused verifications don't roll over
        """,
        "Do you offer a free trial?": """
            Yes! We offer a 14-day free trial on all plans:
            - No credit card required
            - Full access to features
            - 100 free verifications
            - Convert to paid plan anytime
        """
    }

    for question, answer in faqs.items():
        with st.expander(question):
            st.markdown(answer)

if __name__ == "__main__":
    main()
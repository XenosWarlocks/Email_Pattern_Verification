# frontend/pages/dashboard.py
import sys
from pathlib import Path
frontend_path = Path(__file__).parent.parent
sys.path.append(str(frontend_path))
import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_sample_data():
    # Generate sample data for demonstration
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    data = {
        'date': dates,
        'verifications': np.random.randint(100, 1000, size=len(dates)),
        'success_rate': np.random.uniform(0.95, 1.00, size=len(dates)),
        'api_usage': np.random.uniform(0.3, 0.8, size=len(dates)),
        'error_rate': np.random.uniform(0.01, 0.05, size=len(dates))
    }
    return pd.DataFrame(data)

def main():
    st.markdown("## Dashboard")
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Generate sample data
    df = generate_sample_data()
    
    # Key metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Verifications",
            f"{df['verifications'].sum():,}",
            f"{df['verifications'].diff().mean():.1f}/day"
        )
    
    with col2:
        avg_success = df['success_rate'].mean() * 100
        st.metric(
            "Success Rate",
            f"{avg_success:.1f}%",
            f"{(df['success_rate'].iloc[-1] - df['success_rate'].iloc[0]) * 100:.1f}%"
        )
    
    with col3:
        avg_api = df['api_usage'].mean() * 100
        st.metric(
            "API Usage",
            f"{avg_api:.1f}%",
            f"{(df['api_usage'].iloc[-1] - df['api_usage'].iloc[0]) * 100:.1f}%"
        )
    
    with col4:
        avg_error = df['error_rate'].mean() * 100
        st.metric(
            "Error Rate",
            f"{avg_error:.1f}%",
            f"{(df['error_rate'].iloc[-1] - df['error_rate'].iloc[0]) * 100:.1f}%"
        )
    
    # Charts
    st.markdown("### Trends")
    
    # Verifications trend
    fig1 = px.line(
        df,
        x='date',
        y='verifications',
        title='Daily Verifications',
        template='plotly_white'
    )
    fig1.update_traces(line_color='#4CAF50')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Success rate vs Error rate
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['date'],
        y=df['success_rate'] * 100,
        name='Success Rate',
        line=dict(color='#4CAF50')
    ))
    fig2.add_trace(go.Scatter(
        x=df['date'],
        y=df['error_rate'] * 100,
        name='Error Rate',
        line=dict(color='#f44336')
    ))
    fig2.update_layout(
        title='Success vs Error Rate',
        template='plotly_white',
        yaxis_title='Percentage'
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Recent activity
    st.markdown("### Recent Activity")
    activity_data = pd.DataFrame({
        'Timestamp': pd.date_range(end=datetime.now(), periods=5, freq='h')[::-1],
        'Action': ['File Upload', 'API Call', 'Bulk Verification', 'Export Results', 'Settings Update'],
        'Status': ['Success', 'Success', 'Failed', 'Success', 'Success'],
        'Details': ['verified_emails.xlsx', '/api/verify', 'Timeout error', 'export_2024.xlsx', 'Updated API key']
    })
    
    st.dataframe(
        activity_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Timestamp': st.column_config.DatetimeColumn('Timestamp', format='MM/DD/YYYY HH:mm'),
            'Status': st.column_config.Column('Status', help='Operation status')
        }
    )
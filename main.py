# -*- coding: utf-8 -*-

import streamlit as st
import requests
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as ob
from utils import predict
import shap

# Set the page configuration
st.set_page_config(
    page_title="OPTI RECOURSE PRO", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

# Helper function for API prediction
def get_prediction_from_api(payload):
    try:
        response = requests.post(f"{API_BASE_URL}/predict/", json=payload)
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error from API: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}. Make sure the Django server is running.")
        return None

def bulk_predict_api(payload_list):
    try:
        response = requests.post(f"{API_BASE_URL}/bulk-predict/", json=payload_list)
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Bulk API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Bulk Connection error: {e}")
        return None

def get_analytics_api():
    try:
        response = requests.get(f"{API_BASE_URL}/analytics/")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# Helper function to get history
def get_history_from_api():
    try:
        response = requests.get(f"{API_BASE_URL}/history/")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        return []

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background: #f8fafc; }
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem; border-radius: 15px; text-align: center; color: white;
        margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .section-box {
        background: white; padding: 1.5rem; border-radius: 12px;
        margin: 1.5rem 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-top: 4px solid #3b82f6;
    }
    .metric-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        text-align: center; border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .recourse-box {
        background: #eff6ff; border-left: 5px solid #3b82f6;
        padding: 1.5rem; border-radius: 8px; margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>OPTI RECOURSE PRO</h1>
    <p>Enterprise Credit Risk Intelligence & Bulk Analytics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛠️ Dashboard")
    page = st.radio("Select View", ["Single Assessment", "Bulk Assessment", "Analytics Dash", "Assessment History"])
    st.divider()
    st.info("Pro Version: Bulk Upload & Advanced Analytics Enabled")

if page == "Single Assessment":
    st.markdown('<div class="section-box"><h2>👤 Borrower Profile</h2></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", 18, 100, 30)
        income = st.number_input("Annual Income (₹)", 0, 10000000, 500000)
        loan_purpose = st.selectbox("Purpose", ['Education', 'Home', 'Auto', 'Personal'])
    with c2:
        loan_amount = st.number_input("Loan Amount (₹)", 0, 50000000, 1000000)
        tenure = st.slider("Tenure (Months)", 6, 360, 60)
        loan_type = st.radio("Security", ['Secured', 'Unsecured'], horizontal=True)

    st.markdown('<div class="section-box"><h2>📊 Credit Context</h2></div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        utilization = st.slider("Credit Utilization (%)", 0, 100, 30)
    with c4:
        residence = st.selectbox("Residence", ['Owned', 'Rented', 'Mortgage'])

    if st.button("🚀 Run AI Assessment", use_container_width=True):
        payload = {
            "age": age, "income": income, "loan_amount": loan_amount,
            "loan_tenure_months": tenure, "loan_purpose": loan_purpose,
            "loan_type": loan_type, "residence_type": residence,
            "avg_dpd_per_dm": 0, "total_loan_months": 0,
            "credit_utilization_ratio": utilization, "dmtlm": 0
        }
        with st.spinner('Calculating...'):
            res = get_prediction_from_api(payload)
        
        if res:
            m1, m2, m3 = st.columns(3)
            m1.metric("Risk Probability", f"{res['probability']*100:.1f}%")
            m2.metric("Credit Score", res['credit_score'])
            m3.metric("Rating", res['rating'])

            t1, t2 = st.tabs(["🎯 Recourse Strategy", "🔍 Feature Impact"])
            with t1:
                if res['recourse_advice']:
                    st.markdown("### Suggested Path to Improvement")
                    for item in res['recourse_advice']:
                        st.info(f"**{item['feature']}**: {item['advice']} (Target: {item['target_rating']})")
                else:
                    st.success("Profile is in peak condition (Excellent Rating).")
            with t2:
                from components.explanations import display_shap_waterfall
                display_shap_waterfall(res['shap_explanations'])
            
            # Download PDF Report
            from components.pdf_generator import generate_pdf_report
            pdf_bytes = generate_pdf_report(res, payload)
            st.download_button(
                label="📄 Download PDF Credit Report",
                data=bytes(pdf_bytes),
                file_name=f"Credit_Report_{age}_{loan_purpose}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

elif page == "Bulk Assessment":
    st.markdown('<div class="section-box"><h2>📥 Bulk CSV Upload</h2></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Borrower Data (CSV)", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Uploaded Data (First 5 rows):")
        st.dataframe(df.head())
        
        if st.button("⚡ Process Batch Prediction"):
            # Check if required columns exist (simple validation)
            required = ['age', 'income', 'loan_amount', 'loan_tenure_months', 'loan_purpose', 'loan_type', 'residence_type']
            if all(col in df.columns for col in required):
                # Ensure optional columns exist
                for col in ['avg_dpd_per_dm', 'total_loan_months', 'credit_utilization_ratio', 'dmtlm']:
                    if col not in df.columns: df[col] = 0
                
                payload_list = df.to_dict(orient='records')
                with st.spinner(f'Processing {len(payload_list)} records...'):
                    results = bulk_predict_api(payload_list)
                
                if results:
                    st.success(f"Batch completed! {len(results)} records processed.")
                    res_df = pd.DataFrame(results)
                    final_df = pd.concat([df.reset_index(drop=True), res_df], axis=1)
                    st.dataframe(final_df)
                    st.download_button("📥 Download Results", final_df.to_csv(index=False), "risk_results.csv", "text/csv")
            else:
                st.error(f"CSV missing columns. Required: {', '.join(required)}")

elif page == "Analytics Dash":
    st.markdown('<div class="section-box"><h2>📈 Portfolio Intelligence</h2></div>', unsafe_allow_html=True)
    data = get_analytics_api()
    if data:
        # High level KPIs
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Avg Credit Score", int(data['summary']['avg_score'] or 0))
        with k2:
            st.metric("Total Profiles", data['summary']['total_count'])
        with k3:
            st.metric("Avg Income (₹)", f"{int(data['summary']['avg_income'] or 0):,}")
        with k4:
            st.metric("Avg Loan Size (₹)", f"{int(data['summary']['avg_loan'] or 0):,}")
        
        st.divider()
        
        # Row 1: Distribution & Timeline
        col_r1_left, col_r1_right = st.columns(2)
        with col_r1_left:
            st.subheader("🎯 Risk Segmentation")
            df_dist = pd.DataFrame(data['rating_distribution'])
            if not df_dist.empty:
                fig = px.pie(df_dist, values='count', names='rating', hole=.4,
                           color='rating', color_discrete_map={'Excellent':'#10b981', 'Good':'#3b82f6', 'Average':'#f59e0b', 'Poor':'#ef4444'})
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
        
        with col_r1_right:
            st.subheader("📅 Assessment Timeline")
            df_time = pd.DataFrame(data['timeline'])
            if not df_time.empty:
                fig_time = px.area(df_time, x='day', y='count', markers=True, 
                                 title="Daily Volume", color_discrete_sequence=['#3b82f6'])
                fig_time.update_layout(margin=dict(t=30, b=0, l=0, r=0), xaxis_title=None, yaxis_title="Count")
                st.plotly_chart(fig_time, use_container_width=True)

        st.divider()
        
        # Row 2: Purpose & Correlation
        col_r2_left, col_r2_right = st.columns(2)
        with col_r2_left:
            st.subheader("💡 Loan Purpose Analysis")
            df_purpose = pd.DataFrame(data['purpose_distribution'])
            if not df_purpose.empty:
                fig_purp = px.bar(df_purpose, x='loan_purpose', y='count', color='avg_score',
                                labels={'count':'Assessments', 'avg_score':'Avg Score'},
                                color_continuous_scale='Blues', text_auto=True)
                fig_purp.update_layout(margin=dict(t=30, b=0, l=0, r=0))
                st.plotly_chart(fig_purp, use_container_width=True)

        with col_r2_right:
            st.subheader("🔍 Income vs Credit Performance")
            df_scatter = pd.DataFrame(data['scatter_data'])
            if not df_scatter.empty:
                fig_scatter = px.scatter(df_scatter, x='income', y='credit_score', color='rating',
                                       size_max=15, opacity=0.7,
                                       hover_data=['rating'], title="Risk Clusters")
                fig_scatter.update_layout(margin=dict(t=30, b=0, l=0, r=0))
                st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Assessment engine cold. Please run a few profiles to generate intelligence.")

else:
    st.markdown('<div class="section-box"><h2>📜 Assessment History</h2></div>', unsafe_allow_html=True)
    history = get_history_from_api()
    if history:
        df_h = pd.DataFrame(history)
        st.dataframe(df_h[['created_at', 'income', 'loan_amount', 'credit_score', 'rating']], use_container_width=True)
        st.download_button("📥 Download Assessment History (CSV)", df_h.to_csv(index=False), "assessment_history.csv", "text/csv")
    else:
        st.info("No assessments recorded.")

# Footer
st.markdown('<div style="margin-top: 5rem; text-align: center; color: #94a3b8;">© 2026 OPTI RECOURSE AI | Advanced Risk Management Module</div>', unsafe_allow_html=True)

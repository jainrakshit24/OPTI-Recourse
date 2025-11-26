# -*- coding: utf-8 -*-
"""
Enhanced Credit Risk Modeling Application - Beautiful Boxy Minimal Version
@author: Admin
"""

import streamlit as st
from utils import predict

# Set the page configuration
st.set_page_config(
    page_title="OPTI RECOURSE", 
    page_icon="💰", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful boxy minimal design with pastel colors
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(to bottom right, #fef6fb, #f0f4ff);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Main header box */
    .main-header {
        background: linear-gradient(135deg, #c9a0dc 0%, #a8b5ff 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(169, 160, 220, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Section header boxes */
    .section-box {
        background: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #c9a0dc;
    }
    
    .section-box h2 {
        color: #4a4a68;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #fff8f0;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #ffbe98;
        box-shadow: 0 2px 10px rgba(255, 190, 152, 0.15);
    }
    
    .info-box p {
        color: #6b5d4f;
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Input container boxes */
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .input-container:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    /* Input fields styling */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        border: 2px solid #e8e4f3 !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        background: #fafbff !important;
        color: #4a4a68 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus {
        border-color: #c9a0dc !important;
        background: white !important;
        box-shadow: 0 0 0 3px rgba(201, 160, 220, 0.1) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e8e4f3 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: #fafbff !important;
        border-radius: 10px !important;
        color: #4a4a68 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: #c9a0dc !important;
    }
    
    .stSlider > div > div > div {
        background: #e8e4f3 !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stRadio > div > label {
        background: #fafbff !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 8px !important;
        margin: 0.3rem !important;
        border: 2px solid #e8e4f3 !important;
        color: #4a4a68 !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #c9a0dc !important;
        background: white !important;
    }
    
    /* Labels */
    label {
        color: #4a4a68 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #c9a0dc 0%, #a8b5ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 8px 25px rgba(169, 160, 220, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(169, 160, 220, 0.5) !important;
    }
    
    /* Result cards - Beautiful boxy design */
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.08);
        border-top: 5px solid;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .result-card h3 {
        color: #6b6b8a;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    .result-card h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .result-card p {
        color: #9999b3;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Individual card colors */
    .risk-card {
        border-top-color: #ffb3ba;
        background: linear-gradient(to bottom, #fff5f6, white);
    }
    .risk-card h1 { color: #ff6b7a; }
    
    .score-card {
        border-top-color: #bae1c2;
        background: linear-gradient(to bottom, #f5fef6, white);
    }
    .score-card h1 { color: #52c76e; }
    
    .rating-card {
        border-top-color: #c9a0dc;
        background: linear-gradient(to bottom, #fbf7fe, white);
    }
    .rating-card h1 { color: #9370db; }
    
    /* Warning and success boxes */
    .custom-warning {
        background: white;
        border-left: 5px solid #ffb3ba;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(255, 179, 186, 0.2);
    }
    
    .custom-warning h3 {
        color: #d63447;
        margin-top: 0;
        font-weight: 600;
    }
    
    .custom-warning p, .custom-warning li {
        color: #6b5d5d;
    }
    
    .custom-success {
        background: white;
        border-left: 5px solid #bae1c2;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(186, 225, 194, 0.2);
    }
    
    .custom-success h3 {
        color: #2d8a4e;
        margin-top: 0;
        font-weight: 600;
    }
    
    .custom-success p, .custom-success li {
        color: #5d6b5d;
    }
    
    /* Score explanation box */
    .score-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 6px 30px rgba(0, 0, 0, 0.08);
    }
    
    .score-box h3 {
        color: #4a4a68;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    .score-item {
        background: #fafbff;
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 4px solid;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }
    
    .score-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
    }
    
    .score-item:nth-child(1) { border-left-color: #bae1c2; }
    .score-item:nth-child(2) { border-left-color: #ffffba; }
    .score-item:nth-child(3) { border-left-color: #ffd8b3; }
    .score-item:nth-child(4) { border-left-color: #ffb3ba; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #fef6fb, #f8f9ff) !important;
    }
    
    .sidebar-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-box h2 {
        color: #4a4a68;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .sidebar-box ol {
        color: #6b6b8a;
        padding-left: 1.5rem;
        line-height: 2;
    }
    
    /* Footer box */
    .footer-box {
        background: linear-gradient(135deg, #6b6b8a 0%, #8a8aa8 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
        box-shadow: 0 6px 30px rgba(107, 107, 138, 0.3);
    }
    
    .footer-box h4 {
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    
    .footer-box p {
        font-weight: 300;
        opacity: 0.9;
        margin: 0.3rem 0;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #4a4a68 !important;
    }
    
    /* Captions */
    .stCaptionContainer {
        color: #9999b3 !important;
        font-weight: 500 !important;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>OPTI RECOURSE</h1>
    <p>Smart Credit Risk Assessment Platform</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-box">
        <h2>📋 Quick Guide</h2>
        <ol>
            <li>Fill personal details</li>
            <li>Enter loan information</li>
            <li>Add credit history</li>
            <li>Get instant results</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.image("project-root/logo.png", width=180)
    except:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #c9a0dc 0%, #a8b5ff 100%); 
                    color: white; padding: 2.5rem; border-radius: 15px; text-align: center;
                    box-shadow: 0 4px 20px rgba(169, 160, 220, 0.3);">
            <h1 style="margin: 0; font-size: 3rem;">🏦</h1>
        </div>
        """, unsafe_allow_html=True)

# Personal Information Section
st.markdown("""
<div class="section-box">
    <h2>👤 Personal Information</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age", 
        min_value=18, 
        max_value=100, 
        value=28,
        help="Your current age"
    )

with col2:
    income = st.number_input(
        "Annual Income (₹)", 
        min_value=0, 
        max_value=5000000, 
        value=290875, 
        step=10000,
        help="Total yearly income"
    )

# Loan Requirements Section
st.markdown("""
<div class="section-box">
    <h2>💰 Loan Requirements</h2>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    loan_amount = st.number_input(
        "Loan Amount (₹)", 
        min_value=0, 
        value=256000, 
        step=10000,
        help="Amount you want to borrow"
    )

with col4:
    loan_tenure_months = st.slider(
        "Repayment Period (Months)", 
        min_value=6, 
        max_value=240, 
        step=6, 
        value=36,
        help="Duration to repay the loan"
    )
    st.caption(f"📅 {loan_tenure_months//12} years, {loan_tenure_months%12} months")

# Loan-to-Income insight
if income > 0:
    lti = loan_amount / income
    if lti <= 3:
        st.success(f"✅ Excellent ratio: {lti:.1f}x your income")
    elif lti <= 5:
        st.warning(f"⚠️ Moderate ratio: {lti:.1f}x your income")
    else:
        st.error(f"❌ High ratio: {lti:.1f}x your income")

# Loan Details Section
st.markdown("""
<div class="section-box">
    <h2>🎯 Loan Details</h2>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    loan_purpose = st.selectbox(
        "Purpose",
        ['Education', 'Home', 'Auto', 'Personal'],
        help="What will you use the loan for?"
    )

with col6:
    loan_type = st.radio(
        "Security Type",
        ['Secured', 'Unsecured'],
        help="Secured = with collateral | Unsecured = without collateral",
        horizontal=True
    )

residence_type = st.selectbox(
    "Residence Status",
    ['Owned', 'Rented', 'Mortgage'],
    help="Your current living situation"
)

# Credit History Section
st.markdown("""
<div class="section-box">
    <h2>📊 Credit History</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <p>💡 <strong>First-time borrower?</strong> Leave these fields at 0</p>
</div>
""", unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    avg_dpd_per_dm = st.number_input(
        "Average Days Late", 
        min_value=0, 
        value=0,
        help="Average delay in previous loan payments"
    )

with col8:
    total_loan_months = st.number_input(
        "Previous Loan Duration (Months)", 
        min_value=0, 
        value=0,
        help="Total months of all previous loans"
    )

col9, col10 = st.columns(2)

with col9:
    credit_utilization_ratio = st.slider(
        "Credit Card Usage (%)", 
        min_value=0, 
        max_value=100, 
        value=0,
        help="Percentage of credit limit used"
    )

with col10:
    dmtlm = st.slider(
        "Late Payment Rate (%)", 
        min_value=0, 
        max_value=100, 
        value=0,
        help="Percentage of months with late payments"
    )

# Calculate Button
st.markdown("<br>", unsafe_allow_html=True)
col_button = st.columns([1, 1, 1])

with col_button[1]:
    calculate_button = st.button("🚀 Calculate Risk Score", use_container_width=True)

# Results Section
if calculate_button:
    with st.spinner('Analyzing your profile...'):
        probability, credit_score, rating = predict(
            age, avg_dpd_per_dm, credit_utilization_ratio, dmtlm, income,
            loan_amount, loan_tenure_months, total_loan_months,
            loan_purpose, loan_type, residence_type
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Results Display
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        risk_percentage = probability * 100
        st.markdown(f"""
        <div class="result-card risk-card">
            <h3>Default Risk</h3>
            <h1>{risk_percentage:.1f}%</h1>
            <p>Lower is better</p>
        </div>
        """, unsafe_allow_html=True)
    
    with result_col2:
        st.markdown(f"""
        <div class="result-card score-card">
            <h3>Credit Score</h3>
            <h1>{credit_score}</h1>
            <p>Higher is better</p>
        </div>
        """, unsafe_allow_html=True)
    
    with result_col3:
        st.markdown(f"""
        <div class="result-card rating-card">
            <h3>Rating</h3>
            <h1>{rating}</h1>
            <p>Overall assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendations
    if rating in ['Poor', 'Average']:
        st.markdown("""
        <div class="custom-warning">
            <h3>⚠️ Improvement Needed</h3>
            <p><strong>Your application needs strengthening.</strong></p>
            <p><strong>Recommendations:</strong></p>
            <ul>
                <li>Pay all bills on time consistently</li>
                <li>Consider requesting a lower loan amount</li>
                <li>Clear outstanding debts if any</li>
                <li>Opt for secured loan with collateral</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="custom-success">
            <h3>✅ Strong Application</h3>
            <p><strong>Your profile looks excellent!</strong></p>
            <p><strong>Benefits you can expect:</strong></p>
            <ul>
                <li>High approval probability</li>
                <li>Competitive interest rates</li>
                <li>Faster processing time</li>
                <li>Flexible repayment options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Score explanation
    st.markdown("""
    <div class="score-box">
        <h3>Understanding Credit Scores</h3>
        <div class="score-item">
            <span style="font-size: 2rem;">🟢</span>
            <div style="flex: 1;">
                <strong style="color: #2d8a4e; font-size: 1.1rem;">750-850: Excellent</strong><br>
                <small style="color: #6b8a6b;">Best rates, premium services</small>
            </div>
        </div>
        <div class="score-item">
            <span style="font-size: 2rem;">🟡</span>
            <div style="flex: 1;">
                <strong style="color: #d4a017; font-size: 1.1rem;">650-749: Good</strong><br>
                <small style="color: #8a8a6b;">Competitive rates available</small>
            </div>
        </div>
        <div class="score-item">
            <span style="font-size: 2rem;">🟠</span>
            <div style="flex: 1;">
                <strong style="color: #d97706; font-size: 1.1rem;">550-649: Fair</strong><br>
                <small style="color: #8a7a6b;">Standard rates apply</small>
            </div>
        </div>
        <div class="score-item">
            <span style="font-size: 2rem;">🔴</span>
            <div style="flex: 1;">
                <strong style="color: #d63447; font-size: 1.1rem;">Below 550: Needs Work</strong><br>
                <small style="color: #8a6b6b;">Limited options, focus on improvement</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-box">
    <h4>OPTI RECOURSE</h4>
    <p>Powered by Advanced AI | Secure & Confidential</p>
    <p style="font-size: 0.85rem; margin-top: 1rem;">Created by Rakshit Jain</p>
</div>
""", unsafe_allow_html=True)

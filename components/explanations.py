import streamlit as st
import plotly.graph_objects as go
from annotated_text import annotated_text

def display_shap_waterfall(shap_explanations):
    """
    Displays a horizontal bar chart of SHAP values using Plotly.
    """
    features = [x[0].replace('_', ' ').title() for x in shap_explanations[:10]]
    values = [x[1] for x in shap_explanations[:10]]
    
    # Sort for best display in bar chart (impactful at top)
    # Reversing because Plotly bars are plotted bottom to top by default
    features.reverse()
    values.reverse()
    
    colors = ['#ff6b7a' if v > 0 else '#52c76e' for v in values]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=features,
        orientation='h',
        marker_color=colors,
        text=[f"{v:.4f}" for v in values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Top 10 Factors Influencing Your Risk Score",
        xaxis_title="Impact (Positive = More Risk, Negative = Less Risk)",
        yaxis_title="Feature",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif")
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_factor_insights(shap_explanations):
    """
    Displays textual insights based on SHAP values using annotated text.
    """
    st.markdown("### 🔍 Key Insights")
    
    top_pos = [x for x in shap_explanations if x[1] > 0][:2]
    top_neg = [x for x in shap_explanations if x[1] < 0][:2]
    
    st.write("Factors **increasing** your risk:")
    if top_pos:
        items = []
        for feat, val in top_pos:
            items.append((feat.replace('_', ' ').title(), "Warning", "#ffb3ba"))
            items.append(" ")
        annotated_text(*items)
    else:
        st.write("None significant")
        
    st.write("Factors **decreasing** your risk:")
    if top_neg:
        items = []
        for feat, val in top_neg:
            items.append((feat.replace('_', ' ').title(), "Excellent", "#bae1c2"))
            items.append(" ")
        annotated_text(*items)
    else:
        st.write("None significant")

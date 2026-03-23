from fpdf import FPDF
import base64
from datetime import datetime

class CreditReport(FPDF):
    def header(self):
        self.set_fill_color(201, 160, 220) # Pastel purple
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'OPTI RECOURSE', ln=True, align='C')
        self.set_font('helvetica', 'I', 12)
        self.cell(0, 10, 'Credit Risk Assessment Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_pdf_report(results, input_params):
    pdf = CreditReport()
    pdf.add_page()
    
    # Summary Section
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(74, 74, 104)
    pdf.cell(0, 15, '1. Assessment Summary', ln=True)
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(50, 10, 'Credit Score:', 0)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f'{results["credit_score"]}', ln=True)
    
    pdf.set_font('helvetica', '', 12)
    pdf.cell(50, 10, 'Risk Rating:', 0)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f'{results["rating"]}', ln=True)
    
    pdf.set_font('helvetica', '', 12)
    pdf.cell(50, 10, 'Default Probability:', 0)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f'{results["probability"]*100:.2f}%', ln=True)
    
    pdf.ln(10)
    
    # Input Data Section
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(74, 74, 104)
    pdf.cell(0, 15, '2. Borrower Information', ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    col_width = 90
    for key, val in input_params.items():
        pdf.cell(col_width, 8, f'{key.replace("_", " ").title()}: {val}', border=1)
        if pdf.get_x() > 150:
            pdf.ln(8)
    
    if pdf.get_x() > 20:
        pdf.ln(15)
    else:
        pdf.ln(7)

    # Key Factors (SHAP)
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(74, 74, 104)
    pdf.cell(0, 15, '3. Top Influencing Factors', ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    
    top_5 = results['shap_explanations'][:5]
    for feat, impact in top_5:
        impact_dir = "Reduces Score" if impact > 0 else "Increases Score" # In default prob terms, positive impact = higher prob = lower score
        # Note: SHAP values for default probability: positive = higher risk.
        feat_name = feat.replace('_', ' ').title()
        pdf.cell(0, 8, f'- {feat_name}: {impact_dir}', ln=True)

    pdf.ln(10)
    
    # Recommendation Section
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(74, 74, 104)
    pdf.cell(0, 15, '4. Advice', ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    if results['rating'] in ['Poor', 'Average']:
        advice = "Your application needs strengthening. Consider paying all bills on time, reducing your loan amount, or providing collateral for a secured loan."
    else:
        advice = "Your profile looks excellent! You can expect high approval probability and competitive interest rates."
    
    pdf.multi_cell(0, 8, advice)
    
    return pdf.output(dest='S') # Return as string (bytes)

def get_pdf_download_link(results, input_params):
    pdf_bytes = generate_pdf_report(results, input_params)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Credit_Assessment_Report.pdf" style="text-decoration: none;"><button style="background-color: #c9a0dc; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">📥 Download PDF Report</button></a>'
    return href

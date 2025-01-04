from fpdf import FPDF
import os

def generate_report(data_path, output_folder):
    report_path = os.path.join(output_folder, 'report.pdf')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Student Performance Analysis Report", ln=True, align='C')
    pdf.set_font('Arial', size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Data Source: {data_path}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Visualizations included in static/plots", ln=True)
    pdf.output(report_path)
    return report_path

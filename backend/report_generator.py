from fpdf import FPDF
import os

class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    def generate_pdf(self, session_data: dict):
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "NeuroUX - UI Intelligence Report", 0, 1, "C")
        pdf.ln(10)

        # Session Info
        pdf.set_font("Arial", "B", 12)
        pdf.cell(190, 10, f"Analysis ID: {session_data['id']}", 0, 1)
        # Handle datetime if it's an object or string
        date_str = session_data['created_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(session_data['created_at'], 'strftime') else str(session_data['created_at'])
        pdf.cell(190, 10, f"Date: {date_str}", 0, 1)
        pdf.ln(5)

        # Metrics
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "UX Metrics", 0, 1)
        pdf.set_font("Arial", "", 12)
        pdf.cell(95, 10, f"CFI: {session_data['cfi_score']:.2f}", 1)
        pdf.cell(95, 10, f"VCS: {session_data['vcs_score']:.2f}", 1, 1)
        pdf.cell(95, 10, f"IFS: {session_data['ifs_score']:.2f}", 1)
        pdf.cell(95, 10, f"DDP: {session_data['ddp_score']:.2f}", 1, 1)
        pdf.cell(190, 10, f"UX Intelligence Score: {session_data['ux_intelligence_score']:.2f}", 1, 1)
        pdf.ln(10)

        # Recommendations
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Recommendations", 0, 1)
        pdf.set_font("Arial", "", 11)
        for rec in session_data["recommendations"]:
            # Handle object (Pydantic/ORM) or dict
            rec_text = rec.text if hasattr(rec, 'text') else rec['text']
            rec_severity = rec.severity if hasattr(rec, 'severity') else rec['severity']
            pdf.multi_cell(190, 10, f"[{rec_severity}] {rec_text}", 1)
        
        output_path = os.path.join(self.output_dir, f"report_{session_data['id']}.pdf")
        pdf.output(output_path)
        return output_path

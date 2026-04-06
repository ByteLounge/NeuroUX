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
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(31, 41, 55) # Dark gray
        pdf.cell(190, 20, "NeuroUX - UI Intelligence Report", 0, 1, "C")
        pdf.ln(5)

        # Header Line
        pdf.set_draw_color(79, 70, 229) # Indigo
        pdf.set_line_width(1)
        pdf.line(10, 35, 200, 35)
        pdf.ln(10)

        # Session Info
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(107, 114, 128) # Light gray
        pdf.cell(95, 8, f"Analysis ID: {session_data['id']}", 0, 0)
        date_str = session_data['created_at'].strftime("%Y-%m-%d %H:%M:%S") if hasattr(session_data['created_at'], 'strftime') else str(session_data['created_at'])
        pdf.cell(95, 8, f"Date: {date_str}", 0, 1, "R")
        pdf.ln(10)

        # Metrics Section
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(190, 10, "UX Cognitive Metrics", 0, 1)
        pdf.ln(5)

        # Metric Box Styling
        def draw_metric(label, score, x, y):
            pdf.set_xy(x, y)
            pdf.set_fill_color(249, 250, 251) # Very light gray
            pdf.rect(x, y, 90, 20, 'F')
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(107, 114, 128)
            pdf.text(x + 5, y + 7, label)
            pdf.set_font("Arial", "B", 14)
            pdf.set_text_color(31, 41, 55)
            pdf.text(x + 5, y + 16, f"{score:.2f}")

        draw_metric("Cognitive Friction Index (CFI)", session_data['cfi_score'], 10, 70)
        draw_metric("Visual Competition Score (VCS)", session_data['vcs_score'], 105, 70)
        draw_metric("Interaction Fatigue Score (IFS)", session_data['ifs_score'], 10, 95)
        draw_metric("Decision Delay Prob. (DDP)", session_data['ddp_score'], 105, 95)
        
        pdf.set_xy(10, 120)
        pdf.set_fill_color(238, 242, 255) # Light indigo
        pdf.rect(10, 120, 185, 25, 'F')
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(79, 70, 229)
        pdf.text(15, 128, "Overall UX Intelligence Score")
        pdf.set_font("Arial", "B", 20)
        pdf.text(15, 140, f"{session_data['ux_intelligence_score']:.2f} / 100.00")
        
        pdf.ln(45)

        # Recommendations Section
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(190, 10, "Design Recommendations", 0, 1)
        pdf.ln(5)

        for rec in session_data["recommendations"]:
            rec_text = rec.text if hasattr(rec, 'text') else rec['text']
            rec_severity = rec.severity if hasattr(rec, 'severity') else rec['severity']
            
            # Severity color coding
            if rec_severity == "High":
                bg_color = (254, 242, 242)
                text_color = (153, 27, 27)
                border_color = (252, 165, 165)
            elif rec_severity == "Medium":
                bg_color = (255, 251, 235)
                text_color = (146, 64, 14)
                border_color = (253, 230, 138)
            elif rec_severity == "Success":
                bg_color = (240, 253, 244)
                text_color = (22, 101, 52)
                border_color = (187, 247, 208)
            else: # Info
                bg_color = (240, 249, 255)
                text_color = (7, 89, 133)
                border_color = (186, 230, 253)

            pdf.set_fill_color(*bg_color)
            pdf.set_draw_color(*border_color)
            pdf.set_text_color(*text_color)
            
            current_y = pdf.get_y()
            pdf.set_font("Arial", "B", 9)
            pdf.cell(190, 6, f" {rec_severity.upper()} PRIORITY", 1, 1, 'L', True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(190, 8, f" {rec_text}", 1, 'L', True)
            pdf.ln(4)
        
        output_path = os.path.join(self.output_dir, f"report_{session_data['id']}.pdf")
        pdf.output(output_path)
        return output_path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import io

#def embedpdf(pdf_path, qr_path, output_path):
#    
#    chipi = canvas.Canvas(output_path, pagesize=letter)
#    chipi.drawImage(qr_path, 450, 50, width=100, height=100)
#    chipi.drawString(50, 700, "Certificate")
#    chipi.save

def embedpdf(pdf_path, qr_path, output_path):
    
    qr_temp = io.BytesIO()
    qr_canvas = canvas.Canvas(qr_temp, pagesize=letter)
    qr_canvas.drawImage(qr_path, 450, 50, width=100, height=100)
    qr_canvas.save()
    qr_temp.seek(0)

    
    original_pdf = PdfReader(pdf_path)
    qr_overlay = PdfReader(qr_temp)

    writer = PdfWriter()

    
    page = original_pdf.pages[0]
    page.merge_page(qr_overlay.pages[0])
    writer.add_page(page)

    
    with open(output_path, "wb") as f:
        writer.write(f)

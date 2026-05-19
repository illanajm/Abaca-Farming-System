from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_farmer_pdf(farmer, farms):
    filename = f"farmer_{farmer.id}_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "FARMER OFFICIAL REPORT")

    y -= 40
    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Name: {farmer.firstname} {farmer.middlename} {farmer.lastname}")
    y -= 20
    c.drawString(50, y, f"Age: {farmer.age}")
    y -= 20
    c.drawString(50, y, f"Barangay: {farmer.barangay}")
    y -= 20
    c.drawString(50, y, f"Years in Farming: {farmer.years_in_farming}")

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "FARM DETAILS")

    y -= 20
    c.setFont("Helvetica", 12)

    for f in farms:
        c.drawString(50, y, f"- Area: {f.farm_area}, Soil: {f.soil_type}, Yield: {f.average_yield}")
        y -= 20

    c.save()
    return filename
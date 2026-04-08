from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.contrib.auth.decorators import login_required
from .models import Invoice


@login_required
def download_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)

    data = []

    
    data.append(["INVOICE DETAILS", ""])

    
    data.append(["Invoice ID", f"INV-2026-{str(invoice.id).zfill(4)}"])
    data.append(["Student", invoice.enrollment.student.first_name])
    data.append(["Course", invoice.enrollment.course.title])
    data.append(["Enrollment Date", str(invoice.enrollment.enrollment_date)])

    
    data.append(["", ""])

    data.append(["Description", "Amount (₹)"])

    data.append(["Course Fee", str(invoice.base_amount)])
    data.append(["GST (18%)", str(invoice.gst_amount)])
    data.append(["Total Amount", str(invoice.total_amount)])

    table = Table(data, colWidths=[250, 250])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('SPAN', (0, 0), (1, 0)),

        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor("#e2e8f0")),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),

        ('BACKGROUND', (0, 8), (-1, 8), colors.HexColor("#dcfce7")),
    ])

    table.setStyle(style)

    elements = [table]

    doc.build(elements)

    return response

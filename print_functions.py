from docxtpl import DocxTemplate
from docx2pdf import convert
import os


def create_template(data=None):
    id = 1
    product_data = [{
        "i": 1,
        "product_name": "Shirt",
        "quant": "1",
        "rate": "200",
        "item_total": "200"
    }, {
        "i": "",
        "product_name": "Pant",
        "quant": "2",
        "rate": "100",
        "item_total": "200"
    }, {
        "i": "",
        "product_name": "Lift",
        "quant": "1",
        "rate": "320",
        "item_total": "320"
    }
    ]

    context = {
        "date": "27-10-2023",
        "id": "1",
        "customer_name": "Kyle P",
        "customer_address": "Some Random Address",
        "customer_state": "Karnataka",
        "customer_phone": "8730266044",
        "product_data": product_data,
        "total": "3300"
    }

    template = DocxTemplate("Invoice.docx")

    # Render the template with the context data
    template.render(context)

    # Save the generated document to a new file
    template.save("invoices/invoice_1.docx")
    convert("invoices/invoice_1.docx", f"invoices/invoice.pdf")
    os.remove(f"invoices/invoice.docx")


create_template()

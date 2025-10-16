from fpdf import FPDF
import random
import os

# --- Step 1: Generate 200 dummy queries ---
base_queries = [
    "Raise a ticket with id {}",
    "Order the product with given product id {}",
    "Send email to {} by saying your order has been successfully placed",
    "I want my refund",
    "Customer support",
    "After how many days refund gets issued?",
    "How to update billing information?",
    "Contact customer support"
]

emails = ["user{}@example.com".format(i) for i in range(50)]
product_ids = list(range(1, 51))
ticket_ids = list(range(1000, 1050))

dummy_queries = []

for _ in range(200):
    template = random.choice(base_queries)
    if "{}" in template:
        if "ticket" in template:
            q = template.format(random.choice(ticket_ids))
        elif "product" in template:
            q = template.format(random.choice(product_ids))
        elif "email" in template:
            q = template.format(random.choice(emails))
    else:
        q = template
    dummy_queries.append(q)

# --- Step 2: Create a single PDF ---
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for idx, query in enumerate(dummy_queries, start=1):
    pdf.multi_cell(0, 10, f"{idx}. {query}")  # number each query
    pdf.ln(1)  # small line break

# Save PDF
os.makedirs("pdf_docs", exist_ok=True)
pdf_file = "pdf_docs/all_queries.pdf"
pdf.output(pdf_file)

print(f"✅ Created single PDF with all queries: '{pdf_file}'")

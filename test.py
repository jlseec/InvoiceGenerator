from generate_invoice import generate_invoice

# ==============================
# TEST INVOICE DATA
# ==============================
invoice = {
    "invoice_type": 2, 
    "invoice_no": "Testpy20633",
    "date": "4 Jan 2026",
    "customer": "Testing Group",
    "attn": "Gail Peterson",
    "email": "test@email.com",
    "items": [
        {"item": "1601 Black / Blue", "description": "Dress", "qty": 325, "unit_price": 50.50},
        {"item": "1602 Silver / Black", "description": "Skirt", "qty": 300, "unit_price": 87.50},
        {"item": "1603 Black", "description": "Top", "qty": 90, "unit_price": 46.20},
        {"item": "1604 TT / Black", "description": "Watch", "qty": 75, "unit_price": 95.50},
        {"item": "1605 Black / Black", "description": "Accessories", "qty": 135, "unit_price": 94.50},
        {"item": "1606 Black / Black", "description": "Perfume", "qty": 135, "unit_price": 93.50},
        {"item": "1608 Black / Black", "description": "Bottom", "qty": 135, "unit_price": 95.50},                


    ]
}

# ==============================
# RUN GENERATOR
# ==============================
output_file = generate_invoice(invoice)

print("Test invoice generated:", output_file)
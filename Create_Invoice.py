import streamlit as st
import sqlite3

st.title("🧾 Create Invoice")

# ==============================
# Invoice Header
# ==============================
st.subheader("Invoice Information")

col1, col2 = st.columns(2)

with col1:
    customer = st.text_input("Customer", placeholder="e.g. The Focus Group")
    attn = st.text_input("Attn", placeholder="e.g. Michael Peterson")
    email = st.text_input("Email", placeholder="e.g. XXX@gmail.com")

with col2:
    invoice_no = st.text_input("Invoice No", placeholder="e.g. C-20633")
    date = st.text_input("Date", placeholder="e.g. 4 Jan 2026")

    invoice_type = st.selectbox(
        "Invoice Type",
        options=[("ABC Company", 1), ("DEF Company", 2)],
        format_func=lambda x: x[0]
    )[1]

st.divider()

# ==============================
# Search Filter
# ==============================
st.subheader("🔍Search Items")

search_text = st.text_input("Search by Model or Description")

# ==============================
# Load Items From SQLite (Filtered)
# ==============================
conn = sqlite3.connect("items.db")
cur = conn.cursor()

query = """
SELECT id, model_no, description, unit_price
FROM items
WHERE active = 1
"""

params = []

if search_text:
    query += " AND (model_no LIKE ? OR description LIKE ?)"
    params.extend([f"%{search_text}%", f"%{search_text}%"])

query += " ORDER BY model_no"

cur.execute(query, params)
items = cur.fetchall()
conn.close()

# ==============================
# Item Selection Section
# ==============================
selected_items = []

for item_id, model, desc, price in items:

    cols = st.columns([4, 2, 2])

    with cols[0]:
        st.write(f"**{model}**")
        st.caption(desc)

    with cols[1]:
        temp_price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=float(price),
            step=0.1,
            key=f"price_{item_id}"
        )

    with cols[2]:
        qty = st.number_input(
            "Qty",
            min_value=0,
            step=1,
            key=f"qty_{item_id}"
        )

    if qty > 0:
        selected_items.append({
            "item": model,
            "description": desc,
            "qty": qty,
            "unit_price": temp_price
        })

st.divider()

# ==============================
# Selected Items Summary
# ==============================
st.subheader("🛒 Selected Items Summary")

any_selected = False
index = 1

# Reload all active items to map id → name
conn = sqlite3.connect("items.db")
cur = conn.cursor()
cur.execute("""
    SELECT id, model_no, description
    FROM items
    WHERE active = 1
""")
all_items = {str(row[0]): (row[1], row[2]) for row in cur.fetchall()}
conn.close()

for key in sorted(st.session_state.keys()):
    if key.startswith("qty_") and st.session_state[key] > 0:
        item_id = key.replace("qty_", "")
        qty = st.session_state[key]
        price = st.session_state.get(f"price_{item_id}", 0)

        if item_id in all_items:
            model, desc = all_items[item_id]

            # Compact display using markdown (less vertical spacing)
            st.markdown(
                f"{index}. **{model}**  |  Qty: {qty}  |  Price: ${price}"
            )
            any_selected = True
            index += 1

if not any_selected:
    st.write("No items selected yet.")

st.divider()

# ==============================
# Generate Invoice
# ==============================
from generate_invoice import generate_invoice

if st.button("Generate Invoice"):

    missing_fields = []

    if not invoice_no.strip():
        missing_fields.append("Invoice No")
    if not customer.strip():
        missing_fields.append("Customer")
    if not date.strip():
        missing_fields.append("Date")
    if not attn.strip():
        missing_fields.append("Attn")
    if not email.strip():
        missing_fields.append("Email")

    if missing_fields:
        st.error(
            "Please fill in the following required fields: "
            + ", ".join(missing_fields)
        )
        st.stop()

    if not selected_items:
        st.warning("No items selected (qty must be greater than 0).")
        st.stop()

    invoice = {
        "invoice_type": invoice_type,
        "invoice_no": invoice_no,
        "date": date,
        "customer": customer,
        "attn": attn,
        "email": email,
        "items": selected_items
    }

    with st.spinner("Generating invoice..."):
        output_file = generate_invoice(invoice)

    st.success("Invoice generated successfully!")
    st.write(f"📄 File created: **{output_file}**")
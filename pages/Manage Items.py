import streamlit as st
import sqlite3

# ==============================
# Session State
# ==============================
if "edit_target" not in st.session_state:
    st.session_state.edit_target = None

if "delete_target" not in st.session_state:
    st.session_state.delete_target = None


st.title("⚙️ Manage Items")

# ==============================
# Database Connection
# ==============================
conn = sqlite3.connect("items.db")
cur = conn.cursor()


# ==============================
# Modify Item Dialog
# ==============================
@st.dialog("Modify Item")
def edit_item_dialog():
    target = st.session_state.edit_target

    new_model = st.text_input("Model No", value=target["model"])
    new_desc = st.text_input("Description", value=target["desc"])
    new_price = st.number_input(
        "Unit Price",
        min_value=0.0,
        value=float(target["price"]),
        step=0.1
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Changes"):
            conn_local = sqlite3.connect("items.db")
            cur_local = conn_local.cursor()

            cur_local.execute("""
                UPDATE items
                SET model_no = ?, description = ?, unit_price = ?
                WHERE id = ?
            """, (new_model, new_desc, new_price, target["id"]))

            conn_local.commit()
            conn_local.close()


            st.session_state.edit_target = None
            st.success("Item updated successfully.")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.session_state.edit_target = None
            st.rerun()


# ==============================
# Delete Confirmation Dialog
# ==============================
@st.dialog("Confirm Deletion")
def confirm_delete_dialog():
    target = st.session_state.delete_target

    st.write("Are you sure you want to delete this item?")
    st.write(f"**Model:** {target['model']}")
    st.write(f"**Description:** {target['desc']}")
    st.write(f"**Unit Price:** ${target['price']:.2f}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Confirm Delete"):
            conn_local = sqlite3.connect("items.db")
            cur_local = conn_local.cursor()

            cur_local.execute(
                "UPDATE items SET active = 0 WHERE id = ?",
                (target["id"],)
            )

            conn_local.commit()
            conn_local.close()  
            
            st.session_state.delete_target = None
            st.success("Item deleted.")
            st.rerun()

    with col2:
        if st.button("Cancel"):
            st.session_state.delete_target = None
            st.rerun()


# ==============================
# Add New Item
# ==============================
st.subheader("Add New Item")

new_model = st.text_input("Model No")
new_desc = st.text_input("Description")
new_price = st.number_input("Unit Price", min_value=0.0, step=0.1)

if st.button("Add Item"):
    if new_model and new_desc:
        cur.execute("""
            INSERT INTO items (model_no, description, unit_price, active)
            VALUES (?, ?, ?, 1)
        """, (new_model, new_desc, new_price))
        conn.commit()
        st.success("Item added successfully.")
        st.rerun()
    else:
        st.warning("Please fill all fields.")

st.divider()

# ==============================
# Filters
# ==============================
st.subheader("Filter Items")

search_text = st.text_input("Search (Model or Description)")

col_min, col_max = st.columns(2)
with col_min:
    min_price = st.number_input("Min Price", min_value=0.0, value=0.0)
with col_max:
    max_price = st.number_input("Max Price", min_value=0.0, value=100000.0)

sort_option = st.selectbox(
    "Sort By",
    ["Model (A-Z)", "Model (Z-A)", "Price (Low-High)", "Price (High-Low)"]
)

# ==============================
# Existing Items List
# ==============================
st.subheader("Existing Items")

query = """
SELECT id, model_no, description, unit_price
FROM items
WHERE active = 1
"""

params = []

# Search filter
if search_text:
    query += " AND (model_no LIKE ? OR description LIKE ?)"
    params.extend([f"%{search_text}%", f"%{search_text}%"])

# Price range filter
query += " AND unit_price BETWEEN ? AND ?"
params.extend([min_price, max_price])

# Sorting
if sort_option == "Model (A-Z)":
    query += " ORDER BY model_no ASC"
elif sort_option == "Model (Z-A)":
    query += " ORDER BY model_no DESC"
elif sort_option == "Price (Low-High)":
    query += " ORDER BY unit_price ASC"
elif sort_option == "Price (High-Low)":
    query += " ORDER BY unit_price DESC"

cur.execute(query, params)
items = cur.fetchall()

for item_id, model, desc, price in items:

    cols = st.columns([4, 2, 1, 1])

    with cols[0]:
        st.write(f"**{model}**")
        st.caption(desc)

    with cols[1]:
        st.write(f"${price:.2f}")

    with cols[2]:
        if st.button("Modify", key=f"edit_{item_id}"):
            st.session_state.edit_target = {
                "id": item_id,
                "model": model,
                "desc": desc,
                "price": price
            }
            edit_item_dialog()

    with cols[3]:
        if st.button("Delete", key=f"del_{item_id}"):
            st.session_state.delete_target = {
                "id": item_id,
                "model": model,
                "desc": desc,
                "price": price
            }
            confirm_delete_dialog()


conn.close()
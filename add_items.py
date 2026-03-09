import sqlite3

items = [
    ("1229 Black / Blue", "Lecture", 5.50),
    ("0993 Silver / Black", "Test", 8.50),
    ("1610 Black", "Light", 4.20),
    ("1651 TT / Black", "Dress", 2.50),
    ("1652 TT / Black", "Skirt", 9.50),
    ("1853 TT / Black", "Dress", 9.50),
    ("1854 TT / Black", "Bottom", 1.50),
    ("1855 TT / Black", "Skirt", 5.50),
    ("1856 TT / Black", "Pants", 6.50),
    ("1257 TT / Black", "Perfume", 9.50),
    ("1554 TT / Black", "Skirt", 8.50),
    ("1355 TT / Black", "Skirt", 9.50),
    ("1556 TT / Black", "Mini Dress", 9.70),
    ("1757 TT / Black", "Crop Top", 9.40),
]

conn = sqlite3.connect("items.db")
cur = conn.cursor()

cur.executemany(
    "INSERT INTO items (model_no, description, unit_price) VALUES (?, ?, ?)",
    items
)

conn.commit()
conn.close()

print("Items inserted successfully.")

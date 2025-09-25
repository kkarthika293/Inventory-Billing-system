# view_transaction.py – View Transaction History with UI

import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db

# ---------- Window Setup ----------
root = tk.Tk()
root.title("Transaction History")
root.geometry("900x500")
root.configure(bg="#f5f7fa")

# ---------- Frame ----------
frame = tk.Frame(root, bg="white", bd=2, relief="groove")
frame.pack(fill='both', expand=True, padx=15, pady=15)

# ---------- Title ----------
tk.Label(frame, text="Transaction History", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

# ---------- Treeview Table ----------
columns = ("Bill ID", "Date", "Total")
tree = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200 if col != "Total" else 100)
tree.pack(fill="both", expand=True, pady=10)

# ---------- View Items in a Bill ----------
def view_items(event):
    selected = tree.selection()
    if not selected:
        return
    bill_id = tree.item(selected[0])["values"][0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.name, bi.quantity, bi.price
        FROM bill_items bi
        JOIN products p ON p.id = bi.product_id
        WHERE bi.bill_id = %s
    """, (bill_id,))
    items = cursor.fetchall()
    conn.close()

    items_str = "\n".join([f"{name} - {qty} x Rs.{price:.2f} = Rs.{qty*price:.2f}" for name, qty, price in items])
    messagebox.showinfo(f"Items in Bill #{bill_id}", items_str)

# ---------- Populate Table ----------
def load_transactions():
    for i in tree.get_children():
        tree.delete(i)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bill_id, date, total FROM bills ORDER BY date DESC")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

# Bind event to treeview
load_transactions()
tree.bind("<Double-1>", view_items)

root.mainloop()

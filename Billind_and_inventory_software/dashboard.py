# dashboard.py - Enhanced Layout with PDF Export
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -------------------- Database Connection --------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Praveen@2930",
        database="billing_system"
    )

# -------------------- Main Dashboard --------------------
dashboard = tk.Tk()
dashboard.title("Inventory Billing - Dashboard")
dashboard.geometry("1024x720")
dashboard.configure(bg="#1e272e")

# Header
header = tk.Label(dashboard, text="Inventory Billing Dashboard", font=("Segoe UI", 28, "bold"), fg="white", bg="#1e272e")
header.pack(pady=10, fill="x")

# Main Container
main_frame = tk.Frame(dashboard, bg="#2f3640", bd=3, relief="ridge")
main_frame.pack(padx=30, pady=20, fill="both", expand=True)

# -------------------- Variables --------------------
name_var = tk.StringVar()
category_var = tk.StringVar()
price_var = tk.StringVar()
qty_var = tk.IntVar(value=1)

# -------------------- Load Products --------------------
data = {}

# -------------------- UI Layout --------------------
form_frame = tk.Frame(main_frame, bg="#2f3640")
form_frame.pack(pady=20)

FONT = ("Segoe UI", 13)
TEXT_COLOR = "white"
CARD_COLOR = "#2f3640"

fields = [
    ("Product Name", name_var),
    ("Category", category_var),
    ("Price", price_var),
    ("Quantity", qty_var)
]

entry_name = ttk.Combobox(form_frame, textvariable=name_var, font=FONT, width=35, state="readonly")
entry_name.bind("<<ComboboxSelected>>", lambda e: autofill(None))

def load_products():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT name, category, price FROM products")
        rows = cur.fetchall()
        names = []
        for name, category, price in rows:
            data[name] = (category, price)
            names.append(name)
        entry_name["values"] = names
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def autofill(event):
    pname = name_var.get()
    if pname in data:
        category, price = data[pname]
        category_var.set(category)
        price_var.set(price)

for i, (label, var) in enumerate(fields):
    tk.Label(form_frame, text=label, font=FONT, fg=TEXT_COLOR, bg=CARD_COLOR).grid(row=i, column=0, padx=15, pady=15, sticky="e")

    if label == "Product Name":
        entry_name.grid(row=i, column=1, padx=15, pady=15, sticky="w")
    elif label == "Quantity":
        entry = tk.Entry(form_frame, textvariable=var, font=FONT, width=35)
        entry.grid(row=i, column=1, padx=15, pady=15, sticky="w")
    else:
        entry = tk.Entry(form_frame, textvariable=var, font=FONT, width=35, state="readonly")
        entry.grid(row=i, column=1, padx=15, pady=15, sticky="w")

load_products()

# -------------------- Cart Treeview --------------------
cart_frame = tk.Frame(main_frame, bg="#2f3640")
cart_frame.pack(pady=10)

cart_tree = ttk.Treeview(cart_frame, columns=("Product", "Category", "Price", "Qty", "Total"), show="headings", height=8)
for col in ("Product", "Category", "Price", "Qty", "Total"):
    cart_tree.heading(col, text=col)
    cart_tree.column(col, width=120, anchor="center")
cart_tree.pack(padx=10, pady=10)

# -------------------- Buttons --------------------
cart_total = 0

def add_to_cart():
    try:
        pname = name_var.get()
        category = category_var.get()
        price = float(price_var.get())
        qty = int(qty_var.get())
        total = price * qty
        if pname:
            cart_tree.insert("", "end", values=(pname, category, price, qty, total))
            name_var.set("")
            category_var.set("")
            price_var.set("")
            qty_var.set(1)
    except:
        messagebox.showerror("Error", "Enter valid data")

def calculate_total():
    global cart_total
    cart_total = 0
    for item in cart_tree.get_children():
        total = float(cart_tree.item(item)['values'][4])
        cart_total += total
    lbl_total.config(text=f"Total: ₹{cart_total:.2f}")

def view_bill():
    win = tk.Toplevel(dashboard)
    win.title("Bill Summary")
    win.geometry("700x500")
    win.config(bg="#34495e")

    txt = tk.Text(win, font=("Courier New", 11), bg="white")
    txt.pack(padx=10, pady=10, fill="both", expand=True)

    txt.insert("end", f"{'Product':<18}{'Category':<12}{'Qty':<8}{'Total':<10}\n")
    txt.insert("end", "-"*60 + "\n")

    for item in cart_tree.get_children():
        name, category, price, qty, total = cart_tree.item(item)['values']
        try:
            total = float(total)
        except:
            total = 0.0
        txt.insert("end", f"{str(name):<18}{str(category):<12}{str(qty):<8}{float(total):<10.2f}\n")

    txt.insert("end", f"\nTotal Amount: ₹{cart_total:.2f}\n")

    def export():
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file:
            return

        c = canvas.Canvas(file, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 50, "Inventory Billing Receipt")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 90, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

        c.setFont("Helvetica-Bold", 12)
        y = height - 130
        c.drawString(50, y, "Product")
        c.drawString(200, y, "Category")
        c.drawString(320, y, "Qty")
        c.drawString(400, y, "Total")

        c.setFont("Helvetica", 12)
        y -= 20

        for item in cart_tree.get_children():
            name, category, price, qty, total = cart_tree.item(item)['values']
            c.drawString(50, y, str(name))
            c.drawString(200, y, str(category))
            c.drawString(320, y, str(qty))
            c.drawString(400, y, f"₹{float(total):.2f}")
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total Amount: ₹{cart_total:.2f}")

        c.save()
        messagebox.showinfo("Exported", "Bill exported to PDF successfully.")

    tk.Button(win, text="Export as PDF", command=export, bg="#27ae60", fg="white", font=("Segoe UI", 11), width=15).pack(pady=10)
    tk.Button(win, text="Close", command=win.destroy, bg="#c0392b", fg="white", font=("Segoe UI", 11), width=15).pack(pady=(0, 20))

# Buttons Panel
btn_frame = tk.Frame(main_frame, bg="#2f3640")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add to Cart", command=add_to_cart, bg="#00a8ff", fg="white", font=("Segoe UI", 11), width=15).grid(row=0, column=0, padx=15)
tk.Button(btn_frame, text="Calculate Total", command=calculate_total, bg="#9c88ff", fg="white", font=("Segoe UI", 11), width=15).grid(row=0, column=1, padx=15)
tk.Button(btn_frame, text="View Bill", command=view_bill, bg="#e84393", fg="white", font=("Segoe UI", 11), width=15).grid(row=0, column=2, padx=15)

# Total Display
lbl_total = tk.Label(main_frame, text="Total: ₹0.00", font=("Segoe UI", 14, "bold"), fg="#fbc531", bg="#2f3640")
lbl_total.pack(pady=(0, 15))

# -------------------- Mainloop --------------------
dashboard.mainloop()

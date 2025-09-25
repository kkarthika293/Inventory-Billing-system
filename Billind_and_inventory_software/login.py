# login.py - With Show Password Toggle Feature
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Launch dashboard after login (replace with your actual dashboard function or file)
def open_dashboard():
    try:
        subprocess.Popen([sys.executable, 'dashboard.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open dashboard: {e}")

# ---------------------- Login Function ----------------------
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "admin123":
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Toggle password visibility
def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# ---------------------- GUI Setup ----------------------
root = tk.Tk()
root.title("Inventory System - Login")
root.geometry("400x370")
root.configure(bg="#2c3e50")
root.resizable(False, False)

# Outer Frame
frame = tk.Frame(root, bg="#34495e", padx=25, pady=30, bd=3, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor='center')

# Title
tk.Label(frame, text="Admin Login", font=("Segoe UI", 20, "bold"), fg="white", bg="#34495e").pack(pady=10)

# Username
tk.Label(frame, text="Username", font=("Segoe UI", 12), bg="#34495e", fg="white").pack(anchor="w", padx=5)
username_entry = tk.Entry(frame, font=("Segoe UI", 12))
username_entry.pack(fill="x", pady=(6, 12))

# Password
tk.Label(frame, text="Password", font=("Segoe UI", 12), bg="#34495e", fg="white").pack(anchor="w", padx=5)
password_entry = tk.Entry(frame, show="*", font=("Segoe UI", 12))
password_entry.pack(fill="x", pady=(6, 6))

# Show Password Checkbox
show_password_var = tk.BooleanVar()
tk.Checkbutton(
    frame,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password,
    bg="#34495e",
    fg="white",
    activebackground="#34495e",
    font=("Segoe UI", 10),
    anchor="w"
).pack(anchor="w", padx=5, pady=(0, 20))  # Increased bottom padding

# Login Button (Compact and Clean)
tk.Button(
    frame,
    text="LOGIN",
    command=login,
    bg="#1abc9c",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=6,
    pady=4,
    activebackground="#16a085",
    relief="raised",
    bd=2
).pack(pady=5, ipadx=4, ipady=1)

root.mainloop()

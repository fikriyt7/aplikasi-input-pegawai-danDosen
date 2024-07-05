import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from utils.session import Session
from db import get_db_connection

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Placeholder login check, replace with actual database check
    if username == "admin" and password == "admin":
        Session.set_user({"username": username, "profile_pic": "path/to/profile_pic.png"})
        login_window.destroy()
        open_main_application()
    else:
        messagebox.showerror("Login Error", "Invalid username or password")

def open_login_window():
    global login_window
    global entry_username
    global entry_password

    login_window = tk.Tk()
    login_window.title("Form Login Admin")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f0f0")  # Background color

    # Load and resize logo
    logo_path = "gui/logo.png"  # Adjust with your actual path
    load_logo = Image.open(logo_path)
    resized_logo = load_logo.resize((200, 200), Image.LANCZOS)  # Resize logo as needed with LANCZOS filter
    logo_img = ImageTk.PhotoImage(resized_logo)

    logo_label = tk.Label(login_window, image=logo_img, bg="#f0f0f0")
    logo_label.grid(row=0, columnspan=2, pady=10)

    tk.Label(login_window, text="Username", font=("Helvetica", 14), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
    entry_username = tk.Entry(login_window, font=("Helvetica", 12))
    entry_username.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(login_window, text="Password", font=("Helvetica", 14), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
    entry_password = tk.Entry(login_window, show="*", font=("Helvetica", 12))
    entry_password.grid(row=2, column=1, padx=10, pady=5)

    login_button = tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    login_button.grid(row=3, columnspan=2, pady=10, padx=10)

    login_window.mainloop()

if __name__ == "__main__":
    open_login_window()

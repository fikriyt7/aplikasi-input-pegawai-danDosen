import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from gui.main_application import open_main_application
from db import connect_db

def open_login_window():
    
    def login():
        username = entry_username.get()
        password = entry_password.get()

        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Info", "Login Berhasil")
            login_window.destroy()
            open_main_application()
        else:
            messagebox.showerror("Error", "Username atau Password salah")

        cursor.close()
        conn.close()

    login_window = tk.Tk()
    login_window.title("Form Login Admin")
    login_window.geometry("800x600")  # Ukuran jendela login
    login_window.resizable(True,True)  # Mematikan kemampuan diperbesar

    # Canvas untuk background
    canvas = tk.Canvas(login_window, width=login_window.winfo_width(), height=login_window.winfo_height())
    canvas.pack(fill=tk.BOTH, expand=True)
    
    ctk.set_appearance_mode("dark")  # Set the appearance mode
    ctk.set_default_color_theme("blue")  # Set the color theme
    frame = ctk.CTkFrame(master=login_window, fg_color="transparent")
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    # Background Image
    try:
        background_image = Image.open("gui/bg8.png")  # Ganti dengan gambar background yang sesuai
        background_photo = ImageTk.PhotoImage(background_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)
    except FileNotFoundError:
        print("File gui/bg5.png tidak ditemukan.")
    
    # Logo
    try:
        logo_image = Image.open("gui/logo.png")
        logo_image = logo_image.resize((120, 120), Image.LANCZOS)  # Resize logo
        logo_photo = ImageTk.PhotoImage(logo_image)
        
        canvas.create_image(630, 50, anchor=tk.NW, image=logo_photo)  # Memindahkan posisi logo ke kiri atas
    except FileNotFoundError:
        print("File gui/logo.png tidak ditemukan.")

    # Header
    header_label = tk.Label(login_window, text="Aplikasi Kelola Data Pegawai Dan Dosen  ", font=("Helvetica", 16, "bold"), bg="#143c24", fg="white", pady=10)
    header_label.pack(fill=tk.X)

    # Teks Copyright
    copyright_label = tk.Label(login_window, text="Copyright 2024 | Universitas Hamzanwadi", font=("Helvetica", 10), bg="#143c24", fg="white", pady=5)
    copyright_label.pack(fill=tk.X)

    # Frame untuk form login
    title_label = tk.Label(master=frame, text="  Selamat Datang Silahkan  \nLogin", font=("Arial", 28, "bold"),fg="#143c24")
    title_label.pack(pady=22)

    # Add username entry with padding
    entry_username = ctk.CTkEntry(master=frame, placeholder_text="Username", width=300, height=40, font=("Arial", 14), fg_color="#143c24")
    entry_username.pack(pady=10)

    # Add password entry with padding
    entry_password = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*", width=300, height=40, font=("Arial", 14), fg_color="#143c24")
    entry_password.pack(pady=10)

    # Add login button with customized style
    login_button = ctk.CTkButton(master=frame, text="Login", command=login, width=150, height=40, font=("Arial", 14),  fg_color="#143c24")
    login_button.pack(pady=20)


    # Menjalankan loop utama aplikasi
    login_window.mainloop()

# Fungsi untuk membuka jendela login saat aplikasi dijalankan
if __name__ == "__main__":
    open_login_window()

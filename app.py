import tkinter as tk
from gui.login_window import open_login_window
from gui.main_application import open_main_application

if __name__ == "__main__":
    # Menampilkan jendela login terlebih dahulu
    open_login_window()
    
    # Setelah login sukses, baru buka aplikasi utama
    open_main_application()

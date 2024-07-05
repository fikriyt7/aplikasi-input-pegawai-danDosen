import customtkinter as ctk
from db import fetch_data

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Set main frame background color
        self.configure(fg_color="#143c24", corner_radius=10)

        # Container for the content
        content_frame = ctk.CTkFrame(self, fg_color="#1e4b35", corner_radius=10)
        content_frame.pack(pady=20, padx=50, anchor="center", expand=True, fill="both")

        # Title Label
        label = ctk.CTkLabel(content_frame, text="Selamat Datang di Aplikasi Input Data Pegawai dan Dosen",
                             font=("Arial", 24, "bold"), text_color="white")
        label.pack(pady=(30, 10), padx=20, anchor="center")

        # Container for counts
        counts_frame = ctk.CTkFrame(content_frame, fg_color="#1e4b35", corner_radius=10)
        counts_frame.pack(pady=20, padx=20, anchor="center", expand=True, fill="both")

        # Pegawai count section
        pegawai_frame = ctk.CTkFrame(counts_frame, fg_color="#2e5f45", corner_radius=10)
        pegawai_frame.pack(side="left", padx=20, pady=10, expand=True, fill="both")

        pegawai_label = ctk.CTkLabel(pegawai_frame, text="Jumlah Pegawai:", font=("Arial", 16, "bold"), text_color="white")
        pegawai_label.pack(pady=(20, 10), padx=10, anchor="center")

        self.pegawai_count = ctk.StringVar()
        pegawai_count_label = ctk.CTkLabel(pegawai_frame, textvariable=self.pegawai_count, font=("Arial", 16), text_color="white")
        pegawai_count_label.pack(pady=(10, 20), padx=10, anchor="center")

        # Dosen count section
        dosen_frame = ctk.CTkFrame(counts_frame, fg_color="#2e5f45", corner_radius=10)
        dosen_frame.pack(side="right", padx=20, pady=10, expand=True, fill="both")

        dosen_label = ctk.CTkLabel(dosen_frame, text="Jumlah Dosen:", font=("Arial", 16, "bold"), text_color="white")
        dosen_label.pack(pady=(20, 10), padx=10, anchor="center")

        self.dosen_count = ctk.StringVar()
        dosen_count_label = ctk.CTkLabel(dosen_frame, textvariable=self.dosen_count, font=("Arial", 16), text_color="white")
        dosen_count_label.pack(pady=(10, 20), padx=10, anchor="center")

        self.update_counts()

    def update_counts(self):
        pegawai_data = fetch_data("pegawai")
        dosen_data = fetch_data("dosen")

        self.pegawai_count.set(len(pegawai_data))
        self.dosen_count.set(len(dosen_data))

# Example usage:
if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    StartPage(app, None).pack(expand=True, fill="both")
    app.mainloop()

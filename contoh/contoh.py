import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from dbc import fetch_data, save_data, update_data, delete_data

class DosenPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f0f0')  # Warna latar belakang terang
        self.controller = controller

        label = tk.Label(self, text="Data Dosen", font=("Helvetica", 20, "bold"), bg='#f0f0f0', fg='#143c24')  # Pengaturan header
        label.pack(pady=20)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=self.search_var, width=30, font=("Helvetica", 12))
        search_entry.pack(pady=10)
        search_entry.insert(0, "Cari Nama Dosen...")
        search_entry.bind('<FocusIn>', lambda event: self.on_entry_click(event, search_entry))
        search_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, search_entry))
        search_entry.bind('<KeyRelease>', self.search_dosen)

        self.tree = ttk.Treeview(self, columns=("ID", "Nama", "Alamat", "Mata Kuliah", "No. Telpon", "Jabatan", "Foto"), show='headings', selectmode='browse', height=15)
        self.tree.heading("ID", text="ID", anchor='center')
        self.tree.heading("Nama", text="Nama", anchor='center')
        self.tree.heading("Alamat", text="Alamat", anchor='center')
        self.tree.heading("Mata Kuliah", text="Mata Kuliah", anchor='center')
        self.tree.heading("No. Telpon", text="No. Telpon", anchor='center')
        self.tree.heading("Jabatan", text="Jabatan", anchor='center')
        self.tree.heading("Foto", text="Foto", anchor='center')  # Kolom untuk menampilkan gambar

        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Nama", width=150, anchor='center')
        self.tree.column("Alamat", width=200, anchor='center')
        self.tree.column("Mata Kuliah", width=150, anchor='center')
        self.tree.column("No. Telpon", width=100, anchor='center')
        self.tree.column("Jabatan", width=150, anchor='center')
        self.tree.column("Foto", width=100, anchor='center')  # Atur lebar kolom foto

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Gunakan tema yang berbeda untuk tampilan yang lebih modern
        self.style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#143c24', font=('Helvetica', 10))
        self.style.map('Treeview', background=[('selected', '#143c24')])

        self.populate_treeview()

        button_frame = tk.Frame(self, bg='#f0f0f0')  # Sesuaikan warna latar belakang
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Tambah", command=self.add_dosen, style='Accent.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_dosen, style='Accent.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hapus", command=self.delete_dosen, style='Accent.TButton').pack(side="left", padx=5)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        rows = fetch_data("dosen")
        for i, row in enumerate(rows, start=1):
            if row[6]:  # Menampilkan gambar jika ada path gambar dalam basis data
                self.display_image_in_treeview(row[0], row[6])
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], ''))  # Pastikan menyesuaikan indeks

    def add_dosen(self):
        self.show_form("Add", "dosen")

    def edit_dosen(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang akan diedit")
            return

        selected_item = self.tree.item(selected_item)
        self.show_form("Edit", "dosen", selected_item["values"])

    def delete_dosen(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang akan dihapus")
            return

        selected_item = self.tree.item(selected_item)
        delete_data("dosen", selected_item["values"][0])
        self.populate_treeview()

    def show_form(self, action, table, data=None):
        form = tk.Toplevel(self)

        form.title(action + " Data Dosen")
        form.geometry("400x400")
        form.configure(bg='#f0f0f0')

        tk.Label(form, text="Nama", font=("Helvetica", 12), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=5, sticky='e')
        entry_nama = tk.Entry(form, font=("Helvetica", 12))
        entry_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Alamat", font=("Helvetica", 12), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        entry_alamat = tk.Entry(form, font=("Helvetica", 12))
        entry_alamat.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Mata Kuliah", font=("Helvetica", 12), bg='#f0f0f0').grid(row=2, column=0, padx=10, pady=5, sticky='e')
        entry_mata_kuliah = tk.Entry(form, font=("Helvetica", 12))
        entry_mata_kuliah.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="No. Telpon", font=("Helvetica", 12), bg='#f0f0f0').grid(row=3, column=0, padx=10, pady=5, sticky='e')
        entry_no_telpon = tk.Entry(form, font=("Helvetica", 12))
        entry_no_telpon.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form, text="Jabatan", font=("Helvetica", 12), bg='#f0f0f0').grid(row=4, column=0, padx=10, pady=5, sticky='e')
        entry_jabatan = tk.Entry(form, font=("Helvetica", 12))
        entry_jabatan.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form, text="Foto", font=("Helvetica", 12), bg='#f0f0f0').grid(row=5, column=0, padx=10, pady=5, sticky='e')
        upload_button = ttk.Button(form, text="Unggah Foto", command=lambda: self.upload_photo(entry_foto))
        upload_button.grid(row=5, column=1, padx=10, pady=5)
        entry_foto = tk.Entry(form, font=("Helvetica", 12))
        entry_foto.grid(row=5, column=2, padx=10, pady=5)

        if action == "Edit" and data:
            entry_nama.insert(0, data[1])
            entry_alamat.insert(0, data[2])
            entry_mata_kuliah.insert(0, data[3])
            entry_no_telpon.insert(0, data[4])
            entry_jabatan.insert(0, data[5])
            entry_foto.insert(0, data[6])  # Pastikan menyesuaikan indeks

        def save():
            nama = entry_nama.get()
            alamat = entry_alamat.get()
            mata_kuliah = entry_mata_kuliah.get()
            no_telpon = entry_no_telpon.get()
            jabatan = entry_jabatan.get()
            foto = entry_foto.get()  # Path atau data biner gambar

            if action == "Add":
                save_data(table, (nama, alamat, mata_kuliah, no_telpon, jabatan, foto))
            elif action == "Edit":
                update_data(table, (nama, alamat, mata_kuliah, no_telpon, jabatan, foto), data[0])

            self.populate_treeview()
            form.destroy()

        ttk.Button(form, text="Simpan", command=save, style='Accent.TButton').grid(row=6, columnspan=2, pady=10)

    def upload_photo(self, entry_widget):
        file_path = filedialog.askopenfilename(title="Pilih Gambar", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")))
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)

    def display_image_in_treeview(self, item_id, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((50, 50), Image.ANTIALIAS)  # Sesuaikan ukuran gambar
            photo = ImageTk.PhotoImage(image)

            self.tree.set(item_id, column="Foto", value=photo)  # Menetapkan gambar ke kolom 'Foto'

            # Menyimpan referensi agar gambar tetap ditampilkan
            self.tree.image_references[item_id] = photo

        except Exception as e:
            print(f"Error displaying image: {str(e)}")

    def search_dosen(self, event):
        search_term = self.search_var.get().lower()
        if search_term == "":
            self.populate_treeview()
        else:
            self.tree.delete(*self.tree.get_children())
            rows = fetch_data("dosen")
            for row in rows:
                if search_term in row[1].lower():  # Cari berdasarkan nama
                    if row[6]:  # Anggap row[6] berisi path gambar atau data biner gambar
                        self.display_image_in_treeview(row[0], row[6])
                    self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], ''))  # Pastikan menyesuaikan indeks

    def on_entry_click(self, event, entry):
        if entry.get() == "Cari Nama Dosen...":
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focusout(self, event, entry):
        if entry.get() == "":
            entry.insert(0, "Cari Nama Dosen...")
            entry.config(fg='grey')

if __name__ == "__main__":
    # Contoh penggunaan
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Aplikasi Manajemen Dosen dan pegawai")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    dosen_page = DosenPage(main_frame, controller=root)
    dosen_page.pack(fill="both", expand=True)

    root.mainloop()

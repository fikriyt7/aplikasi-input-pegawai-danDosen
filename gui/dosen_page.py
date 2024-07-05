import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Ensure you have PIL installed
from db import fetch_data, save_data, update_data, delete_data

class DosenPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f0f0')  # Light background color
        self.controller = controller

        label = tk.Label(self, text="Data Dosen", font=("Helvetica", 20, "bold"), bg='#f0f0f0', fg='#143c24')  # Header styling
        label.pack(pady=20)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=self.search_var, width=30, font=("Helvetica", 12))
        search_entry.pack(pady=10)
        search_entry.insert(0, "Cari Nama Dosen...")
        search_entry.bind('<FocusIn>', lambda event: self.on_entry_click(event, search_entry))
        search_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, search_entry))
        search_entry.bind('<KeyRelease>', self.search_dosen)

        self.tree = ttk.Treeview(self, columns=("ID", "Nama", "Alamat", "Mata Kuliah", "No. Telpon"), show='headings', selectmode='browse', height=15)
        self.tree.heading("ID", text="ID", anchor='center')
        self.tree.heading("Nama", text="Nama", anchor='center')
        self.tree.heading("Alamat", text="Alamat", anchor='center')
        self.tree.heading("Mata Kuliah", text="Mata Kuliah", anchor='center')
        self.tree.heading("No. Telpon", text="No. Telpon", anchor='center')
        
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Nama", width=150, anchor='center')
        self.tree.column("Alamat", width=200, anchor='center')
        self.tree.column("Mata Kuliah", width=150, anchor='center')
        self.tree.column("No. Telpon", width=100, anchor='center')

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a different theme for more modern look
        self.style.configure('Treeview', background='#ffffff', fieldbackground='#ffffff', foreground='#143c24', font=('Helvetica', 10))
        self.style.map('Treeview', background=[('selected', '#143c24')])

        self.populate_treeview()

        button_frame = tk.Frame(self, bg='#f0f0f0')  # Match background color
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Tambah", command=self.add_dosen, style='Accent.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_dosen, style='Accent.TButton').pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hapus", command=self.delete_dosen, style='Accent.TButton').pack(side="left", padx=5)

    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())
        rows = fetch_data("dosen")
        for row in rows:
            self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

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

        confirmed = messagebox.askyesno("Konfirmasi", "Anda yakin ingin menghapus data ini?")
        if confirmed:
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

        if action == "Edit" and data:
            entry_nama.insert(0, data[1])
            entry_alamat.insert(0, data[2])
            entry_mata_kuliah.insert(0, data[3])
            entry_no_telpon.insert(0, data[4])

        ttk.Button(form, text=action, command=lambda: self.save_or_update_dosen(form, action, table, data, entry_nama.get(), entry_alamat.get(), entry_mata_kuliah.get(), entry_no_telpon.get()), style='Accent.TButton').grid(row=4, column=0, columnspan=2, pady=10)

    def save_or_update_dosen(self, form, action, table, data, nama, alamat, mata_kuliah, no_telpon):
        if action == "Add":
            save_data("dosen", (nama, alamat, mata_kuliah, no_telpon))
        elif action == "Edit":
            update_data("dosen", (nama, alamat, mata_kuliah, no_telpon), data[0])

        form.destroy()
        self.populate_treeview()

    def search_dosen(self, event):
        search_term = self.search_var.get().strip()
        if search_term:
            rows = fetch_data("dosen")
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                if search_term.lower() in row[1].lower():  # Search by name
                    self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
        else:
            self.populate_treeview()

    def on_entry_click(self, event, entry_widget):
        if entry_widget.get() == 'Cari Nama Dosen...':
            entry_widget.delete(0, "end")
            entry_widget.insert(0, '')
            entry_widget.config(fg = 'black')

    def on_focusout(self, event, entry_widget):
        if entry_widget.get() == '':
            entry_widget.insert(0, 'Cari Nama Dosen...')
            entry_widget.config(fg = 'grey')

if __name__ == "__main__":
    app = tk.Tk()
    app.geometry("800x600")
    app.title("Aplikasi Manajemen Data")
    DosenPage(app).pack(side="top", fill="both", expand=True)
    app.mainloop()

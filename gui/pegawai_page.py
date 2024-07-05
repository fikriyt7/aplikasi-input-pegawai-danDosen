import tkinter as tk
from tkinter import ttk, messagebox
from db import fetch_data, save_data, update_data, delete_data

class PegawaiPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Label
        label = tk.Label(self, text="Data Pegawai", font=("Helvetica", 16, "bold"))
        label.pack(pady=20)

        # Search Entry
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=self.search_var, width=30, font=("Helvetica", 12))
        search_entry.pack(pady=10)
        search_entry.insert(0, "Cari Nama Pegawai...")
        search_entry.bind('<FocusIn>', lambda event: self.on_entry_click(event, search_entry))
        search_entry.bind('<FocusOut>', lambda event: self.on_focusout(event, search_entry))
        search_entry.bind('<KeyRelease>', self.search_pegawai)

        # Treeview Widget
        self.tree = ttk.Treeview(self, columns=("ID", "Nama", "Alamat", "Jabatan"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Alamat", text="Alamat")
        self.tree.heading("Jabatan", text="Jabatan")
        self.tree.pack(fill="both", expand=True)

        # Populate Treeview
        self.populate_treeview()

        # Button Frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Buttons
        tk.Button(button_frame, text="Tambah", command=self.add_pegawai).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit", command=self.edit_pegawai).pack(side="left", padx=5)
        tk.Button(button_frame, text="Hapus", command=self.delete_pegawai).pack(side="left", padx=5)

    def populate_treeview(self):
        # Clear existing data in treeview
        self.tree.delete(*self.tree.get_children())
        
        # Fetch data from database and insert into treeview
        rows = fetch_data("pegawai")
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_pegawai(self):
        self.show_form("Add", "pegawai")

    def edit_pegawai(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang akan diedit")
            return
        
        # Retrieve selected item values and show edit form
        selected_item = self.tree.item(selected_item)
        self.show_form("Edit", "pegawai", selected_item["values"])

    def delete_pegawai(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih data yang akan dihapus")
            return
        
        # Retrieve selected item values and delete from database
        selected_item = self.tree.item(selected_item)
        delete_data("pegawai", selected_item["values"][0])
        
        # Refresh treeview
        self.populate_treeview()

    def show_form(self, action, table, data=None):
        form = tk.Toplevel(self)
        form.title(f"{action} Data Pegawai")
        
        # Labels and Entry Fields
        tk.Label(form, text="Nama").grid(row=0, column=0, padx=10, pady=5)
        entry_nama = tk.Entry(form)
        entry_nama.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Alamat").grid(row=1, column=0, padx=10, pady=5)
        entry_alamat = tk.Entry(form)
        entry_alamat.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Jabatan").grid(row=2, column=0, padx=10, pady=5)
        entry_jabatan = tk.Entry(form)
        entry_jabatan.grid(row=2, column=1, padx=10, pady=5)

        # Pre-fill fields if editing
        if action == "Edit" and data:
            entry_nama.insert(0, data[1])
            entry_alamat.insert(0, data[2])
            entry_jabatan.insert(0, data[3])

        # Save function
        def save():
            nama = entry_nama.get()
            alamat = entry_alamat.get()
            jabatan = entry_jabatan.get()

            # Perform database operation based on action
            if action == "Add":
                save_data(table, (nama, alamat, jabatan))
            elif action == "Edit":
                update_data(table, (nama, alamat, jabatan), data[0])

            # Refresh treeview and close form
            self.populate_treeview()
            form.destroy()

        # Save Button
        tk.Button(form, text="Simpan", command=save).grid(row=3, columnspan=2, pady=10)

    def on_entry_click(self, event, entry):
        if entry.get() == "Cari Nama Pegawai...":
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focusout(self, event, entry):
        if entry.get() == "":
            entry.insert(0, "Cari Nama Pegawai...")
            entry.config(fg='grey')

    def search_pegawai(self, event=None):
        keyword = self.search_var.get()
        if keyword == "":
            self.populate_treeview()  # If search field is empty, show all data
        else:
            filtered_rows = []
            rows = fetch_data("pegawai")
            for row in rows:
                if keyword.lower() in row[1].lower():  # Check if keyword matches 'Nama'
                    filtered_rows.append(row)
            self.tree.delete(*self.tree.get_children())
            for row in filtered_rows:
                self.tree.insert("", "end", values=row)

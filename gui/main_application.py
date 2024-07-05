import customtkinter as ctk
from PIL import Image, ImageTk
from gui.start_page import StartPage
from gui.pegawai_page import PegawaiPage
from gui.dosen_page import DosenPage
from gui.pengembangPage import PengembangPage

def open_main_application():
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
    
    root = ctk.CTk()
    root.title("Aplikasi Input Data Pegawai dan Dosen")
    root.geometry("1000x600")  # Increased window size for more space

    # Main container using grid layout
    main_frame = ctk.CTkFrame(root)
    main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Sidebar with background color using grid layout
    sidebar = ctk.CTkFrame(root, width=200, fg_color="#143c24")
    sidebar.grid(row=0, column=0, sticky="ns")

    # Add logo to sidebar
    logo_image = Image.open("gui/logo.png")  # Replace with the actual path to your logo image
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize the image to fit the sidebar
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(sidebar, image=logo_photo, text="")
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=20)

    # Function to switch frames
    def show_frame(frame_class):
        frame = frames[frame_class]
        frame.tkraise()

    # Create sidebar buttons
    buttons = [
        ("Dashboard", StartPage),
        ("Dosen", DosenPage),
        ("Pegawai", PegawaiPage),
        ("Pengembang", PengembangPage)  # Updated with PengembangPage
    ]

    frames = {}
    for btn_text, frame_class in buttons:
        frame = frame_class(parent=main_frame, controller=root)
        frames[frame_class] = frame
        frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=20)  # Use grid layout for frames
        if btn_text == "Dashboard":
            frame.tkraise()

        button = ctk.CTkButton(
            sidebar, text=btn_text, command=lambda f=frame_class: show_frame(f)
        )
        button.pack(fill="x", pady=5, padx=10)

    # Create a logout button at the bottom
    logout_button = ctk.CTkButton(sidebar, text="Logout", fg_color="red", command=root.destroy)
    logout_button.pack(side="bottom", pady=20, padx=10)

    root.mainloop()

if __name__ == "__main__":
    open_main_application()

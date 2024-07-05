import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

class PengembangPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        developers = [
            {
                "name": "Aditiya Pranata",
                "email": "aditiya.pranata@example.com",
                "address": "Jl. Mawar No. 123, Jakarta, Indonesia",
                "photo_path": "gui/p1.png"  # Replace with the actual path to the profile photo
            },
            {
                "name": "Developer Two",
                "email": "developer.two@example.com",
                "address": "Jl. Melati No. 456, Bandung, Indonesia",
                "photo_path": "gui/p2.jpg"# Replace with the actual path to the profile photo
            },
            {
                "name": "Developer Three",
                "email": "developer.three@example.com",
                "address": "Jl. Anggrek No. 789, Surabaya, Indonesia",
                "photo_path": "gui/p3.png"  # Replace with the actual path to the profile photo
            }
        ]

        for developer in developers:
            self.create_developer_section(developer).pack(pady=20)

    def create_developer_section(self, developer):
        frame = ctk.CTkFrame(self)

        # Profile photo
        profile_image = Image.open(developer["photo_path"])
        profile_image = profile_image.resize((150, 150), Image.LANCZOS)
        profile_image = self.make_circle(profile_image)
        profile_photo = ImageTk.PhotoImage(profile_image)
        
        profile_label = ctk.CTkLabel(frame, image=profile_photo, text="")
        profile_label.image = profile_photo  # Keep a reference to avoid garbage collection
        profile_label.grid(row=0, column=0, rowspan=3, padx=20)

        # Developer Info Labels
        name_label = ctk.CTkLabel(frame, text=f"Name: {developer['name']}", font=("Arial", 14))
        name_label.grid(row=0, column=1, sticky="w")

        email_label = ctk.CTkLabel(frame, text=f"Email: {developer['email']}", font=("Arial", 14))
        email_label.grid(row=1, column=1, sticky="w")

        address_label = ctk.CTkLabel(frame, text=f"Address: {developer['address']}", font=("Arial", 14))
        address_label.grid(row=2, column=1, sticky="w")

        return frame

    def make_circle(self, img):
        # Create a circular mask to make the image circular
        size = img.size
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + size, fill=255)
        result = Image.new('RGBA', size)
        result.paste(img, (0, 0), mask)
        return result

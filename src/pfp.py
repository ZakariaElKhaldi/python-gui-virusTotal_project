import os
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
import tkinter as tk
import mysql.connector

class ProfilePicturePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user_info = user
        self.directory = "DefaultImages"
        self.browse_button = "brows_button.png"
        self.next_button = "next_button.png"
        self.default_preview_image = "default_pfp_previeu.png"
        self.user_info.pfp_user = None  # Initialize an instance variable to store the file path

        self.setup_ui()

    def setup_ui(self):
        self.configure(bg="#FFFFFF")
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=512,
            width=384,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.browse_button_img = PhotoImage(file=os.path.join(self.directory, self.browse_button))
        self.next_button_img = PhotoImage(file=os.path.join(self.directory, self.next_button))
        self.default_preview_image = PhotoImage(file=os.path.join(self.directory, self.default_preview_image))

        self.preview_label = self.canvas.create_image(192.0, 256.0, image=self.default_preview_image, anchor='center')

        self.button_browse = Button(
            self,
            image=self.browse_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.browse_file,
            relief="flat"
        )
        self.button_browse.place(
            x=127.0,
            y=446.0,
            width=130.0,
            height=32.0
        )

        self.button_next = Button(
            self,
            image=self.next_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.next_page,  # Change here
            relief="flat"
        )
        self.button_next.place(
            x=127.0,
            y=401.0,
            width=130.0,
            height=30.0
        )

        self.canvas.create_text(
            147.0,
            58.0,
            anchor="nw",
            text="PFP",
            fill="#000000",
            font=("Inter", 48 * -1)
        )

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                self.user_info.pfp_user = file_path  # Store the file path in the instance variable
                circular_photo = self.resize_and_make_circular(file_path, 222)
                self.canvas.itemconfig(self.preview_label, image=circular_photo)
                self.canvas.image = circular_photo  # Keep a reference to prevent garbage collection
            except Exception as e:
                print(f"Error: {e}")

    def resize_and_make_circular(self, image_path, size):
        img = Image.open(image_path)
        img.thumbnail((size, size), Image.LANCZOS)
        img = ImageOps.fit(img, (size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        img.putalpha(mask)
        return ImageTk.PhotoImage(img)
    
    def next_page(self):
        if self.user_info.pfp_user:
            try:
                self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="project_db"
                )

                self.mycursor = self.mydb.cursor()

                query1 = "INSERT INTO pfp_path VALUES (%s, %s)"
                self.mycursor.execute(query1, (self.user_info.id, self.user_info.pfp_user))
                self.mydb.commit()

                print(f"Selected file path: {self.user_info.pfp_user}")
                self.master.show_home_page()

            except Exception as e:
                # Handle exceptions gracefully
                print("Error:", e)
                messagebox.showerror("Error", "An error occurred while processing your request.")
            finally:
                # Close database connection
                if hasattr(self, 'mydb') and self.mydb.is_connected():
                    self.mycursor.close()
                    self.mydb.close()

        else:
            print(f"Selected file path: {self.user_info.pfp_user}")
            messagebox.showwarning("Warning", "Please choose a pfp.")

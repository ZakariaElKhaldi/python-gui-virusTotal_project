import tkinter as tk
from tkinter import Canvas, Button, PhotoImage
import os

class WelcomePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master  # Explicitly assign the master
        self.directory = "DefaultImages"
        self.create_account_button = "creat_account_button.png"
        self.login_button = "wlcome_login_button.png"
        
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

        # Load images
        self.create_account_button_img = PhotoImage(file=os.path.join(self.directory, self.create_account_button))
        self.login_button_img = PhotoImage(file=os.path.join(self.directory, self.login_button))

        self.create_widgets()

    def create_widgets(self):
        self.button_create = Button(
            self,
            image=self.create_account_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_signup,  # Corrected method name
            relief="flat"
        )
        self.button_create.place(
            x=59.0,
            y=256.0,
            width=266.0,
            height=52.0
        )

        self.button_login = Button(
            self,
            image=self.login_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_login,
            relief="flat"
        )
        self.button_login.place(
            x=59.0,
            y=341.0,
            width=266.0,
            height=52.0
        )

        self.canvas.create_text(
            90.0,
            58.0,
            anchor="nw",
            text="Welcome",
            fill="#000000",
            font=("Arial", 48 * -1)  # Changed to Arial for compatibility
        )

        self.canvas.create_text(
            84.0,
            116.0,
            anchor="nw",
            text="To our app: The ultimate file scanning \napplication",
            fill="#484848",
            font=("Arial", 12 * -1)  # Changed to Arial for compatibility
        )

    def go_to_signup(self):  # Corrected method name
        self.master.show_signup_page()

    def go_to_login(self):
        self.master.show_login_page()

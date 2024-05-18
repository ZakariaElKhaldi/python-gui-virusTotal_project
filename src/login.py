import os
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox
import tkinter as tk
import mysql.connector

class LoginPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master

        self.user_info = user

        self.directory = "DefaultImages"
        self.login_button_image = "login_button.png"
        self.signup_text_button_image = "singin_text_image_button.png"
        self.large_text_entry_image = "large_text_enry.png"
        
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
        
        self.text_entry = PhotoImage(file=os.path.join(self.directory, self.large_text_entry_image))
        self.the_login_button = PhotoImage(file=os.path.join(self.directory, self.login_button_image))
        self.signup_button = PhotoImage(file=os.path.join(self.directory, self.signup_text_button_image))
        
        self.login_button = Button(
            self,
            image=self.the_login_button,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.login_button.place(x=63.0, y=412.0, width=266.0, height=52.0)
        
        self.entry_bg_1 = self.canvas.create_image(192.0, 345.0, image=self.text_entry)
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(x=69.0, y=330.0, width=246.0, height=28.0)
        
        self.entry_bg_2 = self.canvas.create_image(192.0, 252.0, image=self.text_entry)
        self.entry_2 = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(x=69.0, y=237.0, width=246.0, height=28.0)
        
        self.canvas.create_text(
            59.0,
            214.0,
            anchor="nw",
            text="Email/Username",
            fill="#000000",
            font=("Inter SemiBold", 15)
        )
        self.canvas.create_text(
            59.0,
            307.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Inter SemiBold", 15)
        )
        self.canvas.create_text(
            130.0,
            58.0,
            anchor="nw",
            text="Login",
            fill="#000000",
            font=("Inter", 48)
        )
        
        self.go_to_signup_button = Button(
            self,
            image=self.signup_button,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_signup,
            relief="flat"
        )
        self.go_to_signup_button.place(x=170.0, y=471.0, width=44.0, height=18.0)

    def login(self):
        self.user_info.u_name = self.entry_2.get()
        self.user_info.password = self.entry_1.get()
    
        try:
            # Connect to the database
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="project_db"
            )
    
            self.mycursor = self.mydb.cursor()
    
            # Check if username and password are correct
            query1 = "SELECT * FROM users WHERE the_user_name = %s AND password = %s"
            self.mycursor.execute(query1, (self.user_info.u_name, self.user_info.password))
            self.result = self.mycursor.fetchone()
    
            if self.result:
                # Retrieve user ID and profile picture path
                query2 = "SELECT ID FROM users WHERE password = %s AND the_user_name = %s"
                self.mycursor.execute(query2, (self.user_info.password, self.user_info.u_name))
                self.user_info.id = self.mycursor.fetchone()[0]
    
                query3 = "SELECT img_path FROM pfp_path WHERE user_id = %s"
                self.mycursor.execute(query3, (self.user_info.id,))
                self.user_info.pfp_user = self.mycursor.fetchone()[0]
    
                # Show the home page
                self.master.show_home_page()
            else:
                # Show a generic message to prevent information disclosure
                messagebox.showinfo("Info", "Invalid username or password.")
        except Exception as e:
            # Handle exceptions gracefully
            print("Error:", e)
            messagebox.showerror("Error", "An error occurred while processing your request.")
        finally:
            # Close database connection
            if hasattr(self, 'mydb') and self.mydb.is_connected():
                self.mycursor.close()
                self.mydb.close()


    def go_to_signup(self):
        self.master.show_signup_page()

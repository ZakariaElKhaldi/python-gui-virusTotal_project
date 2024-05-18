from tkinter import Canvas, Entry, Button, PhotoImage,messagebox
import mysql.connector
import tkinter as tk
import os

class SignupPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master

        self.user_info = user

        self.directory = "DefaultImages"
        self.large_text_entry = "large_text_enry.png"
        self.small_text_entry = "small_text_entry.png"
        self.signup_button_image = "singin_button.png"
        self.login_text_button_image = "login_text_button.png"
        
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

        self.small_text_entry_img = PhotoImage(file=os.path.join(self.directory, self.small_text_entry))
        self.large_text_entry_img = PhotoImage(file=os.path.join(self.directory, self.large_text_entry))
        self.signup_button_img = PhotoImage(file=os.path.join(self.directory, self.signup_button_image))
        self.login_text_button_img = PhotoImage(file=os.path.join(self.directory, self.login_text_button_image))

        self.create_widgets()

    def create_widgets(self):
        self.button_signup = Button(
            self,
            image=self.signup_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.signup,
            relief="flat"
        )
        self.button_signup.place(
            x=63.0,
            y=412.0,
            width=266.0,
            height=52.0
        )

        self.entry_bg_Email = self.canvas.create_image(
            192.0,
            246.0,
            image=self.large_text_entry_img
        )
        self.entry_Email = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_Email.place(
            x=69.0,
            y=231.0,
            width=246.0,
            height=28.0
        )
        self.canvas.create_text(
            59.0,
            208.0,
            anchor="nw",
            text="Email",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.entry_bg_User_name = self.canvas.create_image(
            192.0,
            310.0,
            image=self.large_text_entry_img
        )
        self.entry_User_name = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_User_name.place(
            x=69.0,
            y=295.0,
            width=246.0,
            height=28.0
        )
        self.canvas.create_text(
            59.0,
            272.0,
            anchor="nw",
            text="User name",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.entry_bg_Password = self.canvas.create_image(
            196.0,
            374.0,
            image=self.large_text_entry_img
        )
        self.entry_Password = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_Password.place(
            x=73.0,
            y=359.0,
            width=246.0,
            height=28.0
        )
        self.canvas.create_text(
            63.0,
            336.0,
            anchor="nw",
            text="Password",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.entry_bg_first_name = self.canvas.create_image(
            124.0,
            182.0,
            image=self.small_text_entry_img
        )
        self.entry_first_name = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_first_name.place(
            x=69.0,
            y=167.0,
            width=110.0,
            height=28.0
        )
        self.canvas.create_text(
            59.0,
            144.0,
            anchor="nw",
            text="First name",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.entry_bg_last_name = self.canvas.create_image(
            260.0,
            182.0,
            image=self.small_text_entry_img
        )
        self.entry_last_name = Entry(
            self,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_last_name.place(
            x=205.0,
            y=167.0,
            width=110.0,
            height=28.0
        )
        self.canvas.create_text(
            196.0,
            144.0,
            anchor="nw",
            text="Last name",
            fill="#000000",
            font=("Inter SemiBold", 15 * -1)
        )

        self.canvas.create_text(
            123.0,
            58.0,
            anchor="nw",
            text="Sign Up",
            fill="#000000",
            font=("Inter", 48 * -1)
        )

        self.button_2 = Button(
            self,
            image=self.login_text_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_to_login,
            relief="flat"
        )
        self.button_2.place(
            x=174.0,
            y=471.0,
            width=36.0,
            height=18.0
        )

    def signup(self):
        # Get values from text entries
        self.user_info.u_name = self.entry_User_name.get()
        self.user_info.f_name = self.entry_first_name.get()
        self.user_info.l_name = self.entry_last_name.get()
        self.user_info.email = self.entry_Email.get()
        self.user_info.password = self.entry_Password.get()
    
        # Check if all required fields are filled
        if all([self.user_info.u_name, self.user_info.f_name, self.user_info.l_name, self.user_info.email, self.user_info.password]):
            try:
                # Connect to the database
                self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="project_db"
                )
    
                self.mycursor = self.mydb.cursor()
    
                # Insert user information into the database
                query1 = "INSERT INTO users (first_name,last_name,the_user_name,email,password) VALUES (%s, %s, %s, %s, %s)"
                self.mycursor.execute(query1, (self.user_info.f_name, self.user_info.l_name, self.user_info.u_name, self.user_info.email, self.user_info.password))
                self.mydb.commit()
    
                # Retrieve the user's ID
                query2 = "SELECT ID FROM users WHERE email = %s AND the_user_name = %s"
                self.mycursor.execute(query2, (self.user_info.email, self.user_info.u_name))
                self.user_info.id = self.mycursor.fetchone()[0]
    
                print(self.user_info.u_name)
                print(self.user_info.f_name)
                print(self.user_info.l_name)
                print(self.user_info.email)
                print(self.user_info.password)
                print(self.user_info.id)
    
                # Show the next page
                self.master.show_pfp_page()
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
            # Warn user if not all fields are filled
            messagebox.showwarning("Warning", "Please fill in all the required fields.")



    def go_to_login(self):
        self.master.show_login_page()

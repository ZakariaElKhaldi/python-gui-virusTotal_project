from tkinter import Tk, Canvas, Button, filedialog, simpledialog, messagebox, PhotoImage
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime
import mysql.connector
import requests
import os

class HomePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user_info = user
        self.title = "VirusTotal Scanner"
        self.geometry = "384x512"
        self.configure(bg="#FFFFFF")
        
        self.directory = "DefaultImages"
        self.file_upload_button = "fille_upload_button.png"
        self.url_upload_button = "big_upload_url_button.png"
        self.pfp = self.user_info.pfp_user

        self.api_key = "249bfb34bf7c8d836920725a1f54062d777e4c86126a33439f0eff12db97cc76"

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

        self.button_file_upload = PhotoImage(file=os.path.join(self.directory, self.file_upload_button))
        self.button_url_upload = PhotoImage(file=os.path.join(self.directory, self.url_upload_button))
        self.pfp_img = self.ImageResize(self.pfp)

        self.file_upload = Button(
            self,
            image=self.button_file_upload,
            borderwidth=0,
            highlightthickness=0,
            command=self.scan_file_with_virustotal,
            relief="flat"
        )
        self.file_upload.place(x=59.0, y=196.0, width=266.0, height=52.0)

        self.url_upload = Button(
            self,
            image=self.button_url_upload,
            borderwidth=0,
            highlightthickness=0,
            command=self.scan_url_with_virustotal,
            relief="flat"
        )
        self.url_upload.place(x=59.0, y=315.0, width=266.0, height=52.0)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            384.0,
            64.0,
            fill="#2C2C2C",
            outline=""
        )

        self.the_pfp = self.canvas.create_image(
            35.0,
            31.0,
            image=self.pfp_img
        )

        self.canvas.create_text(
            73.0,
            23.0,
            anchor="nw",
            text=self.user_info.u_name,
            fill="#FFFFFF",
            font=("Inter SemiBold", 15 * -1)
        )

        self.bind("<Map>", lambda event: self.ImageResize(self.pfp))

    def ImageResize(self, pfp):
        if pfp:
            original_pfp_img = Image.open(pfp)
            original_pfp_img.thumbnail((45, 45))  # Resize the image to fit within 45x45
            pfp_img = ImageTk.PhotoImage(original_pfp_img)
        else:
            pfp_img = PhotoImage(file=os.path.join(self.directory, "default_user_icon.png"))
        return pfp_img

    def scan_file_with_virustotal(self):
        file_path = filedialog.askopenfilename(title="Select File")
        if not file_path:
            return
        
        api_url = "https://www.virustotal.com/api/v3/"
        headers = {
            "x-apikey": self.api_key,
            "User-Agent": "vtscan v.1.0",
            "Accept-Encoding": "gzip, deflate",
        }
        
        upload_url = api_url + "files"
        files = {"file": (file_path, open(file_path, "rb"))}
        
        try:
            res = requests.post(upload_url, headers=headers, files=files)
            res.raise_for_status()
            result = res.json()
            file_id = result.get("data").get("id")
            if not file_id:
                messagebox.showerror("Error", "Failed to get file ID from VirusTotal.")
                return
            
            analysis_url = api_url + "analyses/" + file_id
            res = requests.get(analysis_url, headers=headers)
            res.raise_for_status()
            result = res.json()
            stats = result.get("data").get("attributes").get("stats")
            is_malicious = stats.get("malicious") > 0
            
            if is_malicious:
                messagebox.showinfo("Analysis Result", "The file is potentially harmful.")
            else:
                messagebox.showinfo("Analysis Result", "The file seems safe.")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to upload/analyze file: {e}")
        
        self.scantask_file()

    def scan_url_with_virustotal(self):
        url = simpledialog.askstring("Input", "Enter URL:")
        if not url:
            return
        
        api_url = "https://www.virustotal.com/api/v3/"
        headers = {
            "x-apikey": self.api_key,
            "User-Agent": "vtscan v.1.0",
            "Accept-Encoding": "gzip, deflate",
        }
        
        url_upload_url = api_url + "urls"
        data = {"url": url}
        
        try:
            res = requests.post(url_upload_url, headers=headers, data=data)
            res.raise_for_status()
            result = res.json()
            url_id = result.get("data").get("id")
            if not url_id:
                messagebox.showerror("Error", "Failed to get URL ID from VirusTotal.")
                return
            
            analysis_url = api_url + "analyses/" + url_id
            res = requests.get(analysis_url, headers=headers)
            res.raise_for_status()
            result = res.json()
            stats = result.get("data").get("attributes").get("stats")
            is_malicious = stats.get("malicious") > 0
            
            if is_malicious:
                messagebox.showinfo("Analysis Result", "The URL is potentially harmful.")
            else:
                messagebox.showinfo("Analysis Result", "The URL seems safe.")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to upload/analyze URL: {e}")

        self.scantask_url()

    def scantask_url(self):
        if self.user_info.pfp_user:
            try:
                self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="project_db"
                )

                self.mycursor = self.mydb.cursor()
                self.current_datetime = datetime.now()
                query1 = "INSERT INTO history (user_id,task_type,task_date) VALUES (%s, %s, %s)"
                self.mycursor.execute(query1, (self.user_info.id,"url_scan",self.current_datetime))
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

    def scantask_file(self):
        if self.user_info.pfp_user:
            try:
                self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="project_db"
                )

                self.mycursor = self.mydb.cursor()
                self.current_datetime = datetime.now()
                query1 = "INSERT INTO history (user_id,task_type,task_date) VALUES (%s, %s, %s)"
                self.mycursor.execute(query1, (self.user_info.id,"file_scan",self.current_datetime))
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
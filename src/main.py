import tkinter as tk
from welcome import WelcomePage
from signup import SignupPage
from login import LoginPage
from home import HomePage
from pfp import ProfilePicturePage
from loading import AnimatedFrame
from temp_user_info import user_info

class MainController(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.title("Main App")
        
        self.user = user_info()

        self.show_loading_page()

    def show_loading_page(self):
        self.clear_window()
        loading_page = AnimatedFrame(self)
        loading_page.pack(fill="both", expand=True)

    def show_welcome_page(self):
        self.clear_window()
        welcome_page = WelcomePage(self, self.user)
        welcome_page.pack(fill="both", expand=True)

    def show_signup_page(self):
        self.clear_window()
        signup_page = SignupPage(self, self.user)
        signup_page.pack(fill="both", expand=True)

    def show_pfp_page(self):
        self.clear_window()
        pfp_page = ProfilePicturePage(self, self.user)
        pfp_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self.clear_window()
        login_page = LoginPage(self, self.user)
        login_page.pack(fill="both", expand=True)

    def show_home_page(self):
        self.clear_window()
        home_page = HomePage(self, self.user)
        home_page.pack(fill="both", expand=True)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainController()
    app.mainloop()

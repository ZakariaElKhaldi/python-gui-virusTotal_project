import tkinter as tk
from PIL import Image, ImageTk
from itertools import cycle

class AnimatedFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg="#ffffff")
        self.create_widgets()

    def create_widgets(self):
        
        image_path = "DefaultImages/the_app_icon.png"  
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.LANCZOS)  
        self.image = ImageTk.PhotoImage(image)

        # Define your frames
        self.frames = ["█░░░░", "███░░", "████░", "█████"]

        # Create a cycle iterator for frames
        self.cycle_frames = cycle(self.frames)

        # Create a label to display the animation
        self.animation_label = tk.Label(self, text="", fg="#000000", bg="#ffffff", font=("Helvetica", 24))
        self.animation_label.place(relx=0.5, rely=0.6, anchor="center")

        # Counter to track cycles
        self.cycle_counter = 0

        # Start the animation
        self.update_frame()

        
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.place(relx=0.5, rely=0.45, anchor="center")

    # Function to update the frame
    def update_frame(self):
        frame = next(self.cycle_frames)
        self.animation_label.config(text=frame)
        self.after(1000, self.update_frame)  
        if frame == self.frames[-1]:  
            self.cycle_counter += 1
            if self.cycle_counter == 1:  
                self.Next_page()
    
    def Next_page(self):
        self.master.show_welcome_page()

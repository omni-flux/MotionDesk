import multiprocessing
from customtkinter import *
from PIL import Image
import webbrowser
from VRK import VRKeyboard
from VRM import VRMouse

# Initialize VR modules
vr_keyboard = VRKeyboard()
vr_mouse = VRMouse()

def start():
    vr_mouse.start_mouse()
    # You can add any additional logic here for handling mouse functionality

def start_modules():
    # Start the main function in a new process
    process = multiprocessing.Process(target=start)
    process.start()

# Function to open GitHub link
def open_github():
    webbrowser.open("https://github.com/kentuckyfriedkim-chi")  # Replace with your GitHub link

# Hover and click effect functions for buttons
def on_hover(event):
    event.widget.config(fg_color="#7070a0")

def on_leave(event):
    event.widget.config(fg_color="#505080")

if __name__ == '__main__':
    # Initialize main app window
    app = CTk()
    app.title("MotionDesk")
    app.iconbitmap("Intertone-records-logo.ico")
    app.geometry("600x480")
    app.resizable(0, 0)

    # Background image setup
    side_img_data = Image.open("../../MotionDesk/GUI/side-img.png")
    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    # Frame for controls
    frame = CTkFrame(master=app, width=300, height=480, fg_color="#0f1427")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="left")

    # Title label
    CTkLabel(master=frame, text="MotionDesk", text_color="#591f83", anchor="w", font=("Arial Bold", 28)).pack(anchor="w",
                                                                                                              pady=(44, 5),
                                                                                                              padx=(25, 0))

    # GitHub button with improved styling and placement
    info_button = CTkButton(master=frame, text="i", text_color="#591f83", font=("Arial Bold", 14), width=20,
                            height=20,
                            fg_color="#303030", corner_radius=40, command=open_github)
    info_button.place(relx=0.89, rely=0.05)

    # Start Button
    start_button = CTkButton(master=frame, text="Start", font=("Arial Bold", 16), width=240, height=169,corner_radius=40,fg_color="#505080", command=start_modules)
    start_button.pack()
    start_button.bind("<Enter>", on_hover)
    start_button.bind("<Leave>", on_leave)
    start_button.place(relx=0.1, rely=0.2)


    # Run the app
    app.mainloop()
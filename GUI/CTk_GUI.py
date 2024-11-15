from customtkinter import *
from PIL import Image
import webbrowser
from VRK import VRKeyboard
from VRM import VRMouse

# Initialize main app window
app = CTk()
app.title("MotionDesk")
app.iconbitmap("Intertone-records-logo.ico")
app.geometry("600x480")
# noinspection PyTypeChecker
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
(CTkLabel(master=frame, text="MotionDesk", text_color="#7524a6", anchor="w", font=("Arial Bold", 28))
 .pack(anchor="w", pady=(50, 5), padx=(25, 0)))

# Initialize VR modules and state variables
vr_keyboard = VRKeyboard()
vr_mouse = VRMouse()
keyboard_active = False
mouse_active = False

# Functions for button actions


def toggle_keyboard():
    global keyboard_active, mouse_active, vr_keyboard
    if not keyboard_active:
        vr_keyboard.start_keyboard()
        keyboard_active = True
        # Ensure mouse is stopped if it was active
        if mouse_active:
            vr_mouse.end_mouse()
            mouse_active = False
    else:
        vr_keyboard.end_keyboard()
        keyboard_active = False
        # Restart the keyboard module to make it ready for the next toggle
        vr_keyboard = VRKeyboard()  # Reinitialize after stopping


def toggle_mouse():
    global mouse_active, keyboard_active, vr_mouse
    if not mouse_active:
        vr_mouse.start_mouse()
        mouse_active = True
        if keyboard_active:
            vr_keyboard.end_keyboard()
            keyboard_active = False
    else:
        vr_mouse.end_mouse()
        mouse_active = False
        vr_mouse = VRMouse()

# Hover and click effect functions
def on_keyboard_hover(event):
    if not keyboard_active:
        keyboard_button.configure(fg_color="#7070a0")


def on_keyboard_leave(event):
    if not keyboard_active:
        keyboard_button.configure(fg_color="#505080")


def on_mouse_hover(event):
    if not mouse_active:
        mouse_button.configure(fg_color="#7070a0")


def on_mouse_leave(event):
    if not mouse_active:
        mouse_button.configure(fg_color="#505080")


# Buttons for VR Keyboard and VR Mouse
keyboard_button = CTkButton(master=frame, text="Keyboard", fg_color="#505080",font=("Arial Bold", 14), corner_radius=15, height=90, command=toggle_keyboard)
keyboard_button.pack(pady=(10, 5), padx=40, fill="both")
keyboard_button.bind("<Enter>", on_keyboard_hover)
keyboard_button.bind("<Leave>", on_keyboard_leave)

mouse_button = CTkButton(master=frame, text="Mouse", fg_color="#505080",font=("Arial Bold", 14), corner_radius=15, height=90, command=toggle_mouse)
mouse_button.pack(pady=(5, 20), padx=40, fill="both")
mouse_button.bind("<Enter>", on_mouse_hover)
mouse_button.bind("<Leave>", on_mouse_leave)


footer_label = CTkLabel(master=frame, text="Please visit the GitHub page by pressing the 'i' icon at the top to understand all gestures and how to use this app.",wraplength=300,
                        anchor="center",justify="center",text_color="#7A7A7A", font=("Arial", 10))
footer_label.pack(side="bottom", pady=(10, 20), padx=10)


def open_github():
    webbrowser.open("https://github.com/omni-flux/MotionDesk")


info_button = CTkButton(master=frame, text="i", text_color="#a1a9af", font=("Arial Bold", 14), width=20, height=20,
                        fg_color="#303030", corner_radius=40, command=open_github)
info_button.place(relx=0.89, rely=0.05)

# Add a suggestion label at the bottom of the frame
instruction_label = CTkLabel(
    master=frame,
    text="Click on the video feed and press 'Q' to close the modules.",
    text_color="#a0a0a0",
    font=("Arial Bold", 12),
    wraplength=250,
    anchor="center",
    justify="center"
)
instruction_label.pack(side="top", pady=(10, 10), padx=15)


# Run the app
app.mainloop()

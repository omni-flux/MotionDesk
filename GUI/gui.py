from customtkinter import *

from PIL import Image
import customtkinter

app = CTk()
app.title("MotionDesk")
app.iconbitmap("Intertone-records-logo.ico")
app.geometry("600x480")
app.resizable(0,0)

side_img_data = Image.open("../../MotionDesk/GUI/side-img.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#0f1427")
frame.pack_propagate(0)
frame.pack(expand=True, side="left")

CTkLabel(master=frame, text="MotionDesk", text_color="#601E88", anchor="w", justify="right", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

root = customtkinter.CTk()
root.title("MotionDesk.")


app.mainloop()

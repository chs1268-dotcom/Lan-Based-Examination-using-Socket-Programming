# Import Module
from tkinter import *
from PIL import Image, ImageTk
 
# Create Tkinter Object
root = Tk()
root.geometry("500x230")
# Read the Image
image = Image.open("../images/profile.jpeg")
 
# Resize the image using resize() method
resize_image = image.resize((200, 180))
 
img = ImageTk.PhotoImage(resize_image)
 
# create label and add resize image
label1 = Label(image=img)
label1.image = img
label1.place(height=180, width=200,rely=0.1,relx=0.05)
 
# Execute Tkinter
root.mainloop()
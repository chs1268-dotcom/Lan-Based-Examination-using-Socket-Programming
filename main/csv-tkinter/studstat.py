import tkinter as tk
from tkinter import Frame, Pack, filedialog,messagebox,ttk
from types import LambdaType
import pandas as pd

root = tk.Tk()
root.geometry("500x500")
root.pack_propagate(False)
root.resizable(0, 0)

#frame for tree view
frame1 = tk.LabelFrame(root, text="Student Data")
frame1.place(height=250, width=500)

#frame for update button
file_frame = tk.LabelFrame(root, text="Control Panel")
file_frame.place(height=100, width=500,rely=0.5,relx=0)

#buttons
button1 = tk.Button(file_frame,text="Update")
button1.place(rely=0.5, relx=0.47)

#tree view
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1,relwidth=1)

treescrolly = tk.Scrollbar(frame1,orient="vertical",command=tv1.yview)
treescrollx = tk.Scrollbar(frame1,orient="horizontal",command=tv1.xview)

tv1.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set)
treescrollx.pack(side="bottom",fill="x")
treescrolly.pack(side="right",fill="y")






root.mainloop()
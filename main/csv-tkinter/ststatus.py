import tkinter
import csv
from tkinter import Frame, Pack, filedialog,messagebox,ttk
from types import LambdaType


root = tkinter.Tk()
root.geometry("900x320")
root.title("Lan Based Examination Server")



frame1 = tkinter.LabelFrame(root, text="Student Data")
frame1.place(height=320, width=900)






# open file
with open("status.csv", newline = "") as file:
   reader = csv.reader(file)

   # r and c tell us where to grid the labels
   r = 0
   for col in reader:
      c = 0
      for row in col:
         # i've added some styling
         label = tkinter.Label(frame1, width = 15, height = 2, \
                               text = row, relief = tkinter.RIDGE)
         label.grid(row = r, column = c)
         c += 1
      r += 1

root.mainloop()
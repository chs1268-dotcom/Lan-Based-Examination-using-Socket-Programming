from tkinter import *
from tkinter import ttk
import csv
import tkinter

root =Tk()
root.geometry("1050x500")
root.title("Student Credentials Window")
root.resizable(0,0)

filename = "id_passwords.csv"
csvreader = list(csv.DictReader(open(filename)))

#my_tree = ttk.Treeview(root)
frame1 = ttk.LabelFrame(root, text="Student Credentials")
frame1.place(height=390, width=1000,x=25,y=50)
        
treescrolly = ttk.Scrollbar(frame1, orient="vertical")
treescrolly.pack(side="right", fill="y")
        #tree view
tree = ttk.Treeview(frame1, column=("c1", "c2"), show='headings', height=17, yscrollcommand = treescrolly.set)
treescrolly.config(command = tree.yview)

headings = ['Register Number','Password']
# for i in range(len(headings)):
#      tree.column(f"# {i + 1}", anchor=W)
#      tree.heading(f"# {i + 1}", text=headings[i])

# format  the columns
tree.column("c1",width=440,anchor=CENTER)
tree.column("c2",anchor=CENTER,width=440)

#create headings
tree.heading("c1",text="Register Number",anchor=CENTER)
tree.heading("c2",text="Password",anchor=CENTER)
            
#RR_fields = ["Question_ID","Question","Option1","Option2","Option3","Option4","Answer"]
cnt = 1
for i in range(len(csvreader)):
    tree.insert('', 'end', text=cnt, values=( csvreader[i]['id'], csvreader[i]['password']))
    cnt += 1


tree.pack()

root.mainloop()
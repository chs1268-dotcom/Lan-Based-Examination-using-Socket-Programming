import tkinter as tk
from tkinter import *
import time, socket, sys
import csv, os
from _thread import *
import threading
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from tkinter import Frame, Pack, filedialog, messagebox,ttk
from PIL import Image, ImageTk


# event handler for watchdog which will notify whenever change in directory is noticed 
class Event(LoggingEventHandler):
    count = 0
    def on_modified(self, event):
        self.count += 1
        if (self.count == 2):
            app.table()
            self.count = 0
            app.inser_text_in_ter("{ DB_UPDATE_DETECTED } Console has been updated automatically..")


# Tkinter App implementation OO
class App(tk.Tk):
    # Initialization of window
    def __init__(self):
        super().__init__()
        self.title('Server Side')
        self.geometry("1100x600")
        self.pack_propagate(False)
        self.resizable(0, 0)

        #protocol whnever close button in pressed
        self.protocol("WM_DELETE_WINDOW", self.close_window)
    

    def main_window(self):
        label1 = Label(self, text="Welcome!! Host Your Own Exam :)", font=('Helvetica bold', 14, 'bold'))
        label1.place(height=20, width=1050,rely=0.01,relx=0.01)
        
        frame0 = tk.LabelFrame(self, text="Tip")
        frame0.place(height=50, width=1050,rely=0.04,relx=0.02)
        label2 = Label(frame0, bg='#FFFFFF', text="Double Click On A Selected Row To View Student's Credentials OR Student's Response To Questions In Provided Questionaire.", font=('Helvetica bold', 10))
        label2.place(height=20, width=995, rely=0.04,relx=0.02)

        self.table()
        self.terminal()
    

    # heading setup for each column
    def header_setup(self):
        filename3 = "CSV_Files/progress.csv"
        with open(filename3, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            self.RR_fields = next(csvreader)
    

    # whole table setup
    def table(self):
        #frame for tree view
        frame1 = tk.LabelFrame(self, text="Student Data")
        frame1.place(height=390, width=1050,rely=0.13,relx=0.02)
        
        treescrolly = tk.Scrollbar(frame1, orient="vertical")
        treescrolly.pack(side="right", fill="y")
        #tree view
        tree = ttk.Treeview(frame1, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=17, yscrollcommand = treescrolly.set)
        treescrolly.config(command = tree.yview)

        self.tree = tree

        headings = ['Registration ID', 'Exam Started','Exam Finished','Correct Answers', 'Incorrect Answers']
        for i in range(len(headings)):
            tree.column(f"# {i + 1}", anchor=CENTER)
            tree.heading(f"# {i + 1}", text=headings[i])
            
        cnt = 1
        for i in RR:
            tree.insert('', 'end', text=cnt, values=(i, RR[i]['started'], RR[i]['finished'], RR[i]['correct'], RR[i]['wrong']))
            cnt += 1
            tree.bind('<Double-1>', self.selectItem)
        #tree.selection_set(0)
        tree.pack()


    def terminal(self):
        frame3 = tk.LabelFrame(self, text="Status Terminal")
        frame3.place(height=110, width=640,rely=0.79,relx=0.3925)

        scrollbar = Scrollbar(frame3)
        scrollbar.pack( side = RIGHT, fill = Y)
        self.mylist = Listbox(frame3, yscrollcommand = scrollbar.set, bg = "#000000", fg = "#FFFFFF", font=("Terminal", 10))
        #mylist.insert(END, "This is line number " + str(line))
        self.inser_text_in_ter("Press 'Start Server' in control panel to launch your test.")
        self.mylist.place(height=85, width=610,rely=0,relx=0.01)
        scrollbar.config( command = self.mylist.yview)


    def inser_text_in_ter(self, tx):
        self.mylist.delete(END)
        self.mylist.insert(END, " > " + tx)
        self.mylist.insert(END, " > ")
        self.mylist.yview_moveto('1.0')


    def start_server_bt(self):
        self.start_server_button1.config(state = DISABLED)
        self.inser_text_in_ter("Initialized required CSV files..")
        time.sleep(0.5)
        thread_initializer()
        self.table()
        self.inser_text_in_ter('Server has been Started..')


    def about_us_window(self):
        top= Toplevel(self)
        top.title("About Us")
        top.geometry("680x270")
        top.resizable(0, 0)

        l0 = Label(top, text= '[ Lan Based Examination Using Socket Programming ]', font=('Helvetica bold', 16, 'bold'))
        l0.pack()

        l1 = Label(top, text= '', font=('Helvetica bold', 16))
        l1.pack()

        label1 = Label(top, text= '-: Created By :-', font=('Helvetica bold', 11))
        label1.pack()
        label2 = Label(top, text= 'Abhinav Sharma (RA1911003010726)', font=('Helvetica bold', 14))
        label2.pack()
        label3 = Label(top, text= 'Chigilipalli Sriharsha (RA1911003010723)', font=('Helvetica bold', 14))
        label3.pack()
        label4 = Label(top, text= 'Sai Kiran Reddy (RA1911003010721)', font=('Helvetica bold', 14))
        label4.pack()

        l1 = Label(top, text= '', font=('Helvetica bold', 16))
        l1.pack()
        label1 = Label(top, text= '-: Institute Name :-', font=('Helvetica bold', 11))
        label1.pack()
        l0 = Label(top, text= 'SRM Institute Of Science And Technology, Ktr. Chennai', font=('Helvetica bold', 16, 'bold'))
        l0.pack()

        top.mainloop()


    def control_panel(self):
        #frame for update button
        file_frame = tk.LabelFrame(self, text="Control Panel")
        file_frame.place(height=110, width=400,rely=0.79,relx=0.02)
        canvas=Canvas(file_frame,bg='#FFFFFF',width=380,height=80).pack()
        
        #buttons
        button1 = tk.Button(file_frame,text="Manual Update", command=lambda: [self.table(), self.inser_text_in_ter('Console has been updated manually..')])
        button1.place(rely=0.32, relx=0.045)
        self.start_server_button1 = tk.Button(file_frame,text="Start Server", command=lambda: [self.start_server_bt()])
        self.start_server_button1.place(rely=0.32, relx=0.4025)
        button2 = tk.Button(file_frame,text="About Us !!", command=self.about_us_window)
        button2.place(rely=0.32, relx=0.7)


    def show_details(self):
        self.inser_text_in_ter("Credentials shown for " + self.curItem['values'][0])
        top= Toplevel(self)
        top.title("Student Credentials Window")
        top.geometry("680x270")

        top.resizable(0, 0)

        frame0 = tk.LabelFrame(top, text="Student Profile Image")
        frame0.place(height=220, width=230,rely=0.1,relx=0.05)
        # Read the Image
        image = Image.open("images/profile.jpeg")
        # Resize the image using resize() method
        resize_image = image.resize((200, 180))
        img = ImageTk.PhotoImage(resize_image)
        # create label and add resize image
        label1 = Label(frame0, image=img)
        label1.image = img
        label1.place(height=180, width=200,rely=0.05,relx=0.05)


        frame1 = tk.LabelFrame(top, text="Student Details")
        frame1.place(height=130, width=380, rely=0.1, relx=0.4)

        label2 = Label(frame1, text= 'Registration Number :- ' + self.curItem['values'][0], font=('Helvetica bold', 11))
        label2.place(rely=0.1,relx=0.05)
        label3 = Label(frame1, text= 'Name :- Not Availaible', font=('Helvetica bold', 11))
        label3.place(rely=0.28,relx=0.05)
        label4 = Label(frame1, text= 'Specialization :- Not Availaible', font=('Helvetica bold', 11))
        label4.place(rely=0.48,relx=0.05)
        label5 = Label(frame1, text= 'Batch :- Not Availaible', font=('Helvetica bold', 11))
        label5.place(rely=0.68,relx=0.05)


        frame2 = tk.LabelFrame(top, text="Student Credentials")
        frame2.place(height=85, width=380, rely=0.6, relx=0.4)

        label6 = Label(frame2, text= 'Login Id :- ' + self.curItem['values'][0], font=('Helvetica bold', 11))
        label6.place(rely=0.1,relx=0.05)
        label7 = Label(frame2, text= 'Login Password :- ' + PP[self.curItem['values'][0]] + " ", font=('Helvetica bold', 11))
        label7.place(rely=0.45,relx=0.05)
        # Execute Tkinter
        top.mainloop()


    def show_response(self):
        self.inser_text_in_ter("Response shown for " + self.curItem['values'][0])
        top= Toplevel(self)
        top.geometry("1300x230")
        top.title("Student Response Window")
        top.resizable(0, 0)

        # Label(top, text= self.curItem['values'][0], font=('Helvetica bold', 16)).pack()

        tree = ttk.Treeview(top, column=("c1", "c2", "c3", "c4"), show='headings', height=10)
        tree.column("c1",width=70,anchor=CENTER)
        tree.column("c2",anchor=W,width=700)
        tree.column("c3",anchor=W,width=200)
        tree.column("c4",anchor=W,width=300)
        tree.heading("c1",text="Q.no",anchor=CENTER)
        tree.heading("c2",text="Question",anchor=CENTER)
        tree.heading("c3",text="Answer",anchor=CENTER)
        tree.heading("c4",text=self.curItem['values'][0] + " Response", anchor=CENTER)
        cnt = 1
        filename = "CSV_Files/questionaire.csv"
        csvreader = list(csv.DictReader(open(filename)))
        dic = {1 : 'Q1', 2 : 'Q2', 3 : 'Q3', 4 : 'Q4', 5 : 'Q5', 6 : 'Q6', 7 : 'Q7', 8 : 'Q8', 9 : 'Q9', 10 : 'Q10'}
        for i in range(len(csvreader)):
            tree.insert('', 'end', text=cnt, values=(csvreader[i]['Question_ID'], csvreader[i]['Question'], csvreader[i]['Answer'], RR[self.curItem['values'][0]][dic[int(csvreader[i]['Question_ID'])]]))
            cnt += 1

        tree.pack()


    def show_questions(self):
        top= Toplevel(self)
        top.geometry("1000x230")
        top.resizable(0,0)
        top.title("Questionaire Window")
        tree = ttk.Treeview(top, column=("c1", "c2", "c3"), show='headings', height=10)
        tree.column("c1",width=70,anchor=CENTER)
        tree.column("c2",anchor=W,width=700)
        tree.column("c3",anchor=W,width=200)
        tree.heading("c1",text="Q.no",anchor=CENTER)
        tree.heading("c2",text="Question",anchor=CENTER)
        tree.heading("c3",text="Answer",anchor=CENTER)
        cnt = 1
        filename = "CSV_Files/questionaire.csv"
        csvreader = list(csv.DictReader(open(filename)))
        for i in range(len(csvreader)):
            tree.insert('', 'end', text=cnt, values=(csvreader[i]['Question_ID'], csvreader[i]['Question'], csvreader[i]['Answer']))
            cnt += 1

        tree.pack()


    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        self.col = self.tree.identify_column(event.x)
        m = Menu(self, tearoff = 0)
        s = self.curItem['values'][0]
        m.add_command(label ="View Student Credentials", command = lambda: [self.inser_text_in_ter("Credentials requested for " + self.curItem['values'][0] + " .."), self.show_details()])
        m.add_command(label ="View Student Response", command = lambda: [self.inser_text_in_ter("Respone requested for " + self.curItem['values'][0] + " .."), self.show_response()])
        m.add_command(label ="View Questionaire", command = lambda: [self.inser_text_in_ter("Questionaire requested .."), self.show_questions()])
        self.m = m
        m.add_command(label ="Cancel", command = m.pack_forget)
        m.tk_popup(event.x_root, event.y_root)


    def ask_to_quit(self):
        res = messagebox.askquestion('Exit Confirmation', 'Are you sure you want to close the server and exit ?')
        if res == 'yes':
            self.destroy()
            os._exit(0)
        else:
            pass

 
    # closing window action
    def close_window(self):
        self.ask_to_quit()


# CSV initialization
def setting_up_csv():
    filename1 = "CSV_Files/questionaire.csv"
    filename2 = "CSV_Files/id_passwords.csv"
    filename3 = "CSV_Files/progress.csv"
    csvreader1 = csv.DictReader(open(filename1))
    for row in csvreader1:
        QQ.append(row)

    with open(filename2, 'r') as csvfile:
        csvreader2 = csv.reader(csvfile)
        for row in csvreader2:
            PP[row[0]] = str(row[1])
    csvreader3 = csv.DictReader(open(filename3))
    for row in csvreader3:
        RR[row['id']] = {'started' : row['started'], 'finished' : row['finished'], 'Q1' : row['Q1'], 'Q2' : row['Q2'], 'Q3' : row['Q3'], 'Q4' : row['Q4'], 'Q5' : row['Q5'], 'Q6' : row['Q6'], 'Q7' : row['Q7'], 'Q8' : row['Q8'], 'Q9' : row['Q9'], 'Q10' : row['Q10'], 'correct' : row['correct'], 'wrong' : row['wrong']}


# update CSV whenever a change is applied on server side from client
def update_csv():
    filename3 = "CSV_Files/progress.csv"
    with open(filename3, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        RR_fields = next(csvreader)
    with open(filename3, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = RR_fields)
        writer.writeheader()
        tmpdic = []
        for i in RR:
            tmpdic.append({'id' : i, 'started' : RR[i]['started'], 'finished' : RR[i]['finished'], 'Q1' : RR[i]['Q1'], 'Q2' : RR[i]['Q2'], 'Q3' : RR[i]['Q3'], 'Q4' : RR[i]['Q4'], 'Q5' : RR[i]['Q5'], 'Q6' : RR[i]['Q6'], 'Q7' : RR[i]['Q7'], 'Q8' : RR[i]['Q8'], 'Q9' : RR[i]['Q9'], 'Q10' : RR[i]['Q10'], 'correct' : RR[i]['correct'], 'wrong' : RR[i]['wrong']})
        writer.writerows(tmpdic)
    

# questionaire dispenser for seperate threads for different clients
def threaded_client(conn, reg_no):
    try:
        for i in range(len(QQ)):
            time.sleep(0.1)
            conn.send(QQ[i]['Question'].encode())
            time.sleep(0.1)
            conn.send(QQ[i]['Option1'].encode())
            time.sleep(0.1)
            conn.send(QQ[i]['Option2'].encode())
            time.sleep(0.1)
            conn.send(QQ[i]['Option3'].encode())
            time.sleep(0.1)
            conn.send(QQ[i]['Option4'].encode())
            time.sleep(0.1)

        ans = conn.recv(1024).decode()
        dic = {1 : 'Q1', 2 : 'Q2', 3 : 'Q3', 4 : 'Q4', 5 : 'Q5', 6 : 'Q6', 7 : 'Q7', 8 : 'Q8', 9 : 'Q9', 10 : 'Q10'}
        ANS_DICT = {'A' : 'Option1', 'B' : 'Option2', 'C' : 'Option3', 'D' : 'Option4'}

        for i in range(len(ans)):
            if ans[i] == '*':
                RR[reg_no][dic[i + 1]] = "Not Attempted"
                RR[reg_no]['wrong'] = str(int(RR[reg_no]['wrong']) + 1)
            else:
                current_ANS = ANS_DICT[ans[i]]
                RR[reg_no][dic[i + 1]] = QQ[i][current_ANS]
                # receive data stream. it won't accept data packet greater than 1024 bytes
                if QQ[i][current_ANS] ==QQ[i]['Answer']:
                    # result = 'Right answer'
                    # conn.send(result.encode())
                    RR[reg_no]['correct'] = str(int(RR[reg_no]['correct']) + 1)
                else:
                    # result = 'Wrong Answer'
                    # conn.send(result.encode())
                    RR[reg_no]['wrong'] = str(int(RR[reg_no]['wrong']) + 1)
        
        RR[reg_no]['finished'] = 'true'
        
        update_csv()

        app.inser_text_in_ter(f'Registration Number - {reg_no} has finished the test.') 
        conn.close()# close the connection
    except:
        return


# server setup
def setting_up_server():
    # get the hostname
    host = socket.gethostname()
    #host = '127.0.0.1'
    port = 8008  # initiate port no above 1024
    server_socket = socket.socket()  # get instance
    # start the server again if you shut it down, instead of waiting for a minute for TIME_WAIT
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    return server_socket


def start_server(server_socket):
	# configure how many client the server can listen simultaneously
    server_socket.listen(60)
    while True:
        conn, address = server_socket.accept()  # accept new connection	
        s1 = "Enter Your Register Number :- "
        conn.send(s1.encode())
        reg_no = conn.recv(1024).decode()
        time.sleep(0.1)
        s2 = "Enter Your Password :- "
        conn.send(s2.encode())
        passw = conn.recv(1024).decode()

        if (reg_no in PP and PP[reg_no] == passw):
            if RR[reg_no]['started'] == 'true':
                app.inser_text_in_ter(f'Registration Number - {reg_no} is trying to re-access the test.')
                not_allowed = "ALREADY STARTED"
                conn.send(not_allowed.encode())
            else:
                RR[reg_no]['started'] = 'true'
                #q.put((reg_no, 'started'))
                allowed = "ALLOWED"
                conn.send(allowed.encode())
                app.inser_text_in_ter(f'Registration Number - {reg_no} has started the test.')
                update_csv()
        else:
            not_allowed = "NOT ALLOWED"
            conn.send(not_allowed.encode())

        start_new_thread(threaded_client, (conn, reg_no))


def t0(q):
    setting_up_csv()
    server_socket = setting_up_server()
    start_server(server_socket)


def thread_initializer():
    # starting of thread
    thread_0.start()
    thread_1.start()


def t1(q):
    path = 'CSV_Files/progress.csv'
    # Initialize logging event handler
    event_handler = Event()
    # Initialize Observer
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    # Start the observer
    observer.start()
    try:
        while True:
            # Set the thread sleep time
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    # All data will go here
    QQ = []
    PP = dict()
    RR = {}

    global STOP 
    STOP = False

    _sentinel = object()

    q = Queue()
    QUEUE_LENGTH = 0
    # threads announcement
    thread_0 = threading.Thread(target=t0, args=(q,))
    thread_1 = threading.Thread(target=t1, args=(q,))
    # starting tkinter app
    app = App()
    app.header_setup()
    app.main_window()
    app.control_panel()
    app.mainloop()
    # thread_0.join()
    # thread_1.join()
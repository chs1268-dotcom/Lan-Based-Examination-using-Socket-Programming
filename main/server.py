import tkinter as tk
from tkinter import *
import time, socket, sys
import csv, os
from _thread import *
import threading
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from tkinter import Frame, Pack, filedialog,messagebox,ttk



# event handler for watchdog which will notify whenever change in directory is noticed 
class Event(LoggingEventHandler):
    count = 0
    def on_modified(self, event):
        self.count += 1
        if (self.count == 2):
            app.table()
            self.count = 0


# Tkinter App implementation OO
class App(tk.Tk):
    # Initialization of window
    def __init__(self):
        super().__init__()
        self.title('Server Side')
        self.geometry("1100x600")
        self.pack_propagate(False)
        self.resizable(0, 0)
        
        # temporary refresh button
        # b = Button(self, text='Refresh', command=self.table)
        # b.grid(row = 0, column = 9)

        #protocol whnever close button in pressed
        self.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def main_window(self):
        label1 = Label(self, text="Welcome!! Host Your Own Exam :)", font=('Helvetica bold', 14))
        label1.pack()
        
        frame0 = tk.LabelFrame(self, text="Tip")
        frame0.place(height=50, width=1050,rely=0.04,relx=0.02)
        label2 = Label(frame0, text="Double Click On A Selected Row To View Student's Credentials, Student's Response To Questions In Provided Questionaire.", font=('Helvetica bold', 10))
        label2.pack()

        self.table()
    
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
        tree = ttk.Treeview(frame1, column=("c1", "c2", "c3", "c4"), show='headings', height=17, yscrollcommand = treescrolly.set)
        treescrolly.config(command = tree.yview)

        self.tree = tree

        headings = ['Registration ID', 'Exam Started','Exam Finished','Total Score']
        for i in range(len(headings)):
            tree.column(f"# {i + 1}", anchor=CENTER)
            tree.heading(f"# {i + 1}", text=headings[i])
            
        RR_fields = ['started','finished','Q1','Q2','Q3','Q4','Q5','score']
        cnt = 1
        for i in RR:
            tree.insert('', 'end', text=cnt, values=(i, RR[i]['started'], RR[i]['finished'], RR[i]['score']))
            cnt += 1
            tree.bind('<Double-1>', self.selectItem)
        #tree.selection_set(0)
        tree.pack()

    
    def control_panel(self):
        #frame for update button
        file_frame = tk.LabelFrame(self, text="Control Panel")
        file_frame.place(height=100, width=1050,rely=0.79,relx=0.02)
        #buttons
        button1 = tk.Button(file_frame,text="Manual Update", command=self.table)
        button1.place(rely=0.4, relx=0.3)
        button1 = tk.Button(file_frame,text="Start Server")
        button1.place(rely=0.4, relx=0.45)
        button1 = tk.Button(file_frame,text="Close Server")
        button1.place(rely=0.4, relx=0.58)

    def show_details(self):
        top= Toplevel(self)
        top.geometry("750x300")
        top.title("Student Credentials Window")
        Label(top, text= self.curItem['values'][0], font=('Helvetica bold', 16)).pack()


    def show_response(self):
        top= Toplevel(self)
        top.geometry("750x300")
        top.title("Student Response Window")
        Label(top, text= self.curItem['values'][0], font=('Helvetica bold', 16)).pack()


    def show_questions(self):
        top= Toplevel(self)
        top.geometry("750x300")
        top.title("Questionaire Window")
        Label(top, text= self.curItem['values'][0], font=('Helvetica bold', 16)).pack()


    def selectItem(self, event):
        self.curItem = self.tree.item(self.tree.focus())
        self.col = self.tree.identify_column(event.x)
        m = Menu(self, tearoff = 0)
        m.add_command(label ="View Student Credentials", command = self.show_details)
        m.add_command(label ="View Student Response", command = self.show_response)
        m.add_command(label ="View Questionaire", command = self.show_questions)
        self.m = m
        m.add_command(label ="Cancel", command = m.pack_forget)
        m.tk_popup(event.x_root, event.y_root)


    # closing window action
    def close_window(self):
        self.destroy()


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
            PP[row[0]] = row[1]
    csvreader3 = csv.DictReader(open(filename3))
    for row in csvreader3:
        RR[row['id']] = {'started' : row['started'], 'finished' : row['finished'], 'Q1' : row['Q1'], 'Q2' : row['Q2'], 'Q3' : row['Q3'], 'Q4' : row['Q4'], 'Q5' : row['Q5'], 'score' : row['score']}


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
            tmpdic.append({'id' : i, 'started' : RR[i]['started'], 'finished' : RR[i]['finished'], 'Q1' : RR[i]['Q1'], 'Q2' : RR[i]['Q2'], 'Q3' : RR[i]['Q3'], 'Q4' : RR[i]['Q4'], 'Q5' : RR[i]['Q5'], 'score' : RR[i]['score']})
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

            ans = conn.recv(1024).decode()
            dic = {1 : 'Q1', 2 : 'Q2', 3 : 'Q3', 4 : 'Q4', 5 : 'Q5'}
            RR[reg_no][dic[i + 1]] = 'true'
            # receive data stream. it won't accept data packet greater than 1024 bytes
            if QQ[i][ans] ==QQ[i]['Answer']:
                result = 'Right answer'
                conn.send(result.encode())
                RR[reg_no]['score'] = str(int(RR[reg_no]['score']) + 1)
            else:
                result = 'Wrong Answer'
                conn.send(result.encode())
            update_csv()
        RR[reg_no]['finished'] == 'true'    
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
                print('Already Started')
                not_allowed = "NOT ALLOWED"
                conn.send(not_allowed.encode())
            else:
                RR[reg_no]['started'] = 'true'
                #q.put((reg_no, 'started'))
                update_csv()
                allowed = "ALLOWED"
                conn.send(allowed.encode())
                print(f'Registration Number - {reg_no} has started the test.')
        else:
            not_allowed = "NOT ALLOWED"
            conn.send(not_allowed.encode())

        start_new_thread(threaded_client, (conn, reg_no))


def t0(q):
    setting_up_csv()
    server_socket = setting_up_server()
    start_server(server_socket)


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

    _sentinel = object()

    q = Queue()
    QUEUE_LENGTH = 0
    # threads announcement
    thread_0 = threading.Thread(target=t0, args=(q,))
    thread_1 = threading.Thread(target=t1, args=(q,))
    # starting of thread
    thread_0.start()
    thread_1.start()
    # starting tkinter app
    app = App()
    app.header_setup()
    app.main_window()
    app.control_panel()
    app.mainloop()
    # thread_0.join()
    # thread_1.join()
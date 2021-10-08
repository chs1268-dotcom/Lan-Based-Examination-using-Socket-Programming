import tkinter as tk
from tkinter import *
import time, socket, sys
import csv, os
from _thread import *
import threading
from queue import Queue
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# All data will go here
QQ = []
PP = dict()
RR = []

q = Queue()
QUEUE_LENGTH = 0

class Event(LoggingEventHandler):
    def on_modified(self, event):
        push_in_Q(QUEUE_LENGTH)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Test Window')
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()               
        self.geometry("%dx%d" % (width, height))
    
    def header_setup(self):
        filename3 = "CSV_Files/progress.csv"
        with open(filename3, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            self.RR_fields = next(csvreader)
    
    def table(self):
        update_csv()
        total_rows = len(RR)
        total_columns = len(self.RR_fields)
        for j in range(total_columns):
            if j:
                self.e = Entry(self, width=10, fg='blue',font=('Arial',16,'bold'))
            else:
                self.e = Entry(self, width=20, fg='blue',font=('Arial',16,'bold'))
            self.e.grid(row=0, column=j)
            self.e.insert(END, self.RR_fields[j])
        for i in range(total_rows):
            for j in range(total_columns):
                if j:
                    self.e = Entry(self, width=10, fg='blue',font=('Arial',16,'bold'))
                else:
                    self.e = Entry(self, width=20, fg='blue',font=('Arial',16,'bold'))
                self.e.grid(row=i + 1, column=j)
                self.e.insert(END,  RR[i][self.RR_fields[j]])


def setting_up_window(window):
    #window.attributes('-fullscreen', True)
    window.title("Server Side")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width//2}x{screen_height//2}")
    #window.resizable(False, False)


def setting_up_csv():
    filename1 = "CSV_Files/questionaire.csv"
    filename2 = "CSV_Files/id_passwords.csv"
    csvreader1 = csv.DictReader(open(filename1))
    for row in csvreader1:
        QQ.append(row)

    with open(filename2, 'r') as csvfile:
        csvreader2 = csv.reader(csvfile)
        for row in csvreader2:
            PP[row[0]] = row[1]    
    push_in_Q(QUEUE_LENGTH)


def push_in_Q(QUEUE_LENGTH):
    filename3 = "CSV_Files/progress.csv"
    csvreader3 = csv.DictReader(open(filename3))
    for row in csvreader3:
        RR.append(row)
    q.put(RR)
    QUEUE_LENGTH+=1


def update_csv():
    filename3 = "CSV_Files/progress.csv"
    with open(filename3, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        RR_fields = next(csvreader)
    with open(filename3, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = RR_fields)
        writer.writeheader()
        writer.writerows(RR)
    

def threaded_client(conn):
	try:
		while True:
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
				# receive data stream. it won't accept data packet greater than 1024 bytes
				if QQ[i][ans] ==QQ[i]['Answer']:
					result = 'Right answer'
					conn.send(result.encode())
				else:
					result = 'Wrong Answer'
					conn.send(result.encode())
			break		
		conn.close()# close the connection
	except:
		return


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
            for i in RR:
                if i['id'] == reg_no and i['started'] == 'true':
                    print('Already Started')
                    break
                elif i['id'] == reg_no and i['started'] == 'false':
                    i['started'] = 'true'
                    update_csv()
                    break
            allowed = "ALLOWED"
            conn.send(allowed.encode())
            
            print(f'Registration Number - {reg_no} has started the test.')
        else:
            not_allowed = "NOT ALLOWED"
            conn.send(not_allowed.encode())

        start_new_thread(threaded_client, (conn, ))


def display(window):
        window.label.text = q.get()[0]

def chec(window):
    if QUEUE_LENGTH != q.qsize():
        display(window)

def t1():
    app = App()
    app.header_setup()
    app.table()
    app.mainloop()


def t0():
    setting_up_csv()
    server_socket = setting_up_server()
    start_server(server_socket)


def t3():
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
    thread_0 = threading.Thread(target=t0)
    thread_1 = threading.Thread(target=t1)
    thread_3 = threading.Thread(target=t3)
    thread_0.start()
    thread_1.start()
    thread_3.start()
    # thread_0.join()
    # thread_1.join()
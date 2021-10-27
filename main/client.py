from queue import Queue
import threading
from _thread import *
import tkinter as tk
from tkinter import *
import time, socket, sys, os
from tkinter import Frame, Pack, filedialog, messagebox,ttk


class App(tk.Tk):
	# Initialization of window
	def __init__(self):
		super().__init__()
		self.title('Client Side')
		self.W= self.winfo_screenwidth() 
		self.H= self.winfo_screenheight()
		self.geometry("%dx%d" % (self.W, self.H))

		self.pack_propagate(False)
		self.resizable(0, 0)

		#protocol whnever close button in pressed
		self.protocol("WM_DELETE_WINDOW", self.close_window)
		self.q = Queue()
		self.questionaire = []
		self.ANS_STR = {}
		for i in range(1, 11):
			self.ANS_STR[i] = StringVar("")


	def main_window(self):
		label1 = Label(self, text="Welcome!! All The Best For Your Test :)", font=('Helvetica bold', 14, 'bold'))
		label1.place(height=20, width=self.W,rely=0.02,relx=0.01)
		frame0 = tk.LabelFrame(self, text="Instructions")
		frame0.place(height=100, width=self.W - 50,rely=0.06,relx=0.02)
		self.win1()


	def submit(self):
		#thread_0.start()
		name=self.name_var.get()
		password=self.passw_var.get()
		self.name_var.set("")
		self.passw_var.set("")
		self.var1.set(0)

		self.reply1 = name
		self.reply2 = password

		self.connect_to_server()


	def show_hide(self, l):
		if self.var1.get() == 1:
			l.config(show = '*')
		else:
			l.config(show = '')


	def login_win(self):
		self.name_var=tk.StringVar()
		self.passw_var=tk.StringVar()
		self.var1=tk.IntVar(value=1)

		frame0 = tk.LabelFrame(self.frame1, text="Fill Your LogIn Details Here")
		frame0.place(height=320, width=self.W - 200, rely=0.05, relx=0.055)

		self.message_label = tk.Label(frame0, text = '', font=('Helvetica bold', 10)) 
		self.message_label.place(rely=0.3,relx=0.4)

		name_label = tk.Label(frame0, text = 'Student Registration Number', font=('Helvetica bold', 11))  
		name_label.place(rely=0.1,relx=0.1)
		name_entry = tk.Entry(frame0, textvariable = self.name_var, font=('Helvetica bold', 11,'normal'), width=50)
		name_entry.place(rely=0.1,relx=0.4)

		passw_label = tk.Label(frame0, text = 'Password', font = ('Helvetica bold', 11))
		passw_label.place(rely=0.2,relx=0.1)
		passw_entry=tk.Entry(frame0, textvariable = self.passw_var, font = ('Helvetica bold', 11,'normal'), width=34)
		passw_entry.place(rely=0.2,relx=0.4)
		self.show_hide(passw_entry)

		c1 = tk.Checkbutton(frame0, text=' (Hide Password)',variable=self.var1, onvalue=1, offvalue=0, command= lambda: [self.show_hide(passw_entry)])
		c1.place(rely=0.2,relx=0.67)

		login_btn=tk.Button(frame0, text = 'Log In', command = self.submit)
		login_btn.place(rely=0.4,relx=0.5)


	def win1(self):
		self.frame1 = tk.LabelFrame(self, text="Login Page")
		self.frame1.place(height=400, width=self.W - 50,rely=0.21,relx=0.02)
		frame2 = tk.LabelFrame(self, text="Useful Tips")
		frame2.place(height=110, width=self.W - 50, rely=0.75, relx=0.02)

		self.login_win()

	
	def setup_for_success(self):
		self.frame1.destroy()
		self.frame1 = tk.LabelFrame(self, text="Answer the following questions")
		self.frame1.place(height=400, width=self.W - 50,rely=0.21,relx=0.02)

		# self.message_label = tk.Label(self.frame2, text = '', font=('Helvetica bold', 10))
		# self.message_label.place(rely=0.1,relx=0.1)
		self.win2()

	
	def GOOD_TO_SUBMIT(self):
		for i in range(1, 11):
			if self.ANS_STR[i].get() == "":
				return False
		return True


	def ENABLE_MY_BUTTON(self):
		if self.GOOD_TO_SUBMIT():
			self.sub_btn.config(state=NORMAL)


	def send_it(self):
		ANS_STR = ""
		for i in range(1, 11):
			ANS_STR += str(self.ANS_STR[i].get())
		
		self.client_socket.send(ANS_STR.encode())
		self.client_socket.close()  # close the connection

		res = messagebox.showinfo('Good Bye !!', 'Test has been submitted successfully. Press OK to exit.')
		if res == 'ok':
			self.destroy()
			os._exit(0)


	def win2(self):
		style = ttk.Style()
		style.configure('TNotebook.Tab', padding = [35, 8])

		notebook = ttk.Notebook(self.frame1)
		FRAME_LIST = []
		for i in range(10):
			k = ttk.Frame(notebook)
			FRAME_LIST.append(k)
			notebook.add(k, text='Q' + str(i + 1))

		notebook.place(height=320, width=self.W - 195, relx=0.05, rely=0.055)

		q_no = 1
		for i in self.questionaire:
			REL_Y = 0.1
			frame = FRAME_LIST[q_no - 1]
			name_label = tk.Label(frame, text = 'Q' + str(q_no) + '. ' + i['ques'], font=('Helvetica bold', 12))
			name_label.place(rely=REL_Y,relx=0.1)

			v = StringVar("")
			REL_Y += 0.20
			r = Radiobutton(frame, text = i['Option1'], variable = self.ANS_STR[q_no], value = 'A', font=('Helvetica bold', 12), command=self.ENABLE_MY_BUTTON)
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option2'], variable = self.ANS_STR[q_no], value = 'B', font=('Helvetica bold', 12), command=self.ENABLE_MY_BUTTON)
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option3'], variable = self.ANS_STR[q_no], value = 'C', font=('Helvetica bold', 12), command=self.ENABLE_MY_BUTTON)
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option4'], variable = self.ANS_STR[q_no], value = 'D', font=('Helvetica bold', 12), command=self.ENABLE_MY_BUTTON)
			r.place(rely=REL_Y, relx=0.1)
			q_no += 1

		review = ttk.Frame(notebook)
		notebook.add(review, text='Review')

		self.sub_btn=tk.Button(review, text = 'Submit Your Answer', command = self.send_it, state=DISABLED)
		self.sub_btn.place(rely=REL_Y,relx=0.5)


	def ask_to_quit(self):
		res = messagebox.askquestion('Exit Confirmation', 'Are you sure you want to exit ?')
		if res == 'yes':
			self.destroy()
			os._exit(0)
		else:
			pass


	# closing window action
	def close_window(self):
		self.ask_to_quit()


	def connect_to_server(self):
		host = socket.gethostname()  # as both code is running on same pc
		#host = '127.0.0.1'
		port = 8008  # socket server port number

		self.client_socket = socket.socket()  # instantiate
		self.client_socket.connect((host, port))  # connect to the server

		request1 = self.client_socket.recv(1024).decode()
		self.client_socket.send(self.reply1.encode())
		request2 = self.client_socket.recv(1024).decode()
		self.client_socket.send(self.reply2.encode())

		permission = self.client_socket.recv(1024).decode()
		if permission == "NOT ALLOWED":
			self.message_label.config(text = "(** Invalid ID/Password )", foreground="red")
			self.client_socket.close()
			return
		elif permission == "ALREADY STARTED":
			self.message_label.config(text = "(** Test has already been accessed by you, contact your course faculty. )", foreground="red")
			self.client_socket.close()
			return


		for i in range(10):
			dic = {}

			s = self.client_socket.recv(1024).decode()
			dic['ques'] = s
			#print('Question ' + str(i+1) + ' :- ' + Question)
			
			Option1 = self.client_socket.recv(1024).decode()
			#print('A.' + Option1)
			dic['Option1'] = Option1

			Option2 = self.client_socket.recv(1024).decode()
			#print('B.' + Option2)
			dic['Option2'] = Option2

			Option3 = self.client_socket.recv(1024).decode()
			#print('C.' + Option3)
			dic['Option3'] = Option3

			Option4 = self.client_socket.recv(1024).decode()
			#print('D.' + Option4)
			dic['Option4'] = Option4

			self.questionaire.append(dic)
			#self.win2('Q' + str(i+1) + ". " + Question, options)


		# ANS_STR = "AAAAAAAAAA"
		# self.client_socket.send(ANS_STR.encode())

		# self.client_socket.close()  # close the connection

		self.setup_for_success()


# def t0():
#     client_program()


if __name__ == '__main__':
	# threads announcement
	#thread_0 = threading.Thread(target=t0)
	# starting tkinter app
	app = App()
	app.main_window()
	app.mainloop()
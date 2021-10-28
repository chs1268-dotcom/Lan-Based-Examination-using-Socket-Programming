from queue import Queue
import threading
from _thread import *
import tkinter as tk
from tkinter import *
import time, socket, sys, os
from tkinter import Frame, Pack, filedialog, messagebox,ttk
from PIL import Image, ImageTk



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
		self.TEST_START = 'NO'
		self.ANS_STR = {}
		for i in range(1, 11):
			self.ANS_STR[i] = StringVar("")


	def main_window(self):
		label1 = Label(self, text="Welcome!! All The Best For Your Test :)", font=('Helvetica bold', 14, 'bold'))
		label1.place(height=20, width=self.W,rely=0.02,relx=0.01)
		frame0 = tk.LabelFrame(self, text="Instructions")
		frame0.place(height=100, width=self.W - 50,rely=0.06,relx=0.02)
		
		label2 = Label(frame0, bg='#FFFFFF', text="1. Enter your Registration Number and Password (provided by respective course faculty).										", font=('Helvetica bold', 10))
		label2.place(height=20, width=self.W - 100, rely=0.05,relx=0.015)
		label3 = Label(frame0, bg='#FFFFFF', text="2. Do not close window during test. This test is only One-Time Accessible.												", font=('Helvetica bold', 10))
		label3.place(height=20, width=self.W - 100, rely=0.3,relx=0.015)
		label4 = Label(frame0, bg='#FFFFFF', text="3. Review window is availaible at the end of the test. Submit Button will be enabled only when all questions are attempted.							", font=('Helvetica bold', 10))
		label4.place(height=20, width=self.W - 100, rely=0.55,relx=0.015)

		self.win1()


	def submit(self):
		#thread_0.start()
		name=self.name_var.get()
		password=self.passw_var.get()
		self.name_var.set("")
		self.passw_var.set("")
		self.var1.set(1)

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

		image = Image.open("images/login_img2.jpg")
		resize_image = image.resize((350, 250))
		img = ImageTk.PhotoImage(resize_image)
		# create label and add resize image
		label1 = Label(frame0, image=img)
		label1.image = img
		label1.place(height=250, width=350,rely=0.075,relx=0.03)

		left_margin = 0.425

		self.message_label = tk.Label(frame0, text = '', font=('Helvetica bold', 10))
		self.message_label.place(rely=0.1,relx=left_margin)

		name_label = tk.Label(frame0, text = 'Student Registration Number', font=('Helvetica bold', 11))  
		name_label.place(rely=0.2,relx=left_margin)
		name_entry = tk.Entry(frame0, textvariable = self.name_var, font=('Helvetica bold', 11,'normal'), width=60)
		name_entry.place(rely=0.3,relx=left_margin)

		passw_label = tk.Label(frame0, text = 'Password (as provided by respective course faculty)', font = ('Helvetica bold', 11))
		passw_label.place(rely=0.4,relx=left_margin)
		passw_entry=tk.Entry(frame0, textvariable = self.passw_var, font = ('Helvetica bold', 11,'normal'), width=60)
		passw_entry.place(rely=0.5,relx=left_margin)
		self.show_hide(passw_entry)

		c1 = tk.Checkbutton(frame0, text=' (Hide Password)',variable=self.var1, onvalue=1, offvalue=0, command= lambda: [self.show_hide(passw_entry)])
		c1.place(rely=0.6,relx=left_margin)

		login_btn=tk.Button(frame0, text = 'Log In', command = self.submit)
		login_btn.place(rely=0.7,relx=left_margin)


	def win1(self):
		self.frame1 = tk.LabelFrame(self, text="Login Page")
		self.frame1.place(height=400, width=self.W - 50,rely=0.21,relx=0.02)
		frame2 = tk.LabelFrame(self, text="Useful Tips")
		frame2.place(height=110, width=self.W - 50, rely=0.75, relx=0.02)

		label2 = Label(frame2, bg='#FFFFFF', text="1. There are 10 Multiple Choice Questions in this test. All questions are compulsory	.										", font=('Helvetica bold', 10))
		label2.place(height=20, width=self.W - 100, rely=0.05,relx=0.015)
		label3 = Label(frame2, bg='#FFFFFF', text="2. This test is only One-Time Accessible. If you try to access the test again, concerned faculty will be alerted regarding the same.						", font=('Helvetica bold', 10))
		label3.place(height=20, width=self.W - 100, rely=0.25,relx=0.015)
		label4 = Label(frame2, bg='#FFFFFF', text="3. Review window is availaible at the end of the test. Submit Button will be enabled only when all questions are attempted.							", font=('Helvetica bold', 10))
		label4.place(height=20, width=self.W - 100, rely=0.45,relx=0.015)
		label5 = Label(frame2, bg='#FFFFFF', text="4. There are no partial marks and no negative marking.														", font=('Helvetica bold', 10))
		label5.place(height=20, width=self.W - 100, rely=0.65,relx=0.015)

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
			s = self.ANS_STR[i].get()
			if s == "":
				ANS_STR += "*"
			else:
				ANS_STR += str(self.ANS_STR[i].get())

		self.client_socket.send(ANS_STR.encode())
		self.client_socket.close()  # close the connection

		res = messagebox.showinfo('Good Bye !!', 'Test has been submitted successfully. Press OK to exit.')
		if res == 'ok':
			self.destroy()
			os._exit(0)


	def UPDATE_REVIEW(self):
		#tree view
		new_frame = tk.LabelFrame(self.review, text="Current Answer Status")
		new_frame.place(height=255, width=425,rely=0.047,relx=0.02)

		tree = ttk.Treeview(new_frame, column=("c1", "c2"), show='headings', height=10)
		headings = ['Question Number', 'Status']
		for i in range(len(headings)):
			tree.column(f"# {i + 1}", anchor=CENTER)
			tree.heading(f"# {i + 1}", text=headings[i])

		for i in range(1, 11):
			s = self.ANS_STR[i].get()
			if s == "":
				tree.insert('', 'end', text=i, values=('Q.' + str(i), "Not attempted yet."))
			else:
				tree.insert('', 'end', text=i, values=('Q.' + str(i), "Answer Saved"))
		tree.pack()


	def win2(self):
		style = ttk.Style()
		style.configure('TNotebook.Tab', padding = [35, 8], background = [("white")])

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

			c = Canvas(frame, bg="white", height=250, width=self.W - 250)
			c.place(rely=0.05, relx=0.025)

			name_label = tk.Label(frame, text = 'Q' + str(q_no) + '. ' + i['ques'], font=('Helvetica bold', 12), background="white")
			name_label.place(rely=REL_Y,relx=0.1)

			v = StringVar("")
			REL_Y += 0.20
			r = Radiobutton(frame, text = i['Option1'], variable = self.ANS_STR[q_no], value = 'A', background="white", border=0, font=('Helvetica bold', 12), command= lambda : [self.ENABLE_MY_BUTTON(), self.UPDATE_REVIEW()])
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option2'], variable = self.ANS_STR[q_no], value = 'B', background="white", font=('Helvetica bold', 12), command= lambda : [self.ENABLE_MY_BUTTON(), self.UPDATE_REVIEW()])
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option3'], variable = self.ANS_STR[q_no], value = 'C', background="white", font=('Helvetica bold', 12), command= lambda : [self.ENABLE_MY_BUTTON(), self.UPDATE_REVIEW()])
			r.place(rely=REL_Y, relx=0.1)
			REL_Y += 0.15
			r = Radiobutton(frame, text = i['Option4'], variable = self.ANS_STR[q_no], value = 'D', background="white", font=('Helvetica bold', 12), command= lambda : [self.ENABLE_MY_BUTTON(), self.UPDATE_REVIEW()])
			r.place(rely=REL_Y, relx=0.1)
			q_no += 1

		review = ttk.Frame(notebook)
		notebook.add(review, text='Review')
		c = Canvas(review, bg="white", height=250, width=self.W - 250)
		c.place(rely=0.05, relx=0.02)
		self.review = review
		self.UPDATE_REVIEW()

		self.sub_btn=tk.Button(review, text = 'Submit Your Answers And Exit', command = self.send_it, state=DISABLED)
		self.sub_btn.place(rely=0.4,relx=0.62)


	def ask_to_quit(self):
		res = messagebox.askquestion('Exit Confirmation', 'Are you sure you want to exit ?')
		if res == 'yes' and self.TEST_START == 'YES':
			self.send_it()
		elif res == 'yes' and self.TEST_START == 'NO':
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

		self.TEST_START = "YES"

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
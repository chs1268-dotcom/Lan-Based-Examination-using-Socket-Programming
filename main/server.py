import time, socket, sys
import csv
from _thread import *


filename1 = "CSV_Files/questionaire.csv"
filename2 = "CSV_Files/id_passwords.csv"
QQ = []
PP = dict()
with open(filename1, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        mydict = {}
        for i in range(len(row)):
            mydict[fields[i]] = row[i]
        QQ.append(mydict)

with open(filename2, 'r') as csvfile:
	csvreader = csv.reader(csvfile)
	fields = next(csvreader)
	for row in csvreader:
		PP[row[0]] = row[1]

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

def server_program():
	# get the hostname
	host = socket.gethostname()
	#host = '127.0.0.1'
	port = 8008  # initiate port no above 1024
	
	server_socket = socket.socket()  # get instance
	# look closely. The bind() function takes tuple as argument
	server_socket.bind((host, port))  # bind host address and port together
	
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
			allowed = "ALLOWED"
			conn.send(allowed.encode())
			print(f'Registration Number - {reg_no} has started the test.')
		else:
			not_allowed = "NOT ALLOWED"
			conn.send(not_allowed.encode())

		start_new_thread(threaded_client, (conn, ))


if __name__ == '__main__':
	server_program()
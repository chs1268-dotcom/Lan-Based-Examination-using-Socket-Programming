import time, socket, sys
import csv
from _thread import *


filename = "CSV_Files/questionaire.csv"
QQ = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        mydict = {}
        for i in range(len(row)):
            mydict[fields[i]] = row[i]
        QQ.append(mydict)


def threaded_client(conn):
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
		print("Connection from: " + str(address))
		start_new_thread(threaded_client, (conn, ))


if __name__ == '__main__':
	server_program()
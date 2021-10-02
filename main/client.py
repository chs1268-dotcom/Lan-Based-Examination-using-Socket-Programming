import time, socket, sys

def client_program():
	host = socket.gethostname()  # as both code is running on same pc
	#host = '127.0.0.1'
	port = 8008  # socket server port number

	client_socket = socket.socket()  # instantiate
	client_socket.connect((host, port))  # connect to the server

	ANS_DICT = {'A' : 'Option1', 'B' : 'Option2', 'C' : 'Option3', 'D' : 'Option4'}

	request1 = client_socket.recv(1024).decode()
	reply1 = input(request1)
	client_socket.send(reply1.encode())
	request2 = client_socket.recv(1024).decode()
	reply2 = input(request2)
	client_socket.send(reply2.encode())

	permission = client_socket.recv(1024).decode()
	if permission == "NOT ALLOWED":
		print("Invalid ID/Password")
		client_socket.close()
		return

	for i in range(5):
		Question = client_socket.recv(1024).decode()
		print('Question ' + str(i+1) + ' :- ' + Question)
		Option1 = client_socket.recv(1024).decode()
		print('A.' + Option1)
		Option2 = client_socket.recv(1024).decode()
		print('B.' + Option2)
		Option3 = client_socket.recv(1024).decode()
		print('C.' + Option3)
		Option4 = client_socket.recv(1024).decode()
		print('D.' + Option4)
		print()
		ans = input(str("Answer : "))  # take input
		client_socket.send(ANS_DICT[ans].encode())
		print()
		result = client_socket.recv(1024).decode()
		print('Result : ' + result)
		print()
		print()

	client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()
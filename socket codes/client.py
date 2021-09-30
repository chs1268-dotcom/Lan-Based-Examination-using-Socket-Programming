
import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5002  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    data = client_socket.recv(1024).decode()  # receive response   
    print( data)  # show in terminal
   
    data = client_socket.recv(1024).decode()  # receive response   
    print( data)  # show in terminal
   
    
    message = input("-> ")  # take input

    while message != 'end':
        
        
        
        client_socket.send(message.encode())  # send message
        data1 = client_socket.recv(1024).decode()  # receive response
        print('Result : ' + data1)  # show in terminal
        data = client_socket.recv(1024).decode()  # receive response   
        print( data)  # show in terminal
        data = client_socket.recv(1024).decode()  # receive response   
        print( data)  # show in terminal
        message = input("-> ")  # again take input
      
    


    client_socket.close()  # close the connection
   

if __name__ == '__main__':
    client_program()



import socket


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5002  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    Question1 = 'What is the colour of sky?'
    options = 'A.Red   B.Blue   C.Green   D.Yellow'

    conn.send(Question1.encode())  # send data to the client
    conn.send(options.encode())  # send data to the client
            
    if True:
        data1 = conn.recv(1024).decode()

        # receive data stream. it won't accept data packet greater than 1024 bytes
        if data1.upper() =='B':
            result1 = 'Right answer'
            conn.send(result1.encode())
        else:
            result2 = 'Wrong Answer'
            conn.send(result2.encode())    
        

        print("Answer from student: " + str(data1))

    Question2 = 'What is the colour of rose?'
    options = 'A.Red   B.Blue   C.Green   D.Yellow'    
    
    conn.send(Question2.encode())  # send data to the client
    conn.send(options.encode())  # send data to the client
            
    if True:
        data1 = conn.recv(1024).decode()

        # receive data stream. it won't accept data packet greater than 1024 bytes
        if data1.upper() =='A':
            result1 = 'Right answer'
            conn.send(result1.encode())
        else:
            result2 = 'Wrong Answer'
            conn.send(result2.encode())    
        

        print("Answer from student: " + str(data1))

    
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()


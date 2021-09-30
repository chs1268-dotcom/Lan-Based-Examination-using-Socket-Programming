import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print('What is the colour of sky?')
    print('A.Red')
    print('B.Blue')
    print('C.Green')
    print('D.Yellow')
    message = input("-> ")  # take input
    

    if message == 'B':
        print('Right answer')
    else:
        print('Wrong answer')  
    client_socket.send(message.encode())  # send message     
    #second q
    print('What is the colour of rose?')
    print('A.Red')
    print('B.Blue')
    print('C.Green')
    print('D.Yellow')
    message1 = input("-> ")  # take input
    

    if message1 == 'A':
        print('Right answer')
    else:
        print('Wrong answer')  
    client_socket.send(message1.encode())  # send message      
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
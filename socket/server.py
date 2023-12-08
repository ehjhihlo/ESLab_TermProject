# -*- coding: utf-8 -*-
import socket
HOST = '192.168.0.16'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)
print("start server")
import base64






while True:
    conn, addr = server.accept()
    clientMessage = str(conn.recv(1024), encoding='utf-8')
    
    clientMessage = clientMessage.strip().split('d')
    photoString=''
    for i in range(0,len(clientMessage)):
        photoString+=clientMessage[i]
    imgdata = base64.b64decode(photoString)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)    
    print('Client message is:', clientMessage)

    serverMessage = 'I\'m here!'
    conn.sendall(serverMessage.encode())
    conn.close()
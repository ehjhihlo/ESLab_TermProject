import socket

HOST = '192.168.0.16'
PORT = 8000
photo_array=[1,2,3,4]

def socket_to_server(photo_array):    
    Message =''
    for i in photo_array:
        Message = Message+str(i)+ 'd'
    return Message
        
clientMessage=socket_to_server(photo_array)
print(clientMessage)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(clientMessage.encode())

serverMessage = str(client.recv(1024), encoding='utf-8')
print('Server:', serverMessage)

client.close()
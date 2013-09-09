
import socket

host = '158.130.158.227'
port = 5001
backlog = 5
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, adress = s.accept()
    data = client.recv(size)
    if data:
        print str(data)
        client.send(data)
    client.close()

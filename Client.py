import socket
s = socket.socket()
host = "192.168.0.14" #Raspberry pi ip server
port = 5000
s.connect((host, port))
print(s.recv(1024))
s.close()
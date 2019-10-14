
import socket
import sys

def decrypt(data, k):
    alphabet = dict()
    for i in range(26):
        alphabet[chr(i+65)] = chr(((i-k)%26)+65)
    for i in range(26):
        alphabet[chr(i+97)] = chr(((i-k)%26)+97)
    alphabet[' '] = ' '
    return ''.join(map(lambda e: alphabet[e], list(data)))
    

port = int(input("Enter port number to start server on: "))
try:
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(10)
except socket.error as e:
    print(e)
    sys.exit(1)

while True:
    client, addr = server.accept()
    print("Connection from",addr)
    recieved = client.recv(4096).decode('utf-8')
    k = int(recieved.split(' ')[0])
    enc_data = ' '.join((recieved.split(' ')[1:]))
    print("Data recieved:", enc_data)
    dec_data = decrypt(enc_data, k)
    print("Decrypted data:",dec_data)
    client.close()
#     break
server.close()

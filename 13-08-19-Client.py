
# coding: utf-8

# In[65]:


import socket 
import sys


# In[69]:


def encrypt(data, k):
    alphabet = dict()
    for i in range(26):
        alphabet[chr(i+65)] = chr(((i+k)%26)+65)
    for i in range(26):
        alphabet[chr(i+97)] = chr(((i+k)%26)+97)    
    alphabet[' '] = ' '
    return ''.join(map(lambda e: alphabet[e],list(data)))


# In[70]:


port = int(input("Enter the port number of server: "))


# In[71]:


try: 
    client = socket.socket()
    client.connect(('127.0.0.1', port))
    data = input("Enter the data: ")
    k = int(input("Enter key: "))
    client.send(bytes(str(k)+ ' '+encrypt(data, k), 'utf-8'))
    client.close()
except socket.error as e:
    print(e)


import hashlib
import json
import pickle
import socket
import threading
import time
import uuid

from commons import MANAGER_PORT, SERVER_PORT
from transaction_pool import TransactionPool


class ManagerPeer:
    def __init__(self, ip):
        self.peer_set = set()
        self.MANAGER_IP = ip
        self.MANAGER_PORT = MANAGER_PORT
        self.server_port = SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.stop_server = False
        self.transaction_pool = TransactionPool()

    def start_server(self):
        self.server_socket.bind((self.MANAGER_IP, self.MANAGER_PORT))
        self.server_socket.listen(100)
        print(f"Listening at port {self.MANAGER_PORT}")
        while True:
            if self.stop_server:
                break

            client_peer, address = self.server_socket.accept()
            print(f"incoming connection from {address}")
            recieved_request = client_peer.recv(4096).decode('utf-8')
            ip = recieved_request.split()[1]

            if recieved_request.startswith("add"):
                self.inform_peers(recieved_request)
                client_peer.send(pickle.dumps(self.peer_set))
                self.peer_set.add(ip)
                print(f"added {ip}")

            elif recieved_request.startswith('remove'):
                self.peer_set.remove(ip)
                self.inform_peers(recieved_request)
                print(f"removed {ip}")

            elif recieved_request.startswith('update-transactionpool'):
                new_transactionpool = client_peer.recv(4096)
                self.transaction_pool = pickle.loads(new_transactionpool)

            elif recieved_request.startswith('get-transactionpool'):
                client_peer.send(pickle.dumps(self.transaction_pool))

            client_peer.close()
        self.server_socket.close()

    def _stop_server(self):
        self.stop_server = True

    def inform_peers(self, message):
        operation, new_peer = message.split()
        for peer in self.peer_set:
            client_socket = socket.socket()
            client_socket.settimeout(30)
            try:
                client_socket.connect((peer, self.server_port))
                client_socket.send(
                    f"{operation}-peer {new_peer}".encode('utf-8'))
                print(f"Sent to {peer}")
            except Exception as e:
                print(e)
                print(f"{operation}-peer {peer}")
            finally:
                client_socket.close()

    def __repr__(self):
        return f'{self.MANAGER_IP} {self.MANAGER_PORT}\nPeers: '+' '.join(self.peer_set)

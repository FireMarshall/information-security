import hashlib
import pickle
import socket
import threading

from ecdsa import SigningKey

from commons import MANAGER_PORT, SERVER_PORT

# client side


class Peer:

    def __init__(self, ip):
        self.MANAGER_IP = '192.168.1.106'
        self.MANAGER_PORT = MANAGER_PORT
        self.server_port = SERVER_PORT
        self.client_ip = ip
        self.server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, 0)
        self.blockchain = list()
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.stop_server = False
        self.peers = list()
        self.balance = 0

    def start_server(self):
        self.server_socket.bind((self.client_ip, self.server_port))
        self.server_socket.listen(100)
        while True:
            client_peer, address = self.server_socket.accept()
            # actions
            data = client_peer.recv(4096).decode('utf-8')
            # add
            if data.startswith('add-peer'):
                self.peers.add(data.split()[1])
            elif data.startswith('remove-peer'):
                self.peers.remove(data.split()[1])
            else:
                transaction_obj = pickle.loads(client_peer.recv(4096))
                new_block = Block(transaction_obj)
                self.blockchain.append(new_block)
        self.server_socket.close()

    def _stop_server(self):
        self.stop_server = True

    def _inform_manager_add(self, message):
        sock = socket.socket()
        sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
        sock.send(message.encode('utf-8'))
        peers = pickle.loads(sock.recv(4096))
        self.peers = peers

    def _inform_manager_delete(self, message):
        sock = socket.socket()
        sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
        sock.send(message.encode('utf-8'))

    def leave_network(self):
        return self._inform_manager_delete(f"remove {self.client_ip}")

    def join_network(self):
        return self._inform_manager_add(f'add {self.client_ip}')

    def update_balance(self, amount):
        self.balance = amount

    def do_transaction(self, fromm, to, amount):
        if amount > self.balance:
            print("Not allowed")
            # actions
        else:
            self.balance -= amount
            message = str(fromm) + str(to) + str(amount)
            public_key = SigningKey.generate()  # uses NIST192p
            secret_key = public_key.get_verifying_key()
            signature = public_key.sign(message.encode('utf-8'))
            transaction_obj = Transaction(fromm, to, amount, signature)
            new_block = Block(transaction_obj)
            self.blockchain.append(new_block)
            for peer in self.peers:
                sock = socket.socket()
                try:
                    sock.connect((peer, self.server_port))
                    sock.send("something".encode("utf-8"))
                    sock.send(pickle.dumps(transaction_obj))
                except Exception as e:
                    print(peer)
                    print(e)
                finally:
                    sock.close()

    def mine_transaction(self):
        pass

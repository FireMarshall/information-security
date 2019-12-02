import hashlib
import pickle
import socket
import threading
import time
from ecdsa import SigningKey

from block.block import Block
from blockchain.blockchain import Blockchain
from commons import MANAGER_IP, MANAGER_PORT, SERVER_PORT
from transaction.transaction import Transaction
from transaction_pool.transaction_pool import TransactionPool
from wallet.wallet import Wallet

# client side

class Peer:
    
    def __init__(self, ip):
        self.MANAGER_IP = MANAGER_IP
        self.MANAGER_PORT = MANAGER_PORT
        self.server_port = SERVER_PORT
        self.client_ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.stop_server = False
        self.peers = set()
        self.blockchain = Blockchain()
        self.wallet = Wallet(self.blockchain)
        self.transaction_pool = TransactionPool()
       
    
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
            
            elif data.startswith('sync-chain'):
                blockchain_recieved = pickle.loads(client_peer.recv(4096))
                self.blockchain.replace_chain(blockchain_recieved)
            
            elif data.startswith('add-block'):
                block = pickle.loads(client_peer.recv(4096))
                potential_chain = self.blockchain.chain[:]
                potential_chain.append(block)
                try:
                    self.blockchain.replace_chain(potential_chain)
                    self.transaction_pool.clear_blockchain_transactions(
                        self.blockchain
                    )
                    sock = socket.socket()
                    sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
                    sock.send("update-transactionpool".encode('utf-8'))
                    sock.send(pickle.dumps(self.transaction_pool))
                    sock.close()
                    print('\n -- Successfully replaced the local chain')
                except Exception as e:
                    print(f'\n -- Did not replace chain: {e}')

            
            elif data.startswith('add-transaction'):
                print("Adding trasaction")
                new_transaction = client_peer.recv(4096)
                print("Recieved")
                self.transaction_pool.set_transaction(pickle.loads(new_transaction))
                print("Done")
            
            elif data.startswith('update-transactionpool'):
                
                new_transactionpool = client_peer.recv(4096)
                self.transaction_pool = pickle.loads(new_transactionpool)
            
            client_peer.close()
                
        self.server_socket.close()
      
    
    def _stop_server(self):
        self.stop_server = True
      
    
    def _inform_manager_add(self, message):
        sock = socket.socket()
        sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
        sock.send(message.encode('utf-8'))
        peers = pickle.loads(sock.recv(4096))
        sock.close()
        sock = socket.socket()
        sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
        sock.send(f"get-transactionpool {self.client_ip}".encode('utf-8'))
        self.transaction_pool = pickle.loads(sock.recv(40960))
        self.peers = peers
        sock.close()
    
    
    def _inform_manager_delete(self, message):
        sock = socket.socket()
        sock.connect((self.MANAGER_IP, self.MANAGER_PORT))
        sock.send(message.encode('utf-8'))
    
    
    def leave_network(self):
        return self._inform_manager_delete(f"remove {self.client_ip}")
        
        
    def join_network(self):
        return self._inform_manager_add(f'add {self.client_ip}')
    
    
    def show_blockchain(self):
        print(self.blockchain.to_json())
    
    
    def _inform_peers(self, message, data=None):
        for peer in self.peers:
            sock=socket.socket()
            sock.connect((peer, self.server_port))
            sock.send(message.encode("utf-8"))
            if data is not None:
                sock.send(pickle.dumps(data))
            sock.close()
    
    def sync_chain(self):
        for peer in self.peers:
            sock = socket.socket()
            try:
                self._inform_peers("sync-chain", self.blockchain)
            except Exception as e:
                print(peer)
                print(e)
            finally:
                sock.close()
    
    def mine_transaction(self):
        start_time = time.time()
        transaction_data = self.transaction_pool.transaction_data()
        print(transaction_data)
        transaction_data.append(Transaction.reward_transaction(self.wallet).to_json())
        self.blockchain.add_block(transaction_data)
        block = self.blockchain.chain[-1]
        try:
            print("adding")
            self._inform_peers("add-block", block)
            print("clearting transaction")
            self.transaction_pool.clear_blockchain_transactions(self.blockchain)
            print("informing peers")
            self._inform_peers("update-transactionpool", self.transaction_pool)
        except Exception as e:
            print(e)
        finally:
            stop_time = time.time()
        return (stop_time - start_time)
    
    
    def wallet_transact(self, transaction_data):
        transaction = self.transaction_pool.existing_transaction(self.wallet.address)
        if transaction:
            transaction.update(
                self.wallet,
                transaction_data['recipient'],
                transaction_data['amount']
            )
        else:
            print("Creating")
            transaction = Transaction(
                self.wallet,
                transaction_data['recipient'],
                transaction_data['amount']
            )
            print("Done")
        
        try:
            self.transaction_pool.set_transaction(transaction)
            self._inform_peers("add-transaction", transaction)
        except Exception as e:
            print(e)

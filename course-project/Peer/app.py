from flask import Flask
from flask import request
from commons import PEER_IP
from peer.peer import Peer
from transaction_pool.transaction_pool import TransactionPool
import json
import pickle
import hashlib
import pickle
import socket
import threading
import time
from ecdsa import SigningKey
import json

app = Flask(__name__)

peer = Peer(PEER_IP)
peer.join_network()
print(peer.wallet.address)

@app.route("/api/balance")
def f1():
    return json.dumps({'balance' : peer.wallet.balance})

@app.route("/api/blockchain")
def f2():
    return json.dumps({'blockchain': peer.blockchain.to_json()})

@app.route("/api/transact", methods=["POST"])
def f3():
    print({'data': request.data})
    transaction_data = json.loads(request.data.decode('utf-8'))
    peer.wallet_transact(transaction_data)
    print(transaction_data)
    return "ok"

@app.route("/mine", methods=["POST"])
def f4():
    time_took = peer.mine_transaction()
    print(time_took)
    return "ok"

app.run(host='0.0.0.0')

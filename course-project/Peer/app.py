from flask import Flask
from flask import request
from commons import PEER_IP
from peer.peer import Peer
from transaction_pool.transaction_pool import TransactionPool
import json
import pickle
app = Flask(__name__)

peer = Peer(PEER_IP)
peer.join_network()


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
    print(transaction_data)
    return "ok"
@app.route("/mine", methods=["POST"])
def f4():
    pass


app.run(host='0.0.0.0')

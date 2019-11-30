from flask import Flask

from commons import PEER_IP
from peer.peer import Peer

app = Flask(__name__)

peer = Peer(PEER_IP)
peer.join_network()


@app.route("/api/balance")
def f1():
    pass


@app.route("/api/blockchain")
def f2():
    pass


@app.route("/api/transact", methods=["POST"])
def f3():
    pass

@app.route("/mine", methods=["POST"])
def f4():
    pass


app.run(host='0.0.0.0')

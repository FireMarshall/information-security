from flask import Flask

from commons import MANAGER_IP
from manager.manager import ManagerPeer

# from Manager.commons import MANAGER_IP


app = Flask(__name__)

manager = ManagerPeer(MANAGER_IP)


@app.route("/api/user_data")
def get_user_data():
    # print(request)
    return {
        "user": {
            "name": "abc",
            "ip": "192.168.13.11",
            "wallet address": "abcxyz"
        }
    }


app.run(host='0.0.0.0')

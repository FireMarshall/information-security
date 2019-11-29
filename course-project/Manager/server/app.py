from flask import Flask

app = Flask(__name__)


@app.route("/api/user_data")
def f1():
    return {
        "user": {
            "name": "abc",
            "ip": "192.168.13.11",
            "wallet address": "abcxyz"
        }
    }


app.run(host='0.0.0.0')

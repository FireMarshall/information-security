from django.shortcuts import render, HttpResponse, redirect
from blockchainapp.models import UserData
import requests
import json
# Create your views here.

URL_TO_MANAGER = '192.168.43.152:5000'
def login(request):
    return render(request, 'loginpage.html', {})


def get_userdata(request):
    if request.method == 'POST':
        # ip_request_obj = requests.get(url=f'http://{URL_TO_MANAGER}/api/user_data').json()
        # request.session['ip'] = ip_request_obj['user']['ip']
        request.session['username'] = request.POST.get('username')
        user_data = UserData.objects.get(username=request.session['username']) 
        # request.session['wallet_address'] = user_data.wallet_address
        request.session['ip'] = user_data.ip
        request.session['username'] = user_data.username    
        print(f"{request.session['ip']}")
        print(f"{request.session['username']}")
        return render(request, 'wallet.html', {})
    return render(request, 'loginpage.html', {})


def get_balance(request):
    balance_response_obj = requests.get(url=f'http://{request.session["ip"]}:5000/api/balance')
    if balance_response_obj.status_code == 200:
        display_msg = "Success"
        balance_json = balance_response_obj.json()
        balance = balance_json['balance']
    else:
        display_msg = "Unsuccessful"
        balance = 1000
        return render(request, 'wallet.html', {'balance': balance, 'display_msg': display_msg}) #add template
    return render(request,'wallet.html', {'balance': balance, 'display_msg': display_msg})


def get_blockchain(request):
    blockchain = requests.get(url=f'http://{request.session["ip"]}:5000/api/blockchain')
    if blockchain.status_code != 200:
        display_msg = "Unsuccessful"
        return render(request, 'block.html', {'display_msg': display_msg})   #add template
    else:
        blockchain = blockchain.json()
        print(blockchain)
    return render(request, 'block.html', blockchain)     #add template


def do_transaction(request):
    if request.method == 'POST':
        recipient_wallet_address = request.POST.get('address')
        amount = request.POST.get('amount')
        transaction_body = {
            'recipient_address': recipient_wallet_address,
            'amount': amount
        }
        status = requests.post(url=f'http://{request.session["ip"]}:5000/api/transact', data=json.dumps(transaction_body))
        print(status.status_code)
        if status.status_code == 200:
            display_msg = "Transaction done"
        else:
            display_msg = f"Transaction Failed : {status.text}"
    # return render(request, '', {'display_msg': display_msg})    #add template
    return HttpResponse("ok")

def display_transaction(request):
    return render(request, 'transactions.html', {})

def mine_transaction(request):
    mine_status = requests.post(url=f'http://{request.session["ip"]}:5000/mine')
    return redirect("get_blockchain")
        






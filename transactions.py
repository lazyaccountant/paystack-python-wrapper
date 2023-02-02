import requests
import json
import qrcode

api = [YOUR_API_KEY]

with open("bank_code.json", "r") as f:
    bank_code = json.load(f)

#initialize a transaction to get transaction url and transaction ref
def initialize_transaction():
    email = input("Enter Email Address: ")
    amount = int(input("Enter Amount: "))
    data = {
        "email": email,
        "amount": amount * 100
        }

    response = requests.post(url="https://api.paystack.co/transaction/initialize", headers={"Authorization": "Bearer "+api}, data = data)

    transaction_post = response.json()

    img = qrcode.make(transaction_post["data"]["authorization_url"])
    img.save(f'{transaction_post["data"]["reference"]}.jpg')

    print("Transaction Initialized!\nScan the qrcode to pay or follow this link{}".format(transaction_post["data"]["authorization_url"]))

#verify status of transaction, takes in transaction id as an arguement
def verify_transaction(transaction_ref: str):
    response = requests.get(url="https://api.paystack.co/transaction/verify/"+transaction_ref, headers={"Authorization": "Bearer "+api})

    response_dict = response.json()

    verify_status = response_dict["data"]

    if verify_status["status"] == "success":
        print("Payment Successful!")
    else:
        print("Transaction was not successful :(\nPlease try again")
    print(verify_status)
    #print(verify_status)

def list_transactions(method="all"):
    #success, failed, abandoned
    response = requests.get(url="https://api.paystack.co/transaction", headers={"Authorization": "Bearer "+api})
    response_dict = response.json()

    transaction_list = response_dict["data"]

    if method == "success":
        success_trans = []
        for transaction in transaction_list:
            if transaction["status"] == "success":
                success_trans.append(transaction)
            else:
                pass
        print(success_trans)
    
    elif method == "failed":
        failed_trans = []
        for transaction in transaction_list:
            if transaction["status"] == "failed":
                failed_trans.append(transaction)
            else:
                pass
        print(failed_trans)
    
    elif method == "abandoned":
        abandoned_trans = []
        for transaction in transaction_list:
            if transaction["status"] == "abandoned":
                abandoned_trans.append(transaction)
            else:
                pass
        print(abandoned_trans)

    else:
        print(transaction_list)
    

def fetch_transaction(transaction_id: str):
    response = requests.get(url="https://api.paystack.co/transaction/"+transaction_id, headers={"Authorization": "Bearer "+api})
    response_dict = response.json()

    transaction_data = response_dict["data"]

    print(transaction_data)

#charge returning customers in the future without collecting their payment details after collecting it the first time
def charge_auth(email: str, amount: int, auth_code: str):
    data = {
        "email": email,
        "amount": amount * 100,
        "authorization_code": auth_code
        }
    response = requests.post(url="https://api.paystack.co/transaction/charge_authorization", headers={"Authorization": "Bearer "+api}, data = data)

    response_dict = response.json()
    print(response_dict)

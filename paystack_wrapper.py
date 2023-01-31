import requests
import json

api = "sk_test_17a27428727ca80db6bf2f0bb69310617f30744c"

with open("bank_code.json", "r") as f:
    bank_code = json.load(f)

def verify():

    with open("bank_code.json", "r") as f:
        bank_code = json.load(f)

    acc_num = input("Enter Account Number: ")
    bank = input("Enter Beneficiary Bank: ")

    acc_req = requests.get(url=f"https://api.paystack.co/bank/resolve?account_number={acc_num}&bank_code={bank_code[bank]}", headers={"Authorization": "Bearer "+api})

    acc_details = acc_req.json()

    name = acc_details["data"]["account_name"]

    details = {"Name": name, "Account Number": acc_num, "Bank": bank}

    print(f'Transfer Beneficiary: {details["Name"]}')

    return details


def create_transfer():
    acc_details = verify()

    data = { "type": "nuban",
        "name": acc_details["Name"],
        "account_number": acc_details["Account Number"],
        "bank_code": bank_code[acc_details["Bank"]],
        "currency": "NGN"
        }

    bank_post = requests.post(url="https://api.paystack.co/transferrecipient", headers={"Authorization": "Bearer "+api}, data = data)

    post_details = bank_post.json()

    return post_details["data"]

def initiate_transfer():
    transfer_details = create_transfer()
    amount = input("Enter Amount: ")
    reason = input("Reason: ")

    data = { "source": "balance", 
      "amount": str(amount),
      "reference": "your-unique-reference", 
      "recipient": transfer_details["recipient_code"], 
      "reason": reason 
    }

    transfer_post = requests.post(url="https://api.paystack.co/transfer", headers={"Authorization": "Bearer "+api}, data = data)

    transfer_details = transfer_post.json()

    print(transfer_details)

initiate_transfer()
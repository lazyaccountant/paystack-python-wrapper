import requests
import json
import random

api = "[YOUR_API_KEY]"

with open("bank_code.json", "r") as f:
    bank_code = json.load(f)

def create_customer():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    phone = input("Phone Number: ")
    email = input("Enter Email: ")

    data = {"email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
        }

    customer_post = requests.post(url="https://api.paystack.co/customer", headers={"Authorization": "Bearer "+api}, data = data)

    #print(customer_post)
    #print(customer_post.json())
    print("Customer created successfully!")


def list_customers():
    list_details = requests.get(url="https://api.paystack.co/customer", headers={"Authorization": "Bearer "+api})

    print(list_details)
    print(list_details.json())


def fetch_customer():
    email = input("Enter Email Address: ")

    fetch_details = requests.get(url=f"https://api.paystack.co/customer/{email}", headers={"Authorization": "Bearer "+api})

    customer_details = fetch_details.json()

    #print(customer_details["data"])
    return customer_details["data"]

def update_customer():
    customer_details = fetch_customer()

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    phone = input("Phone Number: ")

    data = {"first_name": first_name,
        "last_name": last_name,
        "phone": phone
        }

    update_put = requests.put(url=f'https://api.paystack.co/customer/{customer_details["customer_code"]}', headers={"Authorization": "Bearer "+api}, data = data)

    #print(update_put)
    #print(update_put.json())

def validate_customer():
    customer_data = fetch_customer()
    bvn = input("Enter BVN: ")
    acc_num = input("Account Number: ")
    bank = input("Bank: ")

    data = {"country": "NG",
            "type": "bank_account",
            "account_number": acc_num,
            "bvn": bvn,
            "bank_code": bank_code[bank],
            "first_name": customer_data["first_name"],
            "last_name": customer_data["last_name"]}

    validate_post = requests.post(url=f'https://api.paystack.co/customer/{customer_data["customer_code"]}/identification', headers={"Authorization": "Bearer "+api}, data = data)

    print(validate_post)
    print(validate_post.json())


def blacklist():
    customer_data = fetch_customer()

    data = {"customer": customer_data['customer_code'], "risk_action": "deny"}
    blacklist_post = requests.post(url="https://api.paystack.co/customer/set_risk_action", headers={"Authorization": "Bearer "+api}, data = data)

    #print(blacklist_post)
    #print(blacklist_post.json())
    print("Customer has been blocked")


def whitelist():
    customer_data = fetch_customer()

    data = {"customer": customer_data['customer_code']}
    whitelist_post = requests.post(url="https://api.paystack.co/customer/set_risk_action", headers={"Authorization": "Bearer "+api}, data = data)

    #print(whitelist_post)
    #print(whitelist_post.json())
    print("Customer has been unblocked!")

#deactivate_autorization():

#create virtual account
def create_va():
    customer_data = fetch_customer()
    banks = ["Access Bank", "Wema Bank"]
    data = {"customer":customer_data["id"],"preferred_bank":"test-bank"} #banks[random.randint(0, 1)]}

    va_details = requests.post(url="https://api.paystack.co/dedicated_account", headers={"Authorization": "Bearer "+api}, data = data)

    print(va_details.json())
    print("Bank account created successfully!")

def assign_va():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    middle_name = input("Enter Middle Name: ")
    email = input("Enter Email Address: ")
    phone = input("Enter Phone Number: ")


    data = { 
      "email": email,
      "first_name": first_name,
      "middle_name": middle_name,
      "last_name": last_name,
      "phone": phone,
      "preferred_bank": "test-bank",
      "country": "NG"
    }

    va_post = requests.post(url="https://api.paystack.co/dedicated_account/assign", headers={"Authorization": "Bearer "+api}, data = data)

    print(va_post.json())
    print("Bank account created successfully!")


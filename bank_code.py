import requests
import json

urlx = "https://api.paystack.co/bank"

api = "sk_test_17a27428727ca80db6bf2f0bb69310617f30744c"

banks = requests.get(url=urlx, headers={"Authorization": api, "country": "Nigeria"})

bank_dict = banks.json()

bank_codes = {}

for bank in bank_dict["data"]:
    bank_codes[bank["name"]] = bank["code"]

with open("bank_code.json", "w") as f:
    json.dump(bank_codes, f)
print(bank_codes)
#print(bank_dict["data"])
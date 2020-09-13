from bs4 import BeautifulSoup as soup

with open("checkoutCC2.html", "r") as f:
    contents = f.read()

page = soup(contents, "html.parser")

inputs = page.find("form", {"name":"checkout_confirmation"}).findAll("input", type="hidden")
print(inputs)
'''
cc_data = {
    "mid": inputs[0].get("value"),
    "lang": "en",
    "deviceCategory": "0",
    "orderid": inputs[3].get("value"),
    "orderDesc": "COLORSKATES",
    "orderAmount": inputs[5].get("value"),
    "currency": "EUR",
    "payerEmail": inputs[7].get("value"),
    "payerPhone": "",
    "billCountry": inputs[9].get("value"),
    "billState": inputs[10].get("value"),
    "billZip": inputs[11].get("value"),
    "billCity": inputs[12].get("value"),
    "billAddress": inputs[13].get("value"),
    "weight": "",
    "dimensions": "",
    "shipCountry": "",
    "shipState": "",
    "shipZip": "",
    "shipCity": "",
    "shipAddress": "",
    "addFraudScore": "",
    "maxPayRetries": "",
    "reject3dsU": "",
    "payMethod": "",
    "trType": "1",
    "extInstallmentoffset": "",
    "extInstallmentperiod": "",
    "extRecurringfrequency": "",
    "extRecurringenddate": "",
    "blockScore": "",
    "cssUrl": "",
    "confirmUrl": "https://www.colorskates.com/checkout_process.php",
    "cancelUrl": "https://www.colorskates.com/checkout_payment.php?error_message=Payment error",
    "var1": "",
    "var2": inputs[35].get("value"),
    "var3": inputs[36].get("value"),
    "var4": "",
    "var5": "",
    "digest": inputs[39].get("value"),
}
print(cc_data)
'''
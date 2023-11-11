from colorama import init
from termcolor import colored
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
import os, re, datetime, time, requests, random, json, sys
init()

# To do list:
# - Add monitor module (monitor if product is live and then start the task as "safe mode")
# - Add threading

product = "https://www.workingclassheroes.co.uk/footwear/trainers/nike-sb-dunk-low-pro-j-pack-chicago-shoes-varsity-red-white-black__208109"
size = "random" # Random or number (7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 12) UK + number
payment = "pp" # pp, cc, cc_3DS
mode = "Safe" # Safe & Fast

email = "email@gmail.com"
first_name = "Name"
last_name = "L_Name"
address_line_1 = "street 2"
address_line_2 = ""
city = "Athens"
postcode = "12345"
country = "GR"
phone = "6973453333"
shipping = "5"
card_holder_name = "First Last"
card_type = "Visa" # (Visa, MasterCard, Maestro)
card_nums = "1234 1234 1424 1234"
expiry_month = "02"
expiry_year = "22"
cvv = "123"

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    now = colored(now, "cyan")
    now = '[' + str(now) + ']' + f' [{colored("WorkingClassHeroes", "cyan")}]'
    return now

class Heroes():
    def __init__(self):
        os.system("title WreckAIO v0.0.1 - WorkingClassHeroes")
        self.s = requests.Session()
        self.mainHeaders = {
	        "authority": "www.workingclassheroes.co.uk",
	        "host": "www.workingclassheroes.co.uk",
            "origin": "https://www.workingclassheroes.co.uk",
            "pragma": "no-cache",
	        "referer": product,
	        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
	        "x-requested-with": "XMLHttpRequest"
        }
        self.atcHeaders = {
            "authority": "www.workingclassheroes.co.uk",
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            "origin": "https://www.workingclassheroes.co.uk/",
            "referer": product
        }
        self.paypalHeaders = {
	        "authority": "www.workingclassheroes.co.uk",
	        "path": "/wsCitrusStore.asmx/WightPaypalBtnCallback",
	        "host": "www.workingclassheroes.co.uk",
            "origin": "https://www.workingclassheroes.co.uk",
            "pragma": "no-cache",
	        "referer": "https://www.workingclassheroes.co.uk/shoppingcart.aspx",
	        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
	        "x-requested-with": "XMLHttpRequest"
        }
        self.checkoutHeaders = {
            "cache-control": "no-cache",
            "connection": "keep-alive",
            "host": "www.workingclassheroes.co.uk",
            "origin": "https://www.workingclassheroes.co.uk",
            "pragma": "no-cache",
            "referer": "https://www.workingclassheroes.co.uk/ssl/secure/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
	        "x-requested-with": "XMLHttpRequest"
        }

        if mode == "Safe":
            self.scrape()
            self.scrape_sizes()
            self.atc()
        elif mode == "Fast":
            self.preload_fast()
            self.atc_fast()
        else:
            print(gettime(), colored("Invalid module mode.", "red"))
            sys.exit()

        if payment == "pp":
            self.paypal()
        elif payment == "cc":
            self.guest_checkout()
            self.submit_address()
            self.delivery_details()
            self.payment_details()
            self.three_ds_check()
        elif payment == "cc_3DS":
            self.guest_checkout()
            self.submit_address()
            self.delivery_details()
            self.payment_details()
            self.three_ds_check()
            self.scrape_threeDS()
            self.threeDS_checkout()
        else:
            print(gettime(), colored("Invalid payment method.", "red"))
            sys.exit()

    def sendWebhook(self, payment_method, success):
        webhook = Webhook(os.environ["discordWebhook"])

        if success == False:
            embedColor = 16724787
            embedTitle = "Failed Checkout"
        elif success == True and payment_method == "pp":
            embedColor = 1151440
            embedTitle = "Successful Checkout"
        else:
            embedColor = 182048
            embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Working Class Heroes", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({product})", inline=False)
        embed.add_field(name="Size", value=size, inline=False)
        embed.add_field(name="Price", value="£" + str(price), inline=False)
        embed.add_field(name="Mode", value=mode, inline=False)

        if payment_method == "pp" and success == True:
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
            embed.add_field(name="Complete Payment", value=f"[Click here]({paypal_url})", inline=False)
        elif payment_method == "cc" and success == True:
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
        elif payment_method == "cc_3DS" and success == True:
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
            embed.add_field(name="Complete Payment", value="In App", inline=False)
            # embed.add_field(name="Complete Payment", value=f"[Click here]({cc_url})", inline=False)

        embed.set_thumbnail(url=img)
        embed.set_footer(text="WreckAIO • v0.0.1", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def publicWebhook(self, payment_method):
        webhook = Webhook("public-webhook")

        embedColor = 182048
        embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Working Class Heroes", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({product})", inline=False)
        embed.add_field(name="Size", value=size, inline=False)
        embed.add_field(name="Price", value="£" + str(price), inline=False)
        embed.add_field(name="Mode", value=mode, inline=False)

        if payment_method == "pp":
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
        elif payment_method == "cc" or payment_method == "cc_3DS":
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
        
        embed.set_thumbnail(url=img)
        embed.set_footer(text="WreckAIO Public Checkouts • v0.0.1", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def preload_fast(self):
        global img
        global price
        global title

        print(gettime(), colored("Product information found.", "yellow"))
        title = "Nike SB Dunk Low Pro J-Pack Chicago Shoes Varsity Red White Black"
        img = "https://www.workingclassheroes.co.uk/images/NikeSbDunkLowProVarsityRed6-3.jpg"
        price = 84.95
        print(gettime(), colored("Succesfully got product information.", "green"))

    def atc_fast(self):
        global size
        global size_id
        global pid
        global product_id

        product_id = 208109 # The numbers in the end of the URL
        pid = 23578 # hiddenFieldAttID

        # scrape size ids for each release as they pre upload the product page w/ size attributes
        sizes = {
            "UK 6": "180091",
            "UK 6.5": "180092",
            "UK 7": "180093",
            "UK 7.5": "180094",
            "UK 8": "180095",
            "UK 8.5": "180096",
            "UK 9": "180097",
            "UK 9.5": "180098",
            "UK 10": "180099",
            "UK 10.5": "180100",
            "UK 11": "180101",
            "UK 12": "180102"
        }

        if size == "random":
            size = str(random.choice(list(sizes.keys())))
        else:
            size = "UK " + str(size)
        size_id = sizes[size]

        atc_data = {"iProductID":product_id,"iQuantity":1,"iAttributeID":pid,"iAttributeDetailID":size_id}
        atc_post = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/AddToBasketJSNew", json=atc_data, headers=self.atcHeaders)
        if atc_post.status_code not in (200, 302):
            print(gettime(), colored(f"Failed to add to cart [{size}].", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.atc_fast()
        else:
            print(gettime(), colored(f"Added to cart [{size}].", "green"))

    def scrape(self):
        global img
        global price
        global title
        global product_id

        product_id = int(re.search(r"\d+", product).group(0))

        get_product_lw = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetProductLW", json={"productid":product_id}, headers=self.mainHeaders)
        if get_product_lw.status_code not in (200, 302):
            print(gettime(), colored("Error getting product information.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape()
        else:
            print(gettime(), colored("Product information found.", "yellow"))

        parsed = json.loads(get_product_lw.text)
        title = parsed["d"]["Name"]
        img = "https://www.workingclassheroes.co.uk/" + str(parsed["d"]["ImageLargePath"])
        price = parsed["d"]["SalePrice"]
        print(gettime(), colored("Succesfully got product information.", "green"))
    
    def scrape_sizes(self):
        global sizes
        global pid

        data = '{"controlLocation":"/modules/controls/clAttributeControl.ascx", "ProductID": "", "DetailPage":true, "dollar":0, "percentage":0}'
        parsed = json.loads(data)
        parsed["ProductID"] = str(product_id)

        get_attributes = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetAttributes", json=parsed, headers=self.mainHeaders)
        if get_attributes.status_code not in (200, 302):
            print(gettime(), colored("Error getting size information.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape_sizes()
        else:
            print(gettime(), colored("Size information found.", "yellow"))

        parsed = json.loads(get_attributes.text)
        html = parsed["d"]["HTML"]
        page = soup(html, "lxml")

        sizes = {}
        size_nums = page.findAll("div", class_="name")
        size_ids = page.findAll("div", class_="hideme Attattributeid")
        size_all = page.findAll("div", class_="attRow")
        pid = page.find("input", class_="hiddenFieldAttID")["value"]

        for i in range(0, len(size_all)):
            if "InStockCSS" in str(size_all[i]):
                sizes[str(size_nums[i].text)] = str(size_ids[i].text)

        if bool(sizes) == False:
            print(gettime(), colored("Product out of stock.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape_sizes()
        else:
            print(gettime(), colored("Succesfully got size information.", "green"))

    def atc(self):
        global size

        if size == "random":
            size = str(random.choice(list(sizes.keys())))
        else:
            size = "UK " + str(size)
        size_id = sizes[size]

        atc_post = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/AddToBasketJSNew", json={"iProductID":product_id,"iQuantity":1,"iAttributeID":pid,"iAttributeDetailID":size_id}, headers=self.atcHeaders)
        if atc_post.status_code not in (200, 302):
            print(gettime(), colored(f"Failed to add to cart [{size}].", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.atc()
        else:
            print(gettime(), colored(f"Added to cart [{size}].", "green"))

    def paypal(self):
        global paypal_url
        
        time.sleep(int(os.environ["checkoutDelay"]))
        checkout = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPaypalBtnCallback", json={}, headers=self.paypalHeaders)
        if checkout.status_code not in (200, 302):
            self.sendWebhook(payment_method=payment, success=False)
            print(gettime(), colored("Failed to get checkout link.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.paypal()
        else:
            parsed = json.loads(checkout.text) # Try without parsed = json.loads
            paypal_url = parsed["d"]["errorMsg"]
            self.sendWebhook(payment_method=payment, success=True)
            self.publicWebhook(payment_method=payment)
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))

    def guest_checkout(self):
        data = '{"emailAddress":"", "firstName":"", "GDPRAllowed":false, "lastName":""}'
        parsed = json.loads(data)
        parsed["emailAddress"] = email
        parsed["firstName"] = first_name
        parsed["lastName"] = last_name

        create_guest_checkout = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightCreateAnonymousCustomerLogin", json=parsed, headers=self.checkoutHeaders)
        if create_guest_checkout.status_code not in (200, 302):
            print(gettime(), colored("Failed to initialize guest checkout.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.guest_checkout()
        else:
            print(gettime(), colored("Initialized guest checkout.", "yellow"))
        
    def submit_address(self):
        data = {"firstName":first_name , "lastName":last_name, "company":"", "address1":address_line_1, "address2":address_line_2, "city":city, "postcode":postcode, "country":country}
        post_delivery_address = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightLoadShippingOptions", json=data, headers=self.checkoutHeaders)
        if post_delivery_address.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit address.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.submit_address()
        else:
            print(gettime(), colored("Successfully submitted address.", "green"))
        
    def delivery_details(self):
        global premium_status

        print(gettime(), colored("Setting shipping details.", "yellow"))
        shipping_nums = {
            "1": "RoyalMail48",
            "2": "ExpresspakDpdNextDay",
            "3": "ExpresspakSaturday",
            "4": "ExpresspakSunday",
            "5": "InternationalSigned"
        }
        shipping_options = {
            "RoyalMail48": "3 - 5 Working Days Unsigned",
            "ExpresspakDpdNextDay": "DPD Premium Next Day Tracked",
            "ExpresspakSaturday": "DPD UK Premium Saturday Deliver",
            "ExpresspakSunday": "DPD UK Premium Sunday Delivery",
            "InternationalSigned": "Royal Mail International"
        }
        data = '{"firstName":"" , "lastName":"", "company":"", "address1":"", "address2":"", "city":"", "postcode":"", "phone":"", "country":"","selectedShipping":{"IsPremium":false,"bookingCode":"","carrierCode":"","carrierCustom1":"","carrierCustom2":"","carrierCustom3":"","carrierServiceCode":"","carrierServiceTypeCode":"","collectionSlots":null,"collectionWindow":{"to":"2020-09-01T13:03:24.3442392+01:00","from":"2020-09-01T13:03:24.3442392+01:00"},"cutOffDateTime":"2020-09-01T13:03:24.3442392+01:00","deliverySlots":null,"deliveryWindow":{"to":"2020-09-10T13:03:24.3442392+01:00","from":"2020-09-04T13:03:24.3442392+01:00"},"groupCodes":null,"name":"","nominatableCollectionSlot":false,"nominatableDeliverySlot":false,"recipientTimeZone":null,"score":0,"senderTimeZone":null,"shippingCharge":0,"shippingCost":0,"taxAndDuty":0,"taxAndDutyStatusText":null,"vatRate":0},"nickname":""}'
        parsed = json.loads(data)
        parsed["address1"] = address_line_1
        parsed["address2"] = address_line_2
        parsed["city"] = city
        parsed["country"] = country
        parsed["firstName"] = first_name
        parsed["lastName"] = last_name
        parsed["phone"] = phone
        parsed["postcode"] = postcode
        parsed["selectedShipping"]["shippingCharge"] = 16.99 # 16.99 for greece only
        parsed["selectedShipping"]["bookingCode"] = shipping_nums[shipping]
        parsed["selectedShipping"]["carrierCode"] = shipping_nums[shipping]
        parsed["selectedShipping"]["carrierServiceCode"] = shipping_nums[shipping]
        parsed["selectedShipping"]["name"] = shipping_options[shipping_nums[shipping]]
        if shipping_nums[shipping] == "RoyalMail48" or shipping_nums[shipping] == "InternationalSigned":
            premium_status = False
        else:
            premium_status = True
        parsed["selectedShipping"]["IsPremium"] = premium_status

        post_shipping_details = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPostShippingDetails", json=parsed, headers=self.checkoutHeaders)
        if post_shipping_details.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit shipping details.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.delivery_details()
        else:
            print(gettime(), colored("Successfully submitted shipping details.", "green"))

    def payment_details(self):
        data = '{"MethodType":"Standard","SpecialInstructions":"","PaymentMethod":"credit card","cardTypeUid":8,"cardType":"","cardNumber":"","secureCode":"","expMonth":"","expYear":"","token":"","selectedShipping":{"IsPremium":false,"bookingCode":"","carrierCode":"","carrierCustom1":"","carrierCustom2":"","carrierCustom3":"","carrierServiceCode":"","carrierServiceTypeCode":"","collectionSlots":null,"collectionWindow":{"to":"2019-08-12T00:00:00","from":"2019-08-12T00:00:00"},"cutOffDateTime":"2019-08-12T00:00:00","deliverySlots":null,"deliveryWindow":{"to":"2019-08-13T00:00:00","from":"2019-08-13T00:00:00"},"groupCodes":null,"name":"","nominatableCollectionSlot":false,"nominatableDeliverySlot":false,"recipientTimeZone":null,"score":0,"senderTimeZone":null,"shippingCharge":0,"shippingCost":0,"taxAndDuty":0,"taxAndDutyStatusText":null,"vatRate":0},"paypalToken":"","payPalPayerID":""}'
        parsed = json.loads(data)
        parsed["cardType"] = card_type
        parsed["cardNumber"] = card_nums
        parsed["secureCode"] = cvv
        parsed["expMonth"] = expiry_month
        parsed["expYear"] = "20" + expiry_year
        parsed["selectedShipping"]["IsPremium"] = premium_status
        parsed["selectedShipping"]["shippingCharge"] = 16.99

        submit_payment = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightHandlePaymentSelector", json=parsed, headers=self.checkoutHeaders)
        if submit_payment.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit payment details.", "red"))
            self.sendWebhook(payment_method=payment, success=False)
            time.sleep(int(os.environ["errorDelay"]))
            self.payment_details()
        else:
            print(gettime(), colored("Submitted payment details.", "green"))
            
    def three_ds_check(self):
        post_threeDS_check = self.s.get("https://www.workingclassheroes.co.uk/ssl/secure/3DValidation.aspx")
        if post_threeDS_check.status_code not in (200, 302):
            print(gettime(), colored("Failed to validate card for 3DS.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.three_ds_check()
        else:
            print(gettime(), colored("Validated card for 3DS.", "green"))

    def scrape_threeDS(self):
        global inputs

        threeDS_attributes = self.s.get("https://www.workingclassheroes.co.uk/ssl/controls/3DAuthentication/3DRedirect.aspx")
        if threeDS_attributes.status_code not in (200, 302):
            print(gettime(), colored("Failed to parse 3DS attributes.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape_threeDS()
        else:
            print(gettime(), colored("Parsed 3DS attributes.", "green"))

        page = soup(threeDS_attributes.text, "lxml")
        inputs = page.findAll("input", type="hidden")

    def threeDS_checkout(self):
        payload = {
            "PaReq": inputs[0].get("value"),
            "TermUrl": inputs[1].get("value"),
            "MD": inputs[2].get("value")
        }
        checkout_3DS = self.s.post("https://verifiedbyvisa.acs.touchtechpayments.com/v1/payerAuthentication", data=payload, headers=self.checkoutHeaders)
        if checkout_3DS.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit check out.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.threeDS_checkout()
        else:
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))
            self.sendWebhook(payment_method=payment, success=True)
            self.publicWebhook(payment_method=payment)

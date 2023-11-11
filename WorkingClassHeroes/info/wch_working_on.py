from colorama import init
from termcolor import colored
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
import os, re, datetime, time, requests, random, json
init()

# Notes:
# - Find a way to have sizes dict only with instock sizes
# - Add threading
# - Check all json payloads/data for if values are ints or str (ex: atc json/data)
# - Make a version of the script where everything is set for specific (faster) for the sashiko
# - Finish CC
# - Finish Clink&Collect
# - Remove things from headers and test if it still works

product = "https://www.workingclassheroes.co.uk/nike-sb-dunk-high-pro-shoes-black-university-gold__205357"
size = "7" # Random or number (7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 12)
payment = "click_collect" # cc | pp | click_collect (pp only ready)
email = "email@gmail.com"
first_name = "Joe"
last_name = "Tei"
address1 = ""
address2 = ""
city = ""
country = ""
phone = ""
postcode = ""
card_holder_name = ""
card_type = "Visa"
card_nums = "1234 1234 1234 1234"
expiry_month = "02"
expiry_year = "21"
cvv = ""

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    now = colored(now, "cyan")
    now = '[' + str(now) + ']' + f' [{colored("WreckAIO", "cyan")}]' + f' [{colored("WorkingClassHeroes", "cyan")}]'
    return now

class Heroes():
    def __init__(self):
        # os.system("title WreckAIO v0.0.1 - WorkingClassHeroes")
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

        self.scrape()
        self.size_ids_nums()
        '''
        self.addtocart()
        
        if payment == "pp":
            self.paypal()
        elif payment == "cc":
            self.guest_checkout()
            self.cc()
        elif payment == "click_collect":
            self.guest_checkout()
            self.postcode()
            self.collection_id()
            self.customer_id()
            self.rewards_customer()
        else:
            print(gettime(), colored("Invalid payment method.", "red"))
            sys.exit()
        '''

    def sendWebhook(self, payment_method, success=False):
        webhook = Webhook(os.environ["discordWebhook"])

        if success == False:
            embedColor = 16724787
            embedTitle = "Failed Checkout"
        elif success == True and payment_method == "pp":
            embedColor = 9881393
            embedTitle = "Complete Checkout"
        else:
            embedColor = 9881393
            embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Working Class Heroes", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({product})", inline=False)
        embed.add_field(name="Size", value="UK " + size, inline=False)
        embed.add_field(name="Price", value="£" + str(price), inline=False)

        if payment_method == "click_collect" and success == True:
            embed.add_field(name="Payment Method", value="Click & Collect", inline=False)
        elif payment_method == "pp" and success == True:
            embed.add_field(name="Payment Method", value="Paypal", inline=False)
            embed.add_field(name="Complete Payment", value=f"[Click here]({paypal_url})", inline=False)
        elif payment_method == "cc" and success == True:
            embed.add_field(name="Payment Method", value="CC", inline=False)

        embed.set_thumbnail(url=img)
        embed.set_footer(text="WreckAIO", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

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
    
    def size_ids_nums(self):
        global sizes
        global pid

        data = '{"controlLocation":"/modules/controls/clAttributeControl.ascx", "ProductID": "x", "DetailPage":true, "dollar":0, "percentage":0}'
        parsed = json.loads(data)
        parsed["ProductID"] = str(product_id)

        get_attributes = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/GetAttributes", json=parsed, headers=self.mainHeaders)
        if get_attributes.status_code not in (200, 302):
            print(gettime(), colored("Error getting size information.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.size_ids_nums()
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

        for size in size_all:
            if "Out of stock" in str(size):
                size_num = page.find("div", class_="name").text
                size_id = page.find("div", class_="hideme Attattributeid").text
                sizes[size_num] = size_id

        print(sizes)
        # for i in range(0, len(size_nums)):
        #     sizes[str(size_nums[i].text)] = str(size_ids[i].text)
        print(gettime(), colored("Succesfully got size information.", "green"))

    def addtocart(self):
        global size

        if size == "random":
            size = "UK " + str(random.choice(list(sizes.keys())))
        size_id = sizes["UK " + str(size)]

        atc_post = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/AddToBasketJSNew", json={"iProductID":product_id,"iQuantity":1,"iAttributeID":pid,"iAttributeDetailID":size_id}, headers=self.atcHeaders)
        if atc_post.status_code not in (200, 302):
            print(gettime(), colored(f"Failed to add to cart [UK {size}].", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.addtocart()
        else:
            print(gettime(), colored(f"Added to cart [UK {size}].", "green"))

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
            parsed = json.loads(checkout.text)
            paypal_url = parsed["d"]["errorMsg"]
        
        # remove this if else statement after sizes dict is only in stock sizes
        # if above not fixed try str(paypal_url)
        if "https://www.paypal.com/cgi-bin/" not in paypal_url:
            self.sendWebhook(payment_method=payment, success=False)
            print(gettime(), colored("Failed to check out, Out of Stock.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.paypal()
        else:
            self.sendWebhook(payment_method=payment, success=True)
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))
    
    def guest_checkout(self):
        data = '{"emailAddress":"email@gmail.com", "firstName":"First", "GDPRAllowed":false, "lastName":"Last"}'
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

    def cc(self):
        pass

    # remove click and collect
    def postcode(self):
        global collectionId

        submit_postcode = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightLoadClickCollectMaps", json={"postcode":postcode}, headers=self.checkoutHeaders)
        if submit_postcode.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit postcode.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.postcode()
        else:
            print(gettime(), colored("Submitted postcode.", "yellow"))

        parsed = json.loads(submit_postcode.text)
        html = parsed["d"]
        page = soup(html, "lxml")

        data = page.find("input", id="addressDataStandardstoreWorkingClassHeroes")["value"]
        parsed = json.loads(data)
        collectionId = parsed["CollectionID"]

    def collection_id(self):
        data = {"CollectionID":collectionId , "HDNStr":"", "CollectType":0,"orderAddress":'{"Name":"Working Class Heroes","Distance":0.004194809046828072,"PostCode":"LA12 7LS","CollectionID":1076,"Latitude":54.1958155,"Longitude":-3.094042,"Street":"40-44 Market Street","City":"Ulverston","country":"GB","DealerNumber":"storeWorkingClassHeroes","HomeSetupEnabled":false,"HomeSetupDistance":0,"DealerPostcode":"LA12 7LS","Hours":"Sunday 11:00:00-16:00:00<br></a>Monday 10:00:00-18:00:00<br/>Tuesday 10:00:00-18:00:00<br/>Wednesday 10:00:00-18:00:00<br/>Thursday 10:00:00-18:00:00<br/>Friday 10:00:00-18:00:00<br/>Saturday 10:00:00-18:00:00<br/>"}'}
        
        submit_collectionId = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPostClickAndCollectLocation", json=data, headers=self.checkoutHeaders)
        if submit_collectionId.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit collection id.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.collection_id()
        else:
            print(gettime(), colored("Submitted collection id.", "yellow"))

    def customer_id(self):
        get_customerId = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightGetCheckoutObjects", json={}, headers=self.checkoutHeaders)
        if get_customerId.status_code not in (200, 302):
            print(gettime(), colored("Failed to find customer id.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.customer_id()
        else:
            print(gettime(), colored("Succesfully found customer id.", "yellow"))

        parsed = json.loads(get_customerId.text)
        parsed = parsed["d"].split(',')
        customerId = int(parsed[16].replace('"ID":', ''))

    def rewards_customer(self):
        checkout_rewards = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/newCheckoutRewardsPoints", json={"ncCustomerID":customerId,"ncOrderTotal":price}, headers=self.checkoutHeaders)
        if checkout_rewards.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit customer id.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.rewards_customer()
        else:
            print(gettime(), colored("Submitted customer id.", "yellow"))

    def submit_address(self):
        data = {"firstName":first_name, "lastName":last_name, "company":"", "address1":address1, "address2":address2, "city":city, "postcode":postcode, "phone":phone, "country":country,"nickname":""}

        address = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightPostBillingDetails", json=data, headers=self.checkoutHeaders)
        if address.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit billing details.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.submit_address()
        else:
            print(gettime(), colored("Submitted billing details.", "yellow"))

    def submit_paymet_collect(self):
        data = {"MethodType":"Standard","SpecialInstructions":"","PaymentMethod":"credit card","cardTypeUid":8,"cardType":"Visa","cardNumber":"4917 05869393982","secureCode":"944","expMonth":"02","expYear":"2022","token":"","selectedShipping":{"IsPremium":false,"bookingCode":"","carrierCode":"","carrierCustom1":"","carrierCustom2":"","carrierCustom3":"","carrierServiceCode":"","carrierServiceTypeCode":"","collectionSlots":null,"collectionWindow":{"to":"2019-08-12T00:00:00","from":"2019-08-12T00:00:00"},"cutOffDateTime":"2019-08-12T00:00:00","deliverySlots":null,"deliveryWindow":{"to":"2019-08-13T00:00:00","from":"2019-08-13T00:00:00"},"groupCodes":null,"name":"","nominatableCollectionSlot":false,"nominatableDeliverySlot":false,"recipientTimeZone":null,"score":0,"senderTimeZone":null,"shippingCharge":0,"shippingCost":0,"taxAndDuty":0,"taxAndDutyStatusText":null,"vatRate":0},"paypalToken":"","payPalPayerID":""}
        parsed = json.loads(data)
        parsed["cardType"] = card_type
        parsed["cardNumber"] = card_nums
        parsed["secureCode"] = cvv
        parsed["expMonth"] = expiry_month
        parsed["expYear"] = expiry_year

        time.sleep(int(os.environ["checkoutDelay"]))
        payment = self.s.post("https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/WightHandlePaymentSelector", json=parsed, headers=self.checkoutHeaders)
        if payment.status_code not in (200, 302):
            self.sendWebhook(payment_method=payment, success=False)
            print(gettime(), colored("Failed to submit checkout."))
            time.sleep(int(os.environ["errorDelay"]))
            self.submit_payment_collect(self)
        else:
            self.sendWebhook(payment_method=payment, success=True)
            print(gettime(), colored("Successfully checked out.", "green"))

    

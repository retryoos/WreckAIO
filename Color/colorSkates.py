from colorama import init
from termcolor import colored
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
import os, re, datetime, time, requests, random, sys, csv, threading
init()

# Notes:
# - Improve code
# - Add threading with csv
# - Add fast mode (preloaded sizes)

#product = input("Product URL: ")
#size = input("Size: ") # random or int
#payment = "cod" # pp and cod the fastest
#email = "dimitriskalligaridis@gmail.com"
#pw = "HXucTyihZB5tTX4"
province = "Αττικη"
# For greek province:
# - Only for CC and GR
# - Possible fix check for cc (as payment method) and country in csv if country == gr then ask the user to insert their state
# - Address in account should be in english

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    now = colored(now, "cyan")
    now = '[' + str(now) + ']' + f' [{colored("ColorSkates", "cyan")}]'
    return now

class ColorSkates():
    def __init__(self, product, size, email, pw, payment):
        os.system("title WreckAIO v0.0.1 - ColorSkates")
        self.product = product
        self.size = size
        self.email = email
        self.pw = pw
        self.payment = payment
        self.s = requests.Session()
        self.mainHeaders = {
            "authority": "www.colorskates.com",
            "referer": self.product,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0"
            }
        self.paypalHeaders = {
            "authority": "www.paypal.com",
            "referer": "https://www.colorskates.com/checkout_confirmation.php",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0"
        }
        self.ccHeaders = {
            "host": "www.alphaecommerce.gr",
            "referer": "https://www.colorskates.com/checkout_confirmation.php",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0"
        }

        self.login()
        self.scrape()
        self.addtocart()
        self.address()
        self.sitekey_search()
        
        if self.payment == "cod":
            self.cod()
            self.send_confirmation()
        elif self.payment == "pp":
            self.paypal()
            self.send_paypal()
        elif self.payment == "cc":
            self.cc()
            self.send_cc()
        else:
            print(gettime(), colored("Invalid payment method.", "red"))
            sys.exit()

    def sendWebhook(self, payment_method, success):
        webhook = Webhook(os.environ["discordWebhook"])

        if success == False:
            embedColor = 16724787
            embedTitle = "Failed Checkout"
        elif success == True and payment_method == "cc":
            embedColor = 1151440
            embedTitle = "Successful Checkout"
        elif success == True and payment_method == "pp" or success == True and payment_method == "cod":
            embedColor = 182048
            embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Color Skates", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({self.product})", inline=False)
        embed.add_field(name="Size", value="EU " + self.size, inline=False)
        embed.add_field(name="Price", value=price, inline=False)
        embed.add_field(name="Email", value=f"||{self.email}||", inline=False)

        if payment_method == "cod" and success == True:
            embed.add_field(name="Payment Method", value="Cash On Delivery", inline=False)
        elif payment_method == "pp" and success == True:
            embed.add_field(name="Order Number", value="||" + pp_inputs[21].get("value") + "||", inline=False)
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
            embed.add_field(name="Complete Payment", value=f"[Click here]({paypal_post.url})", inline=False)
        elif payment_method == "cc" and success == True:
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
            embed.add_field(name="Complete Payment", value=f"[Click here]({cc_post.url})", inline=False)

        embed.set_thumbnail(url=str(img))
        embed.set_footer(text="WreckAIO", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def publicWebhook(self, payment_method):
        webhook = Webhook("https://discordapp.com/api/webhooks/744218499672571955/RJjjUpW_hJ-usZMUdpj9fshRMUvdSvkC-c4FgR1eFBaj5uIhNKRJeN6feDYWNy1EEIkK")

        embedColor = 9881393
        embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Color Skates", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({self.product})", inline=False)
        embed.add_field(name="Size", value="EU " + self.size, inline=False)
        embed.add_field(name="Price", value=price, inline=False)

        if payment_method == "pp":
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
        elif payment_method == "cc":
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
        elif payment_method == "cod":
            embed.add_field(name="Payment Method", value="Cash On Delivery")
        
        embed.set_thumbnail(url=str(img))
        embed.set_footer(text="WreckAIO • v0.0.1", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def login(self):
        login_post = self.s.post("https://www.colorskates.com/login.php?action=process&method=login", data={"email_address": self.email, "password": self.pw}, headers=self.mainHeaders)
        if login_post.status_code not in (200, 302):
            print(gettime(), colored("Login was not succesful.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.login()
        else:
            print(gettime(), colored("Login successful.", "green"))
            
    def scrape(self):
        global title
        global img
        global price
        global sizesPage
        global sizeId
        global sizes
        
        r = requests.get(self.product)
        if r.status_code not in (200, 302):
            print(gettime(), colored("Error accessing product page.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape()
        else:
            print(gettime(), colored("Product page found.", "yellow"))
        
        page = soup(r.text, "lxml")

        title = page.find("h2").text
        img = "https://colorskates.com/" + str(page.find("img", id="main_products_image")["src"])
        price = page.find("div", class_ = "inner3_top_right").find("strong").text
        oldPrice = page.find("div", class_ = "inner3_top_right").find("strike")
        if oldPrice != None:
            oldPrice = oldPrice.text
            price = price.replace(oldPrice, "")
            price = price.replace(" ", "")
        sizesPage = page.findAll("div", class_="product_option_size")
        if self.size == "random":
            sizes = {}
            for i in sizesPage:
                sizes[i.text.replace("CLICK TO SELECT", "")] = i.get("data-size-value")
        else:
            for i in sizesPage:
                if i.text.replace("CLICK TO SELECT", "") == self.size:
                    sizeId = i.get("data-size-value")
        print(gettime(), colored("Scraped product info.", "green"))

    def addtocart(self):
        #global size
        global sizeId

        if self.size == "random":
            self.size = str(random.choice(list(sizes.keys())))
            sizeId = sizes[self.size]

        atc_post = self.s.post(url=self.product+"?action=add_product", data={"id[2]": sizeId, "quantity": 1, "products_id": int(re.search(r"\d+", self.product).group(0))}, headers=self.mainHeaders)
        if atc_post.status_code not in (200, 302):
            print(gettime(), colored(f"Failed to add to cart [EU {self.size}].", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.addtocart()
        else:
            print(gettime(), colored(f"Added to cart [EU {self.size}].", "green"))
    
    def address(self):
        address_post = self.s.post("https://www.colorskates.com/checkout_shipping.php", data={"action": "process", "shipping": "courier_courier", "comments": ""}, headers=self.mainHeaders)
        if address_post.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit address.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.address()
        else:
            print(gettime(), colored("Submitted address.", "yellow"))
        
    def sitekey_search(self):
        global return_cap

        response = self.s.get("https://www.colorskates.com/checkout_payment.php")
        if response.status_code not in (200, 302):
            print(gettime(), colored("Failed to check for captcha.", "red"))
            time.sleep(int(os.environ["retryDelay"]))
            self.sitekey_search()
        else:
            print(gettime(), colored("Checking for captcha on checkout.", "yellow"))
            
        pages = soup(response.content, "lxml")
        sitekey = pages.find("div", class_="g-recaptcha")
        if sitekey != None:
            print(gettime(), colored("Captcha found on checkout page.", "yellow"))

            sitekey = sitekey["data-sitekey"]
            api_key = os.environ["twoCaptcha"]
            capId = self.s.post(f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={sitekey}&pageurl={response.url}").text.split('|')[1]
            capAnswer = self.s.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={capId}").text
            while "CAPCHA_NOT_READY" in capAnswer:
                print(gettime(), colored("Waiting for captcha response.", "yellow"))
                time.sleep(int(os.environ["errorDelay"]))
                capAnswer = self.s.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={capId}").text
            return_cap = capAnswer.split("|")[1]
            print(gettime(), colored("Captcha solved.", "green"))
        else:
            print(gettime(), colored("No captcha found on checkout.", "yellow"))
            return_cap = None
            
    def cod(self):
        checkout_payload = {
            "payment": "cod",
            "invoice_request": "0",
            "gv_redeem_code": "",
            "cdfy_code": "",
            "comments": ""
        }
        if return_cap != None:
            checkout_payload["g-recaptcha-response"] = return_cap
            
        time.sleep(int(os.environ["checkoutDelay"]))
        checkout = self.s.post("https://www.colorskates.com/checkout_confirmation.php", data=checkout_payload, headers=self.mainHeaders)
        if checkout.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit checkout.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.cod()
        else:
            print(gettime(), colored("Successfully submitted check out.", "green"))

    def send_confirmation(self):
        cod_data = {
            "": "submit",
            "": "custom_btn",
            "": "Confirm Order",
            "": " Confirm Order "
        }

        cod_post = self.s.post("https://www.colorskates.com/checkout_process.php", data=cod_data, headers=self.mainHeaders)
        if cod_post.status_code not in (200, 302):
            self.sendWebhook(payment_method=self.payment, success=False)
            print(gettime(), colored("Failed to complete checkout.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.send_confirmation()
        else:
            self.sendWebhook(payment_method=self.payment, success=True)
            self.publicWebhook(payment_method=self.payment)
            print(gettime(), colored("Successfully checked out.", "green"))
    
    def paypal(self):
        global pp_inputs

        checkout_payload = {
            "payment": "paypal_ipn",
            "invoice_request": "0",
            "gv_redeem_code": "",
            "cdfy_code": "",
            "comments": ""
        }
        if return_cap != None:
            checkout_payload["g-recaptcha-response"] = return_cap
        
        time.sleep(int(os.environ["checkoutDelay"]))
        checkout = self.s.post("https://www.colorskates.com/checkout_confirmation.php", data=checkout_payload, headers=self.mainHeaders)
        if checkout.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit checkout.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.paypal()
        else:
            print(gettime(), colored("Successfully submitted payment.", "green"))
            
            page = soup(checkout.text, "lxml")
            pp_inputs = page.findAll("input", type="hidden")

    def send_paypal(self):
        global paypal_post

        paypal_data = {
            "cmd": "_ext-enter",
            "redirect_cmd": "_xclick",
            "item_name": "COLORSKATES",
            "amount": pp_inputs[3].get("value"),
            "shipping": pp_inputs[4].get("value"),
            "handling": pp_inputs[5].get("value"),
            "business": "info@colorskates.com",
            "address_override": "1",
            "no_shipping": "2",
            "night_phone_b": pp_inputs[9].get("value"),
            "first_name": pp_inputs[10].get("value"),
            "last_name": pp_inputs[11].get("value"),
            "address1": pp_inputs[12].get("value"),
            "address2": pp_inputs[13].get("value"),
            "city": pp_inputs[14].get("value"),
            "zip": pp_inputs[15].get("value"),
            "country": pp_inputs[17].get("value"),
            "email": pp_inputs[18].get("value"),
            "charset": pp_inputs[19].get("value"),
            "currency_code": "EUR",
            "invoice": pp_inputs[21].get("value"),
            "custom": pp_inputs[22].get("value"),
            "no_note": "1",
            "notify_url": "https://www.colorskates.com/ext/modules/payment/paypal_ipn/ipn.php?language=english",
            "cbt": "Complete your Order Confirmation",
            "return": "https://www.colorskates.com/checkout_process.php",
            "cancel_return": "https://www.colorskates.com/checkout_payment.php",
            "bn": pp_inputs[28].get("value"),
            "lc": pp_inputs[29].get("value")
        }

        paypal_post = self.s.post("https://www.paypal.com/cgi-bin/webscr", data=paypal_data, headers=self.paypalHeaders)
        if paypal_post.status_code not in (200, 302):
            self.sendWebhook(payment_method=self.payment, success=False)
            print(gettime(), colored("Failed to complete checkout.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.send_paypal()
        else:
            self.sendWebhook(payment_method=self.payment, success=True)
            self.publicWebhook(payment_method=self.payment)
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))

    def cc(self):
        global cc_inputs

        checkout_payload = {
            "payment": "cardlink",
            "invoice_request": "0",
            "gv_redeem_code": "",
            "cdfy_code": "",
            "comments": ""
        }
        if return_cap != None:
            checkout_payload["g-recaptcha-response"] = return_cap

        time.sleep(int(os.environ["checkoutDelay"]))
        checkout = self.s.post("https://www.colorskates.com/checkout_confirmation.php", data=checkout_payload, headers=self.mainHeaders)
        if checkout.status_code not in (200, 302):
            print(gettime(), colored("Failed to submit payment.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.cc()
        else:
            print(gettime(), colored("Successfully submitted payment.", "green"))
            
            page = soup(checkout.text, "lxml")
            cc_inputs = page.findAll("input", type="hidden")

    def send_cc(self):
        global cc_post

        cc_data = {
            "mid": cc_inputs[0].get("value"),
            "lang": "en",
            "deviceCategory": "0",
            "orderid": cc_inputs[3].get("value"),
            "orderDesc": "COLORSKATES",
            "orderAmount": cc_inputs[5].get("value"),
            "currency": "EUR",
            "payerEmail": cc_inputs[7].get("value"),
            "payerPhone": "",
            "billCountry": cc_inputs[9].get("value"),
            "billState": province,
            "billZip": cc_inputs[11].get("value"),
            "billCity": cc_inputs[12].get("value"),
            "billAddress": cc_inputs[13].get("value"),
            "trType": "1",
            "confirmUrl": "https://www.colorskates.com/checkout_process.php",
            "cancelUrl": "https://www.colorskates.com/checkout_payment.php?error_message=Payment error",
            "var2": cc_inputs[35].get("value"),
            "var3": cc_inputs[36].get("value"),
            "digest": cc_inputs[39].get("value"),
        }

        cc_post = self.s.post("https://www.alphaecommerce.gr/vpos/shophandlermpi", data=cc_data, headers=self.ccHeaders)
        if cc_post.status_code not in (200, 302):
            print(gettime(), colored("Failed to complete checkout.", "red"))
            self.sendWebhook(payment_method=self.payment, success=False)
            time.sleep(int(os.environ["errorDelay"]))
            self.send_cc()
        else:
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))
            self.sendWebhook(payment_method=self.payment, success=True)
            self.publicWebhook(payment_method=self.payment)
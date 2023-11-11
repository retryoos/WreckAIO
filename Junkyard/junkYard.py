from colorama import init
from termcolor import colored
from bs4 import BeautifulSoup as soup
from dhooks import Webhook, Embed
from selenium import webdriver
import os, re, datetime, time, requests, json, threading
init()

# ---To-Do---
# * Add random sizing
# * Add another payment method
# * Clean up code
# * Add threadsNum on logs

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    now = colored(now, "cyan")
    now = '[' + str(now) + ']' + f' [{colored("JunkYard", "cyan")}]'
    return now

class JunkYard():
    def __init__(self, product, size, payment):
        os.system("title WreckAIO - JunkYard")
        self.product = product
        self.size = size
        self.payment = payment
        self.s = requests.Session()

        self.scrape()
        self.addtocart()

        if payment == "pp":
            self.paypal()

    def sendWebhook(self, payment_method, success):
        webhook = Webhook(os.environ["discordWebhook"])

        if success == False:
            embedColor = 16724787
            embedTitle = "Failed Checkout"
        elif success == True and payment_method == "pp":
            embedColor = 1151440
            embedTitle = "Successful Checkout"
        else:
            embedColor = 9881393
            embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Junk Yard", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({self.product})", inline=False)
        embed.add_field(name="Size", value="US " + self.size, inline=False)
        embed.add_field(name="Price", value=price, inline=False)

        if payment_method == "pp" and success == True:
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
            embed.add_field(name="Complete Payment", value=f"[Click here]({paypal_checkout.url})", inline=False)
        else:
            embed.add_field(name="Payment Method", value="Credit Card", inline=False)
        
        embed.set_thumbnail(url=img)
        embed.set_footer(text="WreckAIO", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def publicWebhook(self, payment_method):
        webhook = Webhook("public-webhook")

        embedColor = 9881393
        embedTitle = "Successful Checkout"

        embed = Embed(
            title=embedTitle,
            color=embedColor,
            timestamp="now"
        )

        embed.add_field(name="Website", value="Junk Yard", inline=False)
        embed.add_field(name="Product", value=f"[{title}]({self.product})", inline=False)
        embed.add_field(name="Size", value="US " + self.size, inline=False)
        embed.add_field(name="Price", value=price, inline=False)

        if payment_method == "pp":
            embed.add_field(name="Payment Method", value="PayPal", inline=False)
        elif payment_method == "cc":
            embed.add_field(name="Payment Method", value="CC", inline=False)
        
        embed.set_thumbnail(url=img)
        embed.set_footer(text="WreckAIO • v0.0.1", icon_url="https://pbs.twimg.com/profile_images/1240768756831473664/U7ED98wV_400x400.jpg")

        try:
            webhook.send(embed=embed)
        except Exception:
            print(gettime(), colored("Failed to send webhook.", "red"))
        return

    def scrape(self):
        global img
        global title
        global product_id
        global price

        r = self.s.get(self.product)
        if r.status_code not in (200, 302):
            print(gettime(), colored("Failed to access product page.", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.scrape()
        else:
            print(gettime(), colored("Product page found.", "yellow"))
        
        page = soup(r.text, "lxml")

        product_id = self.s.cookies["VIEWED_PRODUCT_IDS"]
        price = page.find("span", class_="price").text
        title = page.find("title").text
        img = "https://junkyard.com" + str(page.find("img", itemprop="image")['src'])
        print(gettime(), colored("Scraped product information.", "green"))

    def addtocart(self):
        sizes = {
            "4": "390",
            "4.5": "1270",
            "5": "211",
            "5.5": "1265",
            "6": "213",
            "6.5": "1248",
            "7": "109",
            "7.5": "1209",
            "8": "50",
            "8.5": "1202",
            "9": "54",
            "9.5": "1203",
            "10": "58",
            "10.5": "1204",
            "11": "62",
            "11.5": "1208",
            "12": "200"
        }

        atc = self.s.get(f"https://www.junkyard.com/ajax-cart/cart/add?product={int(product_id)}&super_attribute%5B192%5D={int(sizes[self.size])}&qty=1&isAjax=1")
        if atc.status_code not in (200, 302):
            print(gettime(), colored(f"Failed to add to cart [US {self.size}].", "red"))
            time.sleep(int(os.environ["errorDelay"]))
            self.addtocart()
        else:
            print(gettime(), colored(f"Added to cart [US {self.size}].", "green"))

    def paypal(self):
        global paypal_checkout

        paypal_checkout = self.s.get("https://www.junkyard.com/paypal/express/start")
        if paypal_checkout.status_code not in (200, 302):
            print(gettime(), colored("Failed to get paypal checkout link.", "red"))
            self.sendWebhook(payment_method=self.payment, success=False)
            time.sleep(int(os.environ["errorDelay"]))
            self.paypal()
        else:
            print(gettime(), colored("Successfully checked out, complete payment.", "green"))
            self.sendWebhook(payment_method=self.payment, success=True)
            self.publicWebhook(payment_method=self.payment)

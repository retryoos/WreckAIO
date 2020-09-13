'''
s = requests.Session()

product = "https://www.workingclassheroes.co.uk/nike-sb-dunk-high-pro-shoes-black-university-gold__205357"


mainheaders = {
    'authority': 'www.workingclassheroes.co.uk',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
atcheaders = {
    'authority': 'www.workingclassheroes.co.uk',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'origin': 'https://www.workingclassheroes.co.uk/',
    'referer': product
}
r = s.get('https://www.workingclassheroes.co.uk/footwear/trainers/nike-sb-dunk-low-pro-premium-sashiko-shoes-mystic-navy-sail__207564', headers=mainheaders)

data = {"iProductID":product_id,"iQuantity":1,"iAttributeID":pid,"iAttributeDetailID":attribute_id}

atc = s.post('https://www.workingclassheroes.co.uk/wsCitrusStore.asmx/AddToBasketJSNew', json=data, headers=atcheaders)
print(atc.text)
print(atc.status_code)
print(s.cookies["www.workingclassheroes.co.uk_Session"])
'''
'''
product = "https://www.workingclassheroes.co.uk/nike-sb-dunk-high-pro-shoes-black-university-gold__205357"
pid = "21465" #23148
product_id = "205357" #207564

size = str(random.choice(list(sizes.keys())))

#Sashiko attribute ids
sizes = { 
    "UK 7":"178272",
    "UK 7.5":"178273",
    "UK 8":"178274",
    "UK 8.5":"178275",
    "UK 9":"178276",
    "UK 9.5":"178277",
    "UK 10":"178278",
    "UK 10.5":"178279",
    "UK 11":"178280",
    "UK 12":"178281"
}
attribute_id = sizes[size]

attribute_id = "170121"
'''

'''
r = self.s.get(product)
if r.status_code not in (200, 302):
    print(gettime(), colored("Error accessing product page.", "red"))
    time.sleep(int(os.environ["errorDelay"]))
    self.scrape()
else:
    print(gettime(), colored("Product page found.", "yellow"))

page = soup(r.text, "html.parser")

img = "https://www.workingclassheroes.co.uk" + str(page.find("div", {"class":"col-1 css-image-4k imgCtr"})["style"])
img = img.replace("background:url('", "")
img = img.replace("?width=1998&height=1998&quality=85&mode=pad&format=jpg&bgcolor=ffffff') no-repeat center center;", "")
title = page.find("h1", id="devProductName").text
price = page.find("span", id="productPrice").text
print(gettime(), colored("Scraped product info.", "green"))
'''

# in_stock = parsed["d"]["ComingSoon"] # If false, stock is live if true keep looping
'''
if "https://www.paypal.com/cgi-bin/" not in str(paypal_url):
    self.sendWebhook(payment_method=payment, success=False)
    print(gettime(), colored("Failed to check out, Out of Stock.", "red"))
    time.sleep(int(os.environ["errorDelay"]))
    self.paypal()
else:
    self.sendWebhook(payment_method=payment, success=True)
    print(gettime(), colored("Successfully checked out, complete payment.", "green"))
'''
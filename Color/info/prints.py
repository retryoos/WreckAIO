from colorama import init
from termcolor import colored
import datetime, os, threading
from pypresence import Presence
init()

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    threadname = threading.currentThread().getName()
    threadname = str(threadname).replace('Thread', 'Task')
    now = '[' + str(now) + ']' + f' {website} ' + '[' + str(threadname) + ']'
    return now

website = colored("[ColorSkates]", "cyan")
task = colored("[Task 0]", "white")

size = "44"
name = "NIKE SB JANOSKI REMASTERED WHITE/WHITE-UNIVERSITY RED-MIDNIGHT NAVY"

print(gettime(), colored("Loaded 0 proxies.", "white"))
print(gettime(), colored("Loaded 1 task(s).", "white"))
print(gettime(), colored("Logged in successfully.", "yellow"))
print(gettime(), colored("Product found.", "yellow"))
print(gettime(), colored("Scraped product info.", "yellow"))
print(gettime(), colored(f"Adding to cart [EU {size}].", "yellow"))
print(gettime(), colored(f"Added to cart [EU {size}].", "green"))
print(gettime(), colored("Submitting address.", "yellow"))
print(gettime(), colored("Submitted address.", "green"))
print(gettime(), colored("Submitting payment.", "yellow"))
print(gettime(), colored("Successfully checked out.", "green"))
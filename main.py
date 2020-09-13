import os, sys, json, datetime, threading, csv
from termcolor import colored
from pyfiglet import figlet_format
from colorama import init
init(autoreset=True)

def main():
    os.system("title WreckAIO v0.0.1")
    print((colored(figlet_format("Wreck AIO"), "cyan")))

    try:
        with open("Data/Config/config.json", "r") as file:
            data = json.load(file)
            os.environ["discordWebhook"] = data["discordWebhook"]
            os.environ["licenseKey"] = data["licenseKey"]
            os.environ["twoCaptcha"] = data["twoCaptcha"]
            os.environ["checkoutDelay"] = data["checkoutDelay"]
            os.environ["errorDelay"] = data["errorDelay"]

            file.close()
    except Exception as e:
        print(e)
        print(colored("Error while loading config.json.", "red"))
        return False

    if os.environ["licenseKey"] == "" or None:
        os.environ["licenseKey"] = input("Enter your WreckAIO key: ")
        with open("Data/Config/config.json", "w") as outfile:
            data = {
                "discordWebhook": os.environ["discordWebhook"],
                "licenseKey": os.environ["licenseKey"],
                "twoCaptcha": os.environ["twoCaptcha"],
                "checkoutDelay": os.environ["checkoutDelay"],
                "errorDelay": os.environ["errorDelay"]
                }
            json.dump(data, outfile, indent=4)

            outfile.close()

    # Add a License system 
    print("License key successfully validated, welcome to Wreck AIO!")
    print("Choose an option:")
    print("[1] - Color Skates")
    print("[2] - Junk Yard")
    print("[3] - Working Class Heroes")
    print("[4] - Fuel GR")
    print("[5] - Edit config.json")
    print("[6] - Close Wreck AIO")
    choice = str(input("\n" + "==> "))

    if choice == "1":
        import Color.colorSkates as colorSkates

        with open("./Color/tasks.csv", "r") as f_input:
            csv_input = csv.DictReader(f_input)
            i = 0

            for row in csv_input:
                i = i+1

                product = row["Product URL"]
                size = row["Size"]
                email = row["Color Email"]
                pw = row["Color PW"]
                payment = row["Payment"]
                bot = colorSkates.ColorSkates(product, size, email, pw, payment)
                t = threading.Thread(target=bot, args=i) #args=[i, proxies]
                t.start()

    elif choice == "2":
        import Junkyard.junkYard as junkYard

        with open("./Junkyard/tasks.csv", "r") as f_input:
            csv_input = csv.DictReader(f_input)
            i = 0

            for row in csv_input:
                i = i+1

                product = row["Product URL"]
                size = row["Size"]
                payment = row["Payment"]
                bot = junkYard.JunkYard(product, size, payment)
                t = threading.Thread(target=bot, args=i) #args=[i, proxies]
                t.start()
    elif choice == "3":
        import WorkingClassHeroes.workingClassHeroes as workingClassHeroes
        heroes = workingClassHeroes.Heroes()
    elif choice == "4":
        import Fuel.fuelGR as fuelGR
        fuel = fuelGR.FuelGr()
    elif choice == "5":
        print("Webhook:", os.environ["discordWebhook"])
        print("License key:", os.environ["licenseKey"])
        print("2Captcha key:", os.environ["twoCaptcha"])
        print("Checkout delay:", os.environ["checkoutDelay"])
        print("Error delay:", os.environ["errorDelay"] + "\n")
        os.environ["discordWebhook"] = input("Webhook: ")
        os.environ["licenseKey"] = input("License key: ")
        os.environ["twoCaptcha"] = input("2Captcha key: ")
        os.environ["checkoutDelay"] = input("Checkout delay: ")
        os.environ["errorDelay"] = input("Error delay: ")
        with open("Data/Config/config.json", "w") as outfile:
            data = {
                "discordWebhook": os.environ["discordWebhook"],
                "licenseKey": os.environ["licenseKey"],
                "twoCaptcha": os.environ["twoCaptcha"],
                "checkoutDelay": os.environ["checkoutDelay"],
                "errorDelay": os.environ["errorDelay"]
            }
            json.dump(data, outfile, indent=4)

            outfile.close()
    elif choice == "6":
        print("\nWreck AIO, exiting..")
        sys.exit(0)
    else:
        print("Please choose a valid choice.")
        main()

if __name__ == "__main__":
    main()
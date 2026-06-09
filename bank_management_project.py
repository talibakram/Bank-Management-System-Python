# ----BANK MANAGEMENT PROJECT----

import json
import random
import string
import datetime
from pathlib import Path


class Bank:
    database = "bankdata.json"
    data = []
    try:

        if Path(database).exists():

            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file exists!")

    except Exception as err:
        print(f"An error occurred as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(Bank.data, indent=4))

    @classmethod
    def __generatenumber(cls):
        alpha = random.choices(string.ascii_letters, k=4)
        nums = random.choices(string.digits, k=8)

        id = alpha + nums
        random.shuffle(id)
        return "".join(id)

    def createaccount(self):
        name = input("Enter your full name: ")
        while True:
            try:
                age = int(input("Enter your age (You must be 18 or above): "))
                break
            except ValueError:
                print("Age must be in numbers only!")
        while True:
            try:
                phonenumber = int(
                    input(
                        "Enter yoor 11 digits phone number registered on your id card: "
                    )
                )

            except ValueError:
                print("Phone number must be in digits!")
                continue
            existingphone = [i for i in Bank.data if i["Phone Number"] == phonenumber]
            if len(existingphone) > 0:
                print(
                    "-" * 30,
                    "\nUser with this phone number already exists!\n",
                    "-" * 30,
                )
                continue
            else:
                break

        while True:
            email = input("Enter your email adress: ")
            existingemail = [i for i in Bank.data if i["Email"] == email]
            if len(existingemail) > 0:
                print("-" * 30, "\nUser with this email already exists!\n", "-" * 30)
                continue
            else:
                break

        while True:
            try:
                pin = int(input("Create your 4 digits pin: "))
                if len(str(pin)) != 4:
                    print("Pin must be exactly 4 digits long!")
                    continue
                break
            except ValueError:
                print("Pin must be in digits!")

        info = {
            "Name": name,
            "Age": age,
            "Phone Number": phonenumber,
            "Email": email,
            "Pin": pin,
            "AccNo": Bank.__generatenumber(),
            "Balance": 0,
            "Transactions": [],
        }
        if info["Age"] < 18:
            print("Sorry you are under 18, so you can't create account!")
        else:
            print("---Account created successfully---")
            print("Here's your account details")
            for i in info:
                print(f"{i} : {info[i]}")
            print(
                "Please note down your account number & don't share your pin with anyone!"
            )

            Bank.data.append(info)
            self.__update()

    def depositmoney(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
                continue
            else:
                while True:
                    try:
                        amount = int(
                            input(
                                "Enter amount you want to deposit (or press 0 to cancel): "
                            )
                        )
                    except ValueError:
                        print("Amount must be in numerical form!")
                        continue
                    if amount == 0:
                        print(
                            "-----------------------\n[!] Transaction cancelled.\n-----------------------"
                        )
                        return

                    elif amount > 50000:
                        print("Maximum deposit limit is 0 - 50000 ")
                        continue
                    elif amount < 0:
                        print("You can not deposit negative amount!")
                        continue
                    else:

                        userdata[0]["Balance"] += amount
                        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        transaction = f"Deposited Rs.{amount} on {time}"
                        userdata[0]["Transactions"].append(transaction)
                        self.__update()
                        print(f"---Rs.{amount} deposited successfully!---")
                        return

    def withdrawmoney(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
                continue
            else:
                while True:
                    try:
                        amount = int(
                            input(
                                "Enter amount you want to withdraw (or press 0 to cancel): "
                            )
                        )

                    except ValueError:
                        print("Amount must be in digits!")
                        continue

                    if amount == 0:
                        print(
                            "-----------------------\n[!] Transaction cancelled.\n-----------------------"
                        )
                        return

                    elif userdata[0]["Balance"] < amount:
                        print(f"Insufficient Balance!")
                        continue

                    elif amount < 0:
                        print("Sorry you can not withdraw negative amount!")
                        continue

                    else:
                        userdata[0]["Balance"] -= amount
                        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        transaction = f"withdrew Rs.{amount} on {time}"
                        userdata[0]["Transactions"].append(transaction)
                        Bank.__update()
                        print(f"---Rs.{amount} withdrawn Successfully!---")
                        return

    def showdetails(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")
            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
                continue

            else:
                print("Here's your account details \n" + "-" * 30)
                for i in userdata[0]:
                    if i != "Transactions":
                        print(f"{i} : {userdata[0][i]}")
                break

    def updatedetails(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")
            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
                continue

            else:
                print(
                    "You can change the detalis below\nYou can leave the field empty if you don't want to change"
                )

            newdata = {
                "Name": input("Enter your new name: "),
                "Email": input("Enter your new email: "),
                "Phone Number": input("Enter your new phone number: "),
                "Pin": input("Enter your new pin: "),
            }

            if newdata["Name"] == "":
                newdata["Name"] = userdata[0]["Name"]
            if newdata["Email"] == "":
                newdata["Email"] = userdata[0]["Email"]
            if newdata["Phone Number"] == "":
                newdata["Phone Number"] = userdata[0]["Phone Number"]
            if newdata["Pin"] == "":
                newdata["Pin"] = userdata[0]["Pin"]

            try:

                if type(newdata["Pin"]) == str:
                    newdata["Pin"] = int(newdata["Pin"])

                if type(newdata["Phone Number"]) == str:
                    newdata["Phone Number"] = int(newdata["Phone Number"])

            except ValueError:
                print(
                    "[!] Phone Number and Pin must be in digits! \nUpdate failed! Try again."
                )
                continue

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("Details updated successfully")
            break

    def delete(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
                continue
            else:
                check = input("Do you really want to delete your account, 'Y/N'? : ")
            if check == "N" or check == "n":
                break

            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank.__update()
                print("Account deleted successfully")
                break

    def checkbalance(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")

            else:
                print(f"Your Balance is: {userdata[0]["Balance"]}")
                break

    def transfermoney(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your pin: "))
                    break
                except ValueError:
                    print(f"Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")

            else:
                break
        while True:
            accnumber2 = input("Enter receiver's account number: ")
            while True:
                try:
                    phonenumber2 = int(input("Enter receiver's phone number: "))
                    break
                except ValueError:
                    print("Phone number must be in digits!")

            if accnumber2 == accnumber:
                print("Invalid Receiver! Cannot transfer to your own account.")
                continue
            if phonenumber2 == userdata[0]["Phone Number"]:
                print("Invalid Receiver! Cannot transfer to your own account.")
                continue
            else:
                userdata2 = [
                    j
                    for j in Bank.data
                    if j["AccNo"] == accnumber2 and j["Phone Number"] == phonenumber2
                ]

                if len(userdata2) == 0:
                    print(
                        "Receiver not found! Please enter correct receiver's details."
                    )

                else:
                    break
        while True:
            try:
                amount = int(input("Enter amount you want to send: "))
            except ValueError:
                print("Invalid input, please enter amount in digits!")
                continue
            if userdata[0]["Balance"] < amount:
                print("Insufficient Balance! Please add funds to your account.")
            elif amount == 0:
                print("You can not send 0 amount!")
            elif amount < 0:
                print("You can not send negative amount!")
            else:
                userdata[0]["Balance"] -= amount
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction = f"Transfered Rs.{amount} on {time}"
                userdata[0]["Transactions"].append(transaction)
                userdata2[0]["Balance"] += amount

                transaction2 = f"Recieved Rs.{amount} on {time}"
                userdata2[0]["Transactions"].append(transaction2)
                self.__update()
                print(f"---Rs.{amount} sent successfully!---")
                break

    def transactionhistroy(self):
        while True:
            accnumber = input("Enter your account number: ")
            while True:
                try:
                    pin = int(input("Enter your 4 digit pin: "))
                    break
                except ValueError:
                    print("Pin must be in digits!")

            userdata = [
                i for i in Bank.data if i["AccNo"] == accnumber and i["Pin"] == pin
            ]

            if len(userdata) == 0:
                print("Invalid Credentials! Try Again.")
            else:
                break

        print("\n---Transaction Histroy---\n")
        histroy = userdata[0]["Transactions"]
        if len(histroy) == 0:
            print("0 transactions yet!")
        else:
            for record in histroy:
                print(record)
                print("-----------------------------")


user = Bank()

while True:
    print("\n----WELCOME TO BANK SYSTEM----\n")
    print("1. Create Account")
    print("2. Check Balance")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. View Account Details")
    print("7. View Transaction History")
    print("8. Update Details")
    print("9. Delete Bank Account")
    print("0. Logout/Exit")

    check = int(input("Enter your response: "))

    if check == 1:
        user.createaccount()

    elif check == 2:
        user.checkbalance()

    elif check == 3:
        user.depositmoney()

    elif check == 4:
        user.withdrawmoney()

    elif check == 5:
        user.transfermoney()

    elif check == 6:
        user.showdetails()

    elif check == 7:
        user.transactionhistroy()

    elif check == 8:
        user.updatedetails()

    elif check == 9:
        user.delete()

    elif check == 0:
        print("Thankyou for using our system, Good Bye!")
        break

    else:
        print("Invalid input, please try again!")

    if check != 0:
        input("Press Enter to return to Main Menu...!")

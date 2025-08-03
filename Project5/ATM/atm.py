balance = 0

while True:
    print("\n......Enter Your Choice ......")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = int(input("Enter Your Choice: "))

    if choice == 1:
        print("Total Balance : ", balance)

    elif choice == 2:
        amount = int(input("Enter the amount to deposit: "))
        if amount > 0:
            balance += amount
            print("Total Balance is : ", balance)
        else:
            print("Invalid Amount")

    elif choice == 3:
        amount = int(input("Enter the amount to withdraw: "))
        if amount > 0:
            if balance < amount:
                print("Insufficient Balance")
                print("Available Balance : ", balance)
            else:
                balance -= amount
                print("Total Balance : ", balance)
        else:
            print("Error: Invalid withdrawal amount.")

    elif choice == 4:
        print("Thank you for using our services.")
        break

    else:
        print("Invalid Choice. Please enter between 1 to 4.")

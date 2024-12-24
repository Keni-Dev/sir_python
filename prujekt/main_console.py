from datetime import datetime
import random

accounts = []
current_account_index = None

def generate_account_number():
    while True:
        acc_num = str(random.randint(1, 99))
        if not any(account['account_number'] == acc_num for account in accounts):
            return acc_num

def create_account():
    print("\n=== Create New Account ===")
    name = input("Enter your full name: ")

    while True:
        pin = input("Create a 4-digit PIN: ")
        if len(pin) == 4 and pin.isdigit():
            break
        print("Invalid PIN. Please enter 4 digits.")

    initial_deposit = float(input("Enter initial deposit amount: ₱"))

    account = {
        'account_number': generate_account_number(),
        'name': name,
        'pin': pin,
        'balance': initial_deposit,
        'transaction_history': []
    }

    accounts.append(account)

    print("\nAccount created successfully!")
    generate_receipt("ACCOUNT CREATION", account, initial_deposit)

def add_transaction(account_index, transaction_type, amount, recipient=None):
    timestamp = datetime.now()
    transaction = {
        'type': transaction_type,
        'amount': amount,
        'timestamp': timestamp,
        'recipient': recipient,
        'balance_after': accounts[account_index]['balance']
    }
    accounts[account_index]['transaction_history'].append(transaction)

def login():
    global current_account_index
    print("\n=== Login ===")
    account_number = input("Enter account number: ")
    pin = input("Enter PIN: ")

    for i, account in enumerate(accounts):
        if account['account_number'] == account_number and account['pin'] == pin:
            current_account_index = i
            print(f"\nWelcome, {account['name']}!")
            return True
    print("Invalid account number or PIN.")
    current_account_index = None  # if login fail
    return False

def check_balance():
    if current_account_index is None:
        print("You are not logged in.")
        return

    account = accounts[current_account_index]
    print(f"\nCurrent Balance: ₱{account['balance']:.2f}")
    generate_receipt("BALANCE INQUIRY", account)

def deposit():
    if current_account_index is None:
        print("You are not logged in.")
        return

    amount = float(input("\nEnter deposit amount: ₱"))
    if amount <= 0:
        print("Invalid amount.")
        return

    accounts[current_account_index]['balance'] += amount
    add_transaction(current_account_index, "DEPOSIT", amount)
    print(f"Deposit successful. New balance: ₱{accounts[current_account_index]['balance']:.2f}")
    generate_receipt("DEPOSIT", accounts[current_account_index], amount)

def withdraw():
    if current_account_index is None:
        print("You are not logged in.")
        return

    amount = float(input("\nEnter withdrawal amount: ₱"))
    if amount <= 0:
        print("Invalid amount.")
        return
    if amount > accounts[current_account_index]['balance']:
        print("Insufficient funds.")
        return

    accounts[current_account_index]['balance'] -= amount
    add_transaction(current_account_index, "WITHDRAWAL", amount)
    print(f"Withdrawal successful. New balance: ₱{accounts[current_account_index]['balance']:.2f}")
    generate_receipt("WITHDRAWAL", accounts[current_account_index], amount)

def transfer():
    if current_account_index is None:
        print("You are not logged in.")
        return

    recipient_acc = input("\nEnter recipient's account number: ")
    recipient_index = None

    for i, account in enumerate(accounts):
        if account['account_number'] == recipient_acc:
            recipient_index = i
            break

    if recipient_index is None:
        print("Recipient account not found.")
        return

    amount = float(input("Enter transfer amount: ₱"))
    if amount <= 0:
        print("Invalid amount.")
        return
    if amount > accounts[current_account_index]['balance']:
        print("Insufficient funds.")
        return

    # perform transfer
    accounts[current_account_index]['balance'] -= amount
    accounts[recipient_index]['balance'] += amount

    # record transactions for both accounts
    add_transaction(current_account_index, "TRANSFER", amount, recipient_acc)
    add_transaction(recipient_index, "TRANSFER RECEIVED", amount, accounts[current_account_index]['account_number'])

    print(f"Transfer successful. New balance: ₱{accounts[current_account_index]['balance']:.2f}")
    generate_receipt("TRANSFER", accounts[current_account_index], amount, accounts[recipient_index])

def view_transaction_history():
    if current_account_index is None:
        print("You are not logged in.")
        return

    print("\n=== Transaction History ===")
    for transaction in accounts[current_account_index]['transaction_history']:
        print(f"\nType: {transaction['type']}")
        print(f"Amount: ₱{transaction['amount']:.2f}")
        print(f"Date: {transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Balance After: ₱{transaction['balance_after']:.2f}")
        if transaction['recipient']:
            print(f"Recipient: {transaction['recipient']}")
        print("-" * 40)

def generate_receipt(transaction_type, account, amount=None, recipient=None):
    print("\n" + "=" * 40)
    print(f"{'TRANSACTION RECEIPT':^40}")
    print("=" * 40)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Transaction Type: {transaction_type}")
    print(f"Account Number: {account['account_number']}")
    print(f"Account Holder: {account['name']}")

    if amount is not None:
        print(f"Amount: ₱{amount:.2f}")

    if recipient:
        print(f"Recipient Account: {recipient['account_number']}")
        print(f"Recipient Name: {recipient['name']}")

    print(f"Current Balance: ₱{account['balance']:.2f}")
    print("=" * 40)
    print("Thank you for banking with us!")
    print("=" * 40 + "\n")

def change_pin():
    if current_account_index is None:
        print("You are not logged in.")
        return

    account = accounts[current_account_index]

    # Verify current PIN
    current_pin = input("\nEnter your current PIN: ")
    if current_pin != account['pin']:
        print("Incorrect current PIN.")
        return

    # Get new PIN
    while True:
        new_pin = input("Enter your new 4-digit PIN: ")
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("Invalid PIN. Please enter 4 digits.")
            continue
        confirm_pin = input("Confirm your new PIN: ")
        if new_pin != confirm_pin:
            print("PINs do not match. Please try again.")
            continue
        break

    # Update the PIN
    account['pin'] = new_pin

    # Record the PIN change in transaction history
    add_transaction(current_account_index, "PIN CHANGE", 0)

    print("PIN changed successfully.")
    generate_receipt("PIN CHANGE", account)

def main():
    while True:
        print("\n=== ATM Banking System ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            if login():
                while True:
                    print("\n=== Main Menu ===")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer")
                    print("5. Transaction History")
                    print("6. Change PIN")
                    print("7. Logout")

                    operation = input("Enter your choice (1-7): ")

                    if operation == "1":
                        check_balance()
                    elif operation == "2":
                        deposit()
                    elif operation == "3":
                        withdraw()
                    elif operation == "4":
                        transfer()
                    elif operation == "5":
                        view_transaction_history()
                    elif operation == "6":
                        change_pin()
                    elif operation == "7":
                        global current_account_index
                        current_account_index = None
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                continue
        elif choice == "3":
            print("Thank you for using our ATM Banking System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
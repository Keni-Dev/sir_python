import pytest
from datetime import datetime
import io
from unittest.mock import patch
import random

# Your ATM code (atm.py)
# Global lists to store data
from datetime import datetime
import random

# Global lists to store data
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

    return

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
    current_account_index = None  # Explicitly set to None on failed login
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

    # Perform transfer
    accounts[current_account_index]['balance'] -= amount
    accounts[recipient_index]['balance'] += amount

    # Record transactions for both accounts
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
                    print("6. Logout")

                    operation = input("Enter your choice (1-6): ")

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
                        global current_account_index
                        current_account_index = None
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                continue  # Go back to main menu if login fails.
        elif choice == "3":
            print("Thank you for using our ATM Banking System.")
            break
        else:
            print("Invalid choice. Please try again.")

@pytest.fixture
def test_account():
    global accounts
    accounts = [] #Clear accounts before each test
    account = {
        'account_number': '12',
        'name': 'Test User',
        'pin': '1234',
        'balance': 1000.0,
        'transaction_history': []
    }
    accounts.append(account)
    global current_account_index
    current_account_index = 0
    return account

def test_generate_account_number():
    global accounts
    accounts = []
    num1 = generate_account_number()
    assert num1 is not None
    accounts.append({'account_number': num1})
    num2 = generate_account_number()
    assert num2 is not None
    assert num1 != num2

def test_create_account(monkeypatch):
    inputs = iter(['Test User', '1234', '1000'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_account()
    assert len(accounts) == 1
    assert accounts[0]['name'] == 'Test User'
    assert accounts[0]['pin'] == '1234'
    assert accounts[0]['balance'] == 1000.0

def test_create_account_invalid_pin(monkeypatch):
    inputs = iter(['Test User', '123', '12345', '1234', '1000'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_account()
    assert len(accounts) == 1

def test_login_success(test_account):
    inputs = iter(['12', '1234'])
    with patch('builtins.input', lambda _: next(inputs)):
        assert login() is True
        assert current_account_index == 0

def test_login_fail_account_number():
    inputs = iter(['99', '1234'])
    with patch('builtins.input', lambda _: next(inputs)):
        assert login() is False
        assert current_account_index is None

def test_login_fail_pin():
    inputs = iter(['12', '0000'])
    with patch('builtins.input', lambda _: next(inputs)):
        assert login() is False
        assert current_account_index is None

def test_check_balance(test_account, capsys):
    check_balance()
    captured = capsys.readouterr()
    assert "Current Balance: ₱1000.00" in captured.out

def test_deposit(test_account):
    inputs = iter(['500'])
    with patch('builtins.input', lambda _: next(inputs)):
        deposit()
    assert accounts[0]['balance'] == 1500.0

def test_deposit_invalid(test_account, capsys):
    inputs = iter(['-500'])
    with patch('builtins.input', lambda _: next(inputs)):
        deposit()
    captured = capsys.readouterr()
    assert "Invalid amount." in captured.out
    assert accounts[0]['balance'] == 1000.0

def test_withdraw_sufficient_funds(test_account):
    inputs = iter(['500'])
    with patch('builtins.input', lambda _: next(inputs)):
        withdraw()
    assert accounts[0]['balance'] == 500.0

def test_withdraw_insufficient_funds(test_account, capsys):
    inputs = iter(['1500'])
    with patch('builtins.input', lambda _: next(inputs)):
        withdraw()
    captured = capsys.readouterr()
    assert "Insufficient funds." in captured.out
    assert accounts[0]['balance'] == 1000.0

def test_withdraw_invalid_amount(test_account, capsys):
    inputs = iter(['-500'])
    with patch('builtins.input', lambda _: next(inputs)):
        withdraw()
    captured = capsys.readouterr()
    assert "Invalid amount." in captured.out
    assert accounts[0]['balance'] == 1000.0

def test_transfer_success(test_account):
    accounts.append({'account_number': '13', 'name': 'Recipient', 'pin': '5678', 'balance': 500, 'transaction_history': []})
    inputs = iter(['13', '500'])
    with patch('builtins.input', lambda _: next(inputs)):
        transfer()
    assert accounts[0]['balance'] == 500.0
    assert accounts[1]['balance'] == 1000.0

def test_transfer_recipient_not_found(test_account, capsys):
    inputs = iter(['99', '500'])
    with patch('builtins.input', lambda _: next(inputs)):
        transfer()
    captured = capsys.readouterr()
    assert "Recipient account not found." in captured.out
    assert accounts[0]['balance'] == 1000.0

def test_transfer_insufficient_funds(test_account, capsys):
    accounts.append({'account_number': '13', 'name': 'Recipient', 'pin': '5678', 'balance': 500, 'transaction_history': []})
    inputs = iter(['13', '1500'])
    with patch('builtins.input', lambda _: next(inputs)):
        transfer()
    captured = capsys.readouterr()
    assert "Insufficient funds." in captured.out
    assert accounts[0]['balance'] == 1000.0

def test_view_transaction_history(test_account, capsys):
    add_transaction(0, "TEST", 100)
    view_transaction_history()
    captured = capsys.readouterr()
    assert "Type: TEST" in captured.out
    assert "Amount: ₱100.00" in captured.out

def test_generate_receipt(test_account, capsys):
    generate_receipt("TEST", test_account, 500)
    captured = capsys.readouterr()
    assert "TRANSACTION RECEIPT" in captured.out
    assert "Amount: ₱500.00" in captured.out

def test_generate_receipt_transfer(test_account, capsys):
    recipient = {'account_number': '13', 'name': 'Recipient', 'balance': 500}
    generate_receipt("TRANSFER", test_account, 500, recipient)
    captured = capsys.readouterr()
    assert "Recipient Account: 13" in captured.out
    assert "Recipient Name: Recipient" in captured.out
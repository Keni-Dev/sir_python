from datetime import datetime
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich.style import Style
import time

console = Console()

# Styles
HEADER_STYLE = Style(color="blue", bold=True)
SUCCESS_STYLE = Style(color="green", bold=True)
ERROR_STYLE = Style(color="red", bold=True)
HIGHLIGHT_STYLE = Style(color="yellow")

accounts = []
current_account_index = None

def clear_screen():
    console.clear()

def display_header(text):
    header = Panel(
        Align.center(Text(text, style=HEADER_STYLE)),
        border_style="blue",
        padding=(1, 2)
    )
    console.print(header)

def display_message(message, style="default"):
    if style == "error":
        console.print(Panel(message, style=ERROR_STYLE, border_style="red"))
    elif style == "success":
        console.print(Panel(message, style=SUCCESS_STYLE, border_style="green"))
    else:
        console.print(Panel(message))
    time.sleep(1.5)  # Give users time to read the message

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

def generate_account_number():
    while True:
        acc_num = str(random.randint(1, 20))
        if not any(account['account_number'] == acc_num for account in accounts):
            return acc_num

def create_account():
    clear_screen()
    display_header("Create New Account")
    
    name = Prompt.ask("[blue]Enter your full name")
    
    while True:
        pin = Prompt.ask("[blue]Create a 4-digit PIN", password=True)
        if len(pin) == 4 and pin.isdigit():
            break
        display_message("Invalid PIN. Please enter 4 digits.", "error")
    
    initial_deposit = FloatPrompt.ask("[blue]Enter initial deposit amount (₱)")
    
    account = {
        'account_number': generate_account_number(),
        'name': name,
        'pin': pin,
        'balance': initial_deposit,
        'transaction_history': []
    }
    
    accounts.append(account)
    display_message(f"Account created successfully!\nYour account number is: {account['account_number']}", "success")
    generate_receipt("ACCOUNT CREATION", account, initial_deposit)

def check_balance():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return

    clear_screen()
    display_header("Balance Inquiry")
    
    account = accounts[current_account_index]
    balance_table = Table(show_header=False, border_style="blue")
    balance_table.add_column("Key", style="cyan")
    balance_table.add_column("Value", style="yellow")
    
    balance_table.add_row("Account Number", account['account_number'])
    balance_table.add_row("Account Holder", account['name'])
    balance_table.add_row("Current Balance", f"₱{account['balance']:,.2f}")
    
    console.print(Panel(balance_table, border_style="blue", padding=(1, 2)))
    input("\nPress Enter to continue...")

def deposit():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return

    clear_screen()
    display_header("Deposit")
    
    amount = FloatPrompt.ask("[blue]Enter deposit amount (₱)")
    if amount <= 0:
        display_message("Invalid amount.", "error")
        return

    accounts[current_account_index]['balance'] += amount
    add_transaction(current_account_index, "DEPOSIT", amount)
    display_message(f"Deposit successful.\nNew balance: ₱{accounts[current_account_index]['balance']:,.2f}", "success")
    generate_receipt("DEPOSIT", accounts[current_account_index], amount)

def withdraw():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return

    clear_screen()
    display_header("Withdrawal")
    
    amount = FloatPrompt.ask("[blue]Enter withdrawal amount (₱)")
    if amount <= 0:
        display_message("Invalid amount.", "error")
        return
    if amount > accounts[current_account_index]['balance']:
        display_message("Insufficient funds.", "error")
        return

    accounts[current_account_index]['balance'] -= amount
    add_transaction(current_account_index, "WITHDRAWAL", amount)
    display_message(f"Withdrawal successful.\nNew balance: ₱{accounts[current_account_index]['balance']:,.2f}", "success")
    generate_receipt("WITHDRAWAL", accounts[current_account_index], amount)

def transfer():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return

    clear_screen()
    display_header("Transfer")
    
    recipient_acc = Prompt.ask("[blue]Enter recipient's account number")
    recipient_index = None

    for i, account in enumerate(accounts):
        if account['account_number'] == recipient_acc:
            recipient_index = i
            break

    if recipient_index is None:
        display_message("Recipient account not found.", "error")
        return

    amount = FloatPrompt.ask("[blue]Enter transfer amount (₱)")
    if amount <= 0:
        display_message("Invalid amount.", "error")
        return
    if amount > accounts[current_account_index]['balance']:
        display_message("Insufficient funds.", "error")
        return

    # Perform transfer
    accounts[current_account_index]['balance'] -= amount
    accounts[recipient_index]['balance'] += amount

    # Record transactions for both accounts
    add_transaction(current_account_index, "TRANSFER", amount, recipient_acc)
    add_transaction(recipient_index, "TRANSFER RECEIVED", amount, accounts[current_account_index]['account_number'])

    display_message(f"Transfer successful.\nNew balance: ₱{accounts[current_account_index]['balance']:,.2f}", "success")
    generate_receipt("TRANSFER", accounts[current_account_index], amount, accounts[recipient_index])

def change_pin():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return

    clear_screen()
    display_header("Change PIN")
    
    account = accounts[current_account_index]
    current_pin = Prompt.ask("[blue]Enter your current PIN", password=True)
    
    if current_pin != account['pin']:
        display_message("Incorrect current PIN.", "error")
        return

    while True:
        new_pin = Prompt.ask("[blue]Enter your new 4-digit PIN", password=True)
        if len(new_pin) != 4 or not new_pin.isdigit():
            display_message("Invalid PIN. Please enter 4 digits.", "error")
            continue
            
        confirm_pin = Prompt.ask("[blue]Confirm your new PIN", password=True)
        if new_pin != confirm_pin:
            display_message("PINs do not match. Please try again.", "error")
            continue
        break

    account['pin'] = new_pin
    add_transaction(current_account_index, "PIN CHANGE", 0)
    display_message("PIN changed successfully.", "success")
    generate_receipt("PIN CHANGE", account)

def generate_receipt(transaction_type, account, amount=None, recipient=None):
    receipt = Table(show_header=False, border_style="blue")
    receipt.add_column("Key", style="cyan")
    receipt.add_column("Value", style="yellow")
    
    receipt.add_row("TRANSACTION RECEIPT", "")
    receipt.add_row("Date", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    receipt.add_row("Transaction Type", transaction_type)
    receipt.add_row("Account Number", account['account_number'])
    receipt.add_row("Account Holder", account['name'])
    
    if amount is not None:
        receipt.add_row("Amount", f"₱{amount:,.2f}")
    
    if recipient:
        receipt.add_row("Recipient Account", recipient['account_number'])
        receipt.add_row("Recipient Name", recipient['name'])
    
    receipt.add_row("Current Balance", f"₱{account['balance']:,.2f}")
    
    console.print(Panel(receipt, title="Receipt", border_style="blue", padding=(1, 2)))
    input("\nPress Enter to continue...")

def view_transaction_history():
    if current_account_index is None:
        display_message("You are not logged in.", "error")
        return
        
    clear_screen()
    display_header("Transaction History")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type")
    table.add_column("Amount")
    table.add_column("Date")
    table.add_column("Balance After")
    table.add_column("Recipient")
    
    for transaction in accounts[current_account_index]['transaction_history']:
        table.add_row(
            transaction['type'],
            f"₱{transaction['amount']:,.2f}",
            transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            f"₱{transaction['balance_after']:,.2f}",
            transaction['recipient'] if transaction['recipient'] else "-"
        )
    
    console.print(Panel(table, border_style="blue", padding=(1, 2)))
    input("\nPress Enter to continue...")

def login():
    global current_account_index
    clear_screen()
    display_header("Login")
    
    account_number = Prompt.ask("[blue]Enter account number")
    pin = Prompt.ask("[blue]Enter PIN", password=True)
    
    for i, account in enumerate(accounts):
        if account['account_number'] == account_number and account['pin'] == pin:
            current_account_index = i
            display_message(f"Welcome, {account['name']}!", "success")
            return True
            
    display_message("Invalid account number or PIN.", "error")
    current_account_index = None
    return False

def display_menu(title, options):
    clear_screen()
    display_header(title)
    
    menu_table = Table(show_header=False, border_style="blue", box=None)
    menu_table.add_column("Option", style="cyan")
    menu_table.add_column("Description", style="yellow")
    
    for key, value in options.items():
        menu_table.add_row(f"[{key}]", value)
    
    console.print(Panel(menu_table, border_style="blue", padding=(1, 2)))
    
    choice = Prompt.ask("[blue]Enter your choice", choices=list(options.keys()))
    return choice

def main():
    while True:
        main_options = {
            "1": "Create Account",
            "2": "Login",
            "3": "Exit"
        }
        
        choice = display_menu("ATM Banking System", main_options)
        
        if choice == "1":
            create_account()
        elif choice == "2":
            if login():
                while True:
                    logged_in_options = {
                        "1": "Check Balance",
                        "2": "Deposit",
                        "3": "Withdraw",
                        "4": "Transfer",
                        "5": "Transaction History",
                        "6": "Change PIN",
                        "7": "Logout"
                    }
                    
                    operation = display_menu("Main Menu", logged_in_options)
                    
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
                        display_message("Logged out successfully.", "success")
                        break
            else:
                continue
        elif choice == "3":
            display_message("Thank you for using our ATM Banking System.", "success")
            break

if __name__ == "__main__":
    main()
import random, os, sys, time
import tkinter as tk
import ttkbootstrap as tbs
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt, FloatPrompt
from rich.style import Style

# --- Shared Data and Functions ---
accounts = []
current_account_index = None

def generate_account_number():
    while True:
        acc_num = str(random.randint(1, 99))
        if not any(account['account_number'] == acc_num for account in accounts):
            return acc_num

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


# --- TUI (Rich) Interface ---
def run_tui():
    console = Console()
    HEADER_STYLE = Style(color="blue", bold=True)
    SUCCESS_STYLE = Style(color="green", bold=True)
    ERROR_STYLE = Style(color="red", bold=True)

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
        time.sleep(1.5)

    def generate_receipt_tui(transaction_type, account, amount=None, recipient=None):
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

    def view_transaction_history_tui():
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

    def login_tui():
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
    def create_account_tui():
        clear_screen()
        display_header("Create New Account")

        while True:
            name = Prompt.ask("[blue]Enter your full name")
            if not name or any(char.isdigit() for char in name):
                display_message("Invalid name.", "error")
                continue
            break

        while True:
            pin = Prompt.ask("[blue]Create a 4-digit PIN [red](hidden)", password=True)
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
        generate_receipt_tui("ACCOUNT CREATION", account, initial_deposit)

    def check_balance_tui():
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

    def deposit_tui():
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
        generate_receipt_tui("DEPOSIT", accounts[current_account_index], amount)

    def withdraw_tui():
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
        generate_receipt_tui("WITHDRAWAL", accounts[current_account_index], amount)

    def transfer_tui():
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
        generate_receipt_tui("TRANSFER", accounts[current_account_index], amount, accounts[recipient_index])

    def change_pin_tui():
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
        generate_receipt_tui("PIN CHANGE", account)


    while True:
        main_options = {
            "1": "Create Account",
            "2": "Login",
            "3": "Exit"
        }

        choice = display_menu("ATM Banking System", main_options)

        if choice == "1":
            create_account_tui()
        elif choice == "2":
            if login_tui():
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
                        check_balance_tui()
                    elif operation == "2":
                        deposit_tui()
                    elif operation == "3":
                        withdraw_tui()
                    elif operation == "4":
                        transfer_tui()
                    elif operation == "5":
                        view_transaction_history_tui()
                    elif operation == "6":
                        change_pin_tui()
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

# --- GUI (Tkinter) Interface ---
class ATMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Banking System")
        self.root.geometry("600x600")
        self.center_window()

        self.button_pady = 7.5
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.style = tbs.Style(theme="superhero")
        self.style.configure("TButton", \
                             background="#4997A9", \
                             foreground="#F4F4F4", \
                             borderwidth=1, \
                             focuscolor="#75D1C5", \
                             relief="flat", 
                             width=20,
                             padding=(10),
                             font=('Segoe UI Variable Text Semibold', 9))
        self.style.map("TButton", background=[('active', '#75D1C5')])

        self.init_frames()
        self.show_main_menu()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"600x600+{x}+{y}")

    def clear_frames(self):
        for frame in [self.main_menu_frame, self.login_frame, self.create_account_frame,
                      self.banking_menu_frame, self.transaction_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
            frame.grid_forget()

        for widget in self.main_frame.winfo_children():
            if widget not in [self.main_menu_frame, self.login_frame, self.create_account_frame,
                               self.banking_menu_frame, self.transaction_frame]:
                widget.destroy()

    def init_frames(self):
        self.main_menu_frame = ttk.Frame(self.main_frame)
        self.login_frame = ttk.Frame(self.main_frame)
        self.create_account_frame = ttk.Frame(self.main_frame)
        self.banking_menu_frame = ttk.Frame(self.main_frame)
        self.transaction_frame = ttk.Frame(self.main_frame)

        for frame in [self.main_menu_frame, self.login_frame, self.create_account_frame,
                      self.banking_menu_frame, self.transaction_frame]:
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_remove()

    def generate_receipt_image(self, transaction_type, account, amount=None, recipient=None):
        img_width = 500
        img_height = 400
        image = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 16)  # Use a valid font path if needed
            title_font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        y_position = 20
        draw.text((img_width // 2, y_position), "TRANSACTION RECEIPT", font=title_font, fill='black', anchor='mm')
        y_position += 40
        draw.line([(40, y_position), (img_width - 40, y_position)], fill='black', width=2)
        y_position += 30
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        receipt_content = [
            f"Date: {timestamp}",
            f"Transaction Type: {transaction_type}",
            f"Account Number: {account['account_number']}",
            f"Account Holder: {account['name']}"
        ]

        if amount is not None:
            receipt_content.append(f"Amount: ₱{amount:.2f}")

        if recipient:
            receipt_content.extend([
                f"Recipient Account: {recipient['account_number']}",
                f"Recipient Name: {recipient['name']}"
            ])

        receipt_content.append(f"Current Balance: ₱{account['balance']:.2f}")

        for line in receipt_content:
            draw.text((50, y_position), line, font=font, fill='black')
            y_position += 30

        y_position += 10
        draw.line([(40, y_position), (img_width - 40, y_position)], fill='black', width=2)
        y_position += 30
        draw.text((img_width // 2, y_position), "Thank you for banking with us!", font=font, fill='black', anchor='mm')

        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"./receipts/{account['account_number']}_{transaction_type}_{timestamp_str}.png"
        os.makedirs('./receipts', exist_ok=True) # Create directory if it doesn't exist
        image.save(filename)
        return filename

    def show_main_menu(self):
        self.clear_frames()
        ttk.Label(self.main_menu_frame, text="ATM Banking System", font=('Segoe UI Variable Text Semibold', 16, 'bold')).grid(row=0, column=0, pady=20)
        ttk.Button(self.main_menu_frame, text="Create Account", command=self.show_create_account).grid(row=1, column=0, pady=self.button_pady)
        ttk.Button(self.main_menu_frame, text="Login", command=self.show_login).grid(row=2, column=0, pady=self.button_pady)
        ttk.Button(self.main_menu_frame, text="Exit", command=self.root.quit).grid(row=3, column=0, pady=self.button_pady)
        self.main_menu_frame.grid(row=0, column=0)

    def show_create_account(self):
        self.clear_frames()
        ttk.Label(self.create_account_frame, text="Create New Account", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=self.button_pady)
        ttk.Label(self.create_account_frame, text="Full Name: ").grid(row=1, column=0, pady=5)
        name_entry = ttk.Entry(self.create_account_frame)
        name_entry.grid(row=1, column=1, pady=5)
        ttk.Label(self.create_account_frame, text="PIN (4 digits): ").grid(row=2, column=0, pady=5)
        pin_entry = ttk.Entry(self.create_account_frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5)
        ttk.Label(self.create_account_frame, text="Initial Deposit (₱): ").grid(row=3, column=0, pady=5)
        deposit_entry = ttk.Entry(self.create_account_frame)
        deposit_entry.grid(row=3, column=1, pady=5)

        def create():
            name = name_entry.get()
            pin = pin_entry.get()

            if not name or any(char.isdigit() for char in name):
                messagebox.showerror("Error", "Invalid name")
                return
                    
            try:
                initial_deposit = float(deposit_entry.get())
                if len(pin) != 4 or not pin.isdigit():
                    messagebox.showerror("Error", "PIN must be 4 digits")
                    return
                if initial_deposit <= 0:
                    messagebox.showerror("Error", "Initial deposit must be positive")
                    return

                account = {
                    'account_number': generate_account_number(),
                    'name': name,
                    'pin': pin,
                    'balance': initial_deposit,
                    'transaction_history': []
                }
                accounts.append(account)
                messagebox.showinfo("Success", f"Account created successfully!\nYour account number is: {account['account_number']}")
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid deposit amount")

        ttk.Button(self.create_account_frame, text="Create Account", command=create).grid(row=4, column=0, columnspan=2, pady=self.button_pady)
        ttk.Button(self.create_account_frame, text="Back", command=self.show_main_menu).grid(row=5, column=0, columnspan=2, pady=self.button_pady)
        self.create_account_frame.grid(row=0, column=0)

    def show_login(self):
        self.clear_frames()
        ttk.Label(self.login_frame, text="Login", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.login_frame, text="Account Number:").grid(row=1, column=0, pady=5)
        acc_entry = ttk.Entry(self.login_frame)
        acc_entry.grid(row=1, column=1, pady=5)
        ttk.Label(self.login_frame, text="PIN:").grid(row=2, column=0, pady=5)
        pin_entry = ttk.Entry(self.login_frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5)

        def login():
            global current_account_index
            acc_num = acc_entry.get()
            pin = pin_entry.get()

            for i, account in enumerate(accounts):
                if account['account_number'] == acc_num and account['pin'] == pin:
                    current_account_index = i
                    self.show_banking_menu()
                    return
            messagebox.showerror("Error", "Invalid account number or PIN")

        ttk.Button(self.login_frame, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=self.button_pady)
        ttk.Button(self.login_frame, text="Back", command=self.show_main_menu).grid(row=4, column=0, columnspan=2)
        self.login_frame.grid(row=0, column=0)

    def show_banking_menu(self):
        self.clear_frames()
        account = accounts[current_account_index]
        ttk.Label(self.banking_menu_frame, text=f"Welcome, {account['name']}", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.banking_menu_frame, text=f"Balance: ₱{account['balance']:.2f}", font=('Segoe UI Variable Text Semibold', 12)).grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Deposit", command=lambda: self.show_transaction('deposit')).grid(row=2, column=0, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Withdraw", command=lambda: self.show_transaction('withdraw')).grid(row=2, column=1, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Transfer", command=lambda: self.show_transaction('transfer')).grid(row=3, column=0, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Transaction History", command=self.show_history).grid(row=3, column=1, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Change PIN", command=self.show_change_pin).grid(row=4, column=0, pady=5, padx=5)
        ttk.Button(self.banking_menu_frame, text="Logout", command=self.logout).grid(row=4, column=1, pady=5, padx=5)
        self.banking_menu_frame.grid(row=0, column=0)

    def show_change_pin(self):
        self.clear_frames()
        ttk.Label(self.transaction_frame, text="Change PIN", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.transaction_frame, text="Current PIN:").grid(row=1, column=0, pady=5)
        current_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        current_pin_entry.grid(row=1, column=1, pady=5)
        ttk.Label(self.transaction_frame, text="New PIN (4 digits):").grid(row=2, column=0, pady=5)
        new_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        new_pin_entry.grid(row=2, column=1, pady=5)
        ttk.Label(self.transaction_frame, text="Confirm New PIN:").grid(row=3, column=0, pady=5)
        confirm_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        confirm_pin_entry.grid(row=3, column=1, pady=5)

        def change_pin():
            current_pin = current_pin_entry.get()
            new_pin = new_pin_entry.get()
            confirm_pin = confirm_pin_entry.get()

            account = accounts[current_account_index]

            if current_pin != account['pin']:
                messagebox.showerror("Error", "Incorrect current PIN.")
                return
            if new_pin != confirm_pin:
                messagebox.showerror("Error", "New PIN and confirmation do not match.")
                return
            if len(new_pin) != 4 or not new_pin.isdigit():
                messagebox.showerror("Error", "New PIN must be 4 digits.")
                return

            account['pin'] = new_pin
            add_transaction(current_account_index, "PIN CHANGE", 0)
            receipt_path = self.generate_receipt_image("PIN CHANGE", account)
            messagebox.showinfo("Success", f"PIN changed successfully.\nReceipt saved as: {receipt_path}")
            self.show_banking_menu()

        ttk.Button(self.transaction_frame, text="Change PIN", command=change_pin).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(self.transaction_frame, text="Back", command=self.show_banking_menu).grid(row=5, column=0, columnspan=2)
        self.transaction_frame.grid(row=0, column=0)

    def show_transaction(self, trans_type):
        self.clear_frames()
        ttk.Label(self.transaction_frame, text=f"{trans_type.title()}", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)

        if trans_type == 'transfer':
            ttk.Label(self.transaction_frame, text="Recipient Account:").grid(row=1, column=0, pady=5)
            recipient_entry = ttk.Entry(self.transaction_frame)
            recipient_entry.grid(row=1, column=1, pady=5)

        ttk.Label(self.transaction_frame, text="Amount:").grid(row=2, column=0, pady=5)
        amount_entry = ttk.Entry(self.transaction_frame)
        amount_entry.grid(row=2, column=1, pady=5)

        def process_transaction():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return

                if trans_type == 'deposit':
                    self.deposit(amount)
                elif trans_type == 'withdraw':
                    self.withdraw(amount)
                elif trans_type == 'transfer':
                    recipient_acc = recipient_entry.get()
                    self.transfer(amount, recipient_acc)

                self.show_banking_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount")

        ttk.Button(self.transaction_frame, text="Submit", command=process_transaction).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self.transaction_frame, text="Back", command=self.show_banking_menu).grid(row=4, column=0, columnspan=2)
        self.transaction_frame.grid(row=0, column=0)

    def show_history(self):
        self.clear_frames()
        ttk.Label(self.transaction_frame, text="Transaction History", font=('Segoe UI Variable Text Semibold', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)

        text_widget = tk.Text(self.transaction_frame, height=15, width=50)
        text_widget.grid(row=1, column=0, columnspan=2, pady=10)

        scrollbar = ttk.Scrollbar(self.transaction_frame, orient='vertical', command=text_widget.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        text_widget['yscrollcommand'] = scrollbar.set

        for trans in accounts[current_account_index]['transaction_history']:
            text_widget.insert('end', f"\nType: {trans['type']}\n")
            text_widget.insert('end', f"Amount: ₱{trans['amount']:.2f}\n")
            text_widget.insert('end', f"Date: {trans['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            text_widget.insert('end', f"Balance After: ₱{trans['balance_after']:.2f}\n")
            if trans['recipient']:
                text_widget.insert('end', f"Recipient: {trans['recipient']}\n")
            text_widget.insert('end', "-" * 40 + "\n")

        text_widget.config(state='disabled')

        ttk.Button(self.transaction_frame, text="Back", command=self.show_banking_menu).grid(row=2, column=0, columnspan=2, pady=10)
        self.transaction_frame.grid(row=0, column=0)

    def deposit(self, amount):
        accounts[current_account_index]['balance'] += amount
        add_transaction(current_account_index, "DEPOSIT", amount)
        receipt_path = self.generate_receipt_image("DEPOSIT", accounts[current_account_index], amount)
        messagebox.showinfo("Success", f"Deposit successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}\nReceipt saved as: {receipt_path}")

    def withdraw(self, amount):
        if amount > accounts[current_account_index]['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return False

        accounts[current_account_index]['balance'] -= amount
        add_transaction(current_account_index, "WITHDRAWAL", amount)
        receipt_path = self.generate_receipt_image("WITHDRAWAL", accounts[current_account_index], amount)
        messagebox.showinfo("Success", f"Withdrawal successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}\nReceipt saved as: {receipt_path}")
        return True

    def transfer(self, amount, recipient_acc):
        recipient_index = None
        for i, account in enumerate(accounts):
            if account['account_number'] == recipient_acc:
                recipient_index = i
                break

        if recipient_index is None:
            messagebox.showerror("Error", "Recipient account not found")
            return

        if recipient_index == current_account_index:
            messagebox.showerror("Error", "Cannot transfer to your own account")
            return

        if amount > accounts[current_account_index]['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return

        accounts[current_account_index]['balance'] -= amount
        accounts[recipient_index]['balance'] += amount

        add_transaction(current_account_index, "TRANSFER (SENT)", amount, recipient_acc)
        add_transaction(recipient_index, "TRANSFER (RECEIVED)", amount, accounts[current_account_index]['account_number'])

        receipt_path = self.generate_receipt_image("TRANSFER", accounts[current_account_index], amount, accounts[recipient_index])
        messagebox.showinfo("Success", f"Transfer successful.\nReceipt saved as: {receipt_path}")

    def logout(self):
        self.clear_frames()
        global current_account_index
        current_account_index = None
        self.show_main_menu()

# --- Main Program (Interface Selection) ---
HEADER_STYLE = Style(color="blue", bold=True)
SUCCESS_STYLE = Style(color="green", bold=True)
ERROR_STYLE = Style(color="red", bold=True)
console = Console()

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
    time.sleep(1.5)

def choose_interface():
    clear_screen()
    display_header("ATM Banking System - Interface Selection")
    
    options = {
        "1": "TUI Interface (Rich text interface)",
        "2": "GUI Interface (Graphical interface)",
        "3": "Exit"
    }
    
    for key, value in options.items():
        console.print(f"[cyan][{key}][/cyan] {value}")
    
    choice = Prompt.ask("\n[blue]Choose your interface", choices=list(options.keys()))
    return choice

def main_program():
    # root = tk.Tk()
    # app = ATMGui(root)
    # root.mainloop()
    while True:
        choice = choose_interface()

        if choice == "1":
            clear_screen()
            display_message("Starting TUI Interface...", "success")
            time.sleep(1)
            run_tui()
        elif choice == "2":
            clear_screen()
            display_message("Starting GUI Interface...", "success")
            time.sleep(1)
            print("running")
            root = tk.Tk()
            app = ATMGui(root)
            root.mainloop()
        elif choice == "3":
            clear_screen()
            display_message("Thank you for using the ATM Banking System!", "success")
            time.sleep(1)
            sys.exit(0)
        

if __name__ == "__main__":
    main_program()
import random
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

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

class ATMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Banking System")
        self.root.geometry("600x600")
        self.root.configure(bg="#f7f7f7")
        self.center_window()

        self.BG_COLOR = "#f7f7f7"
        self.PRIMARY = "#EFB6C8"

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", \
                             background="#EFB6C8", \
                             foreground="black", \
                             borderwidth=1, \
                             focuscolor="#e090a9", \
                             relief="flat")
        self.style.map("TButton", background=[('active', '#e87b9d')])

        self.main_frame = tk.Frame(root, bg=self.BG_COLOR, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

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

    def init_frames(self):
        self.main_menu_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.login_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.create_account_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.banking_menu_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)
        self.transaction_frame = tk.Frame(self.main_frame, bg=self.BG_COLOR)

    def show_main_menu(self):
        self.clear_frames()
        tk.Label(self.main_menu_frame, text="ATM Banking System", bg=self.BG_COLOR, fg="#000000",
                 font=("Franklin Gothic Heavy", 16, "bold")).pack(pady=20)
        ttk.Button(self.main_menu_frame, text="Create Account", command=self.show_create_account).pack(pady=10)
        ttk.Button(self.main_menu_frame, text="Login", command=self.show_login).pack(pady=10)
        ttk.Button(self.main_menu_frame, text="Exit", command=self.root.quit).pack(pady=10)
        self.main_menu_frame.grid(row=0, column=0, sticky="nsew")

    def show_create_account(self):
        self.clear_frames()
        tk.Label(self.create_account_frame, text="Create New Account", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.create_account_frame, text="Full Name:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        name_entry = ttk.Entry(self.create_account_frame)
        name_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(self.create_account_frame, text="PIN (4 digits):", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        pin_entry = ttk.Entry(self.create_account_frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5, padx=5)
        tk.Label(self.create_account_frame, text="Initial Deposit (₱):", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        deposit_entry = ttk.Entry(self.create_account_frame)
        deposit_entry.grid(row=3, column=1, pady=5, padx=5)

        def create():
            name = name_entry.get()
            pin = pin_entry.get()
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

        ttk.Button(self.create_account_frame, text="Create Account", command=create).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(self.create_account_frame, text="Back", command=self.show_main_menu).grid(row=5, column=0, columnspan=2)
        self.create_account_frame.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.clear_frames()
        tk.Label(self.login_frame, text="Login", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.login_frame, text="Account Number:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        acc_entry = ttk.Entry(self.login_frame)
        acc_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(self.login_frame, text="PIN:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        pin_entry = ttk.Entry(self.login_frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5, padx=5)

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

        ttk.Button(self.login_frame, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self.login_frame, text="Back", command=self.show_main_menu).grid(row=4, column=0, columnspan=2)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def show_banking_menu(self):
        self.clear_frames()
        account = accounts[current_account_index]
        tk.Label(self.banking_menu_frame, text=f"Welcome, {account['name']}", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.banking_menu_frame, text=f"Balance: ₱{account['balance']:.2f}", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 12)).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.banking_menu_frame, text="Deposit", command=lambda: self.show_transaction('deposit')).grid(row=2, column=0, pady=10, padx=5)
        ttk.Button(self.banking_menu_frame, text="Withdraw", command=lambda: self.show_transaction('withdraw')).grid(row=2, column=1, pady=10, padx=5)
        ttk.Button(self.banking_menu_frame, text="Transfer", command=lambda: self.show_transaction('transfer')).grid(row=3, column=0, pady=10, padx=5)
        ttk.Button(self.banking_menu_frame, text="Transaction History", command=self.show_history).grid(row=3, column=1, pady=10, padx=5)
        ttk.Button(self.banking_menu_frame, text="Change PIN", command=self.show_change_pin).grid(row=4, column=0, pady=10, padx=5)
        ttk.Button(self.banking_menu_frame, text="Logout", command=self.logout).grid(row=4, column=1, pady=10, padx=5)
        self.banking_menu_frame.grid(row=0, column=0, sticky="nsew")

    def show_transaction(self, trans_type):
        self.clear_frames()
        tk.Label(self.transaction_frame, text=f"{trans_type.title()}", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        if trans_type == 'transfer':
            tk.Label(self.transaction_frame, text="Recipient Account:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=1, column=0, pady=5, padx=5, sticky="w")
            recipient_entry = ttk.Entry(self.transaction_frame)
            recipient_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.transaction_frame, text="Amount:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        amount_entry = ttk.Entry(self.transaction_frame)
        amount_entry.grid(row=2, column=1, pady=5, padx=5)

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
        self.transaction_frame.grid(row=0, column=0, sticky="nsew")

    def deposit(self, amount):
        accounts[current_account_index]['balance'] += amount
        add_transaction(current_account_index, "DEPOSIT", amount)
        messagebox.showinfo("Success", f"Deposit successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}")

    def withdraw(self, amount):
        if amount > accounts[current_account_index]['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return False

        accounts[current_account_index]['balance'] -= amount
        add_transaction(current_account_index, "WITHDRAWAL", amount)
        messagebox.showinfo("Success", f"Withdrawal successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}")
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

        messagebox.showinfo("Success", "Transfer successful.")

    def show_history(self):
        self.clear_frames()
        tk.Label(self.transaction_frame, text="Transaction History", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        history_text = tk.Text(self.transaction_frame, height=15, width=50, bg="#A5BFCC", fg=self.BG_COLOR)
        history_text.grid(row=1, column=0, columnspan=2, pady=10)

        scrollbar = ttk.Scrollbar(self.transaction_frame, orient="vertical", command=history_text.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        history_text["yscrollcommand"] = scrollbar.set

        for trans in accounts[current_account_index]['transaction_history']:
            history_text.insert('end', f"\nType: {trans['type']}\n")
            history_text.insert('end', f"Amount: ₱{trans['amount']:.2f}\n")
            history_text.insert('end', f"Date: {trans['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            history_text.insert('end', f"Balance After: ₱{trans['balance_after']:.2f}\n")
            if trans['recipient']:
                history_text.insert('end', f"Recipient: {trans['recipient']}\n")
            history_text.insert('end', "-" * 40 + "\n")

        history_text.config(state='disabled')

        ttk.Button(self.transaction_frame, text="Back", command=self.show_banking_menu).grid(row=2, column=0, columnspan=2, pady=10)
        self.transaction_frame.grid(row=0, column=0, sticky="nsew")

    def show_change_pin(self):
        self.clear_frames()
        tk.Label(self.transaction_frame, text="Change PIN", bg=self.BG_COLOR, fg="#F4EDD3",
                 font=("Franklin Gothic Heavy", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self.transaction_frame, text="Current PIN:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        current_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        current_pin_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(self.transaction_frame, text="New PIN (4 digits):", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        new_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        new_pin_entry.grid(row=2, column=1, pady=5, padx=5)
        tk.Label(self.transaction_frame, text="Confirm New PIN:", bg=self.BG_COLOR, fg="#F4EDD3").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        confirm_pin_entry = ttk.Entry(self.transaction_frame, show="*")
        confirm_pin_entry.grid(row=3, column=1, pady=5, padx=5)

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
            messagebox.showinfo("Success", "PIN changed successfully.")
            self.show_banking_menu()

        ttk.Button(self.transaction_frame, text="Change PIN", command=change_pin).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(self.transaction_frame, text="Back", command=self.show_banking_menu).grid(row=5, column=0, columnspan=2)
        self.transaction_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.clear_frames()
        global current_account_index
        current_account_index = None
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMGui(root)
    root.mainloop()
       

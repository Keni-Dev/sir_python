import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random

# Global lists to store data
accounts = []
current_account_index = None

class ATMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Banking System")
        self.root.geometry("400x400")
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize all frames but only show login frame
        self.init_frames()
        self.show_main_menu()

    def init_frames(self):
        # Create all frames
        self.main_menu_frame = ttk.Frame(self.main_frame)
        self.login_frame = ttk.Frame(self.main_frame)
        self.create_account_frame = ttk.Frame(self.main_frame)
        self.banking_menu_frame = ttk.Frame(self.main_frame)
        self.transaction_frame = ttk.Frame(self.main_frame)

    def clear_frames(self):
        for widget in self.main_frame.winfo_children():
            widget.grid_forget()

    def show_main_menu(self):
        self.clear_frames()
        
        # Title
        ttk.Label(self.main_menu_frame, text="ATM Banking System", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, pady=20)
        
        # Buttons
        ttk.Button(self.main_menu_frame, text="Create Account", command=self.show_create_account).grid(row=1, column=0, pady=10)
        ttk.Button(self.main_menu_frame, text="Login", command=self.show_login).grid(row=2, column=0, pady=10)
        ttk.Button(self.main_menu_frame, text="Exit", command=self.root.quit).grid(row=3, column=0, pady=10)
        
        self.main_menu_frame.grid(row=0, column=0)

    def show_create_account(self):
        self.clear_frames()
        
        ttk.Label(self.create_account_frame, text="Create New Account", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(self.create_account_frame, text="Full Name:").grid(row=1, column=0, pady=5)
        name_entry = ttk.Entry(self.create_account_frame)
        name_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.create_account_frame, text="PIN (4 digits):").grid(row=2, column=0, pady=5)
        pin_entry = ttk.Entry(self.create_account_frame, show="*")
        pin_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.create_account_frame, text="Initial Deposit (₱):").grid(row=3, column=0, pady=5)
        deposit_entry = ttk.Entry(self.create_account_frame)
        deposit_entry.grid(row=3, column=1, pady=5)
        
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
                    'account_number': self.generate_account_number(),
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
        
        self.create_account_frame.grid(row=0, column=0)

    def show_login(self):
        self.clear_frames()
        
        ttk.Label(self.login_frame, text="Login", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
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

        ttk.Button(self.login_frame, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self.login_frame, text="Back", command=self.show_main_menu).grid(row=4, column=0, columnspan=2)
        
        self.login_frame.grid(row=0, column=0)

    def show_banking_menu(self):
        self.clear_frames()
        
        account = accounts[current_account_index]
        ttk.Label(self.banking_menu_frame, text=f"Welcome, {account['name']}", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.banking_menu_frame, text=f"Balance: ₱{account['balance']:.2f}", font=('Helvetica', 12)).grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.banking_menu_frame, text="Deposit", command=lambda: self.show_transaction('deposit')).grid(row=2, column=0, pady=10)
        ttk.Button(self.banking_menu_frame, text="Withdraw", command=lambda: self.show_transaction('withdraw')).grid(row=2, column=1, pady=10)
        ttk.Button(self.banking_menu_frame, text="Transfer", command=lambda: self.show_transaction('transfer')).grid(row=3, column=0, pady=10)
        ttk.Button(self.banking_menu_frame, text="Transaction History", command=self.show_history).grid(row=3, column=1, pady=10)
        ttk.Button(self.banking_menu_frame, text="Logout", command=self.logout).grid(row=4, column=0, columnspan=2, pady=20)
        
        self.banking_menu_frame.grid(row=0, column=0)

    def show_transaction(self, trans_type):
        self.clear_frames()
        
        ttk.Label(self.transaction_frame, text=f"{trans_type.title()}", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
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
        
        ttk.Label(self.transaction_frame, text="Transaction History", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Create text widget
        text_widget = tk.Text(self.transaction_frame, height=15, width=50)
        text_widget.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.transaction_frame, orient='vertical', command=text_widget.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        text_widget['yscrollcommand'] = scrollbar.set
        
        # Display transactions
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

    def generate_account_number(self):
        while True:
            acc_num = str(random.randint(1, 99))
            if not any(account['account_number'] == acc_num for account in accounts):
                return acc_num

    def add_transaction(self, transaction_type, amount, recipient=None):
        accounts[current_account_index]['transaction_history'].append({
            'type': transaction_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'recipient': recipient,
            'balance_after': accounts[current_account_index]['balance']
        })

    def deposit(self, amount):
        accounts[current_account_index]['balance'] += amount
        self.add_transaction("DEPOSIT", amount)
        messagebox.showinfo("Success", f"Deposit successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}")

    def withdraw(self, amount):
        if amount > accounts[current_account_index]['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return False
        
        accounts[current_account_index]['balance'] -= amount
        self.add_transaction("WITHDRAWAL", amount)
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
        
        if self.withdraw(amount):
            accounts[recipient_index]['balance'] += amount
            self.add_transaction("TRANSFER", amount, recipient_acc)
            messagebox.showinfo("Success", "Transfer successful")

    def logout(self):
        global current_account_index
        current_account_index = None
        self.show_main_menu()

def main():
    root = tk.Tk()
    app = ATMGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
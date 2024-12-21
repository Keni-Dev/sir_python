import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont
import os

# Global lists to store data
accounts = []
current_account_index = None

# Create receipts directory if it doesn't exist
if not os.path.exists('receipts'):
    os.makedirs('receipts')

class ATMGui:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Banking System")
        self.root.geometry("400x400")
        
        # Center the window
        self.center_window()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights to center content
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Initialize all frames but only show login frame
        self.init_frames()
        self.show_main_menu()

    def clear_frames(self):
        """Hide all frames by removing them from the grid"""
        for frame in [self.main_menu_frame, self.login_frame, 
                     self.create_account_frame, self.banking_menu_frame, 
                     self.transaction_frame]:
            frame.grid_remove()
    def center_window(self):
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width - 400) // 2
        y = (screen_height - 400) // 2
        
        # Set window position
        self.root.geometry(f"400x400+{x}+{y}")

    def init_frames(self):
        # Create all frames with center alignment
        self.main_menu_frame = ttk.Frame(self.main_frame)
        self.login_frame = ttk.Frame(self.main_frame)
        self.create_account_frame = ttk.Frame(self.main_frame)
        self.banking_menu_frame = ttk.Frame(self.main_frame)
        self.transaction_frame = ttk.Frame(self.main_frame)
        
        # Configure grid weights for all frames
        for frame in [self.main_menu_frame, self.login_frame, self.create_account_frame, 
                     self.banking_menu_frame, self.transaction_frame]:
            frame.grid_columnconfigure(0, weight=1)

    def generate_receipt_image(self, transaction_type, account, amount=None, recipient=None):
        # Create image
        img_width = 500
        img_height = 400
        image = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to load a font, fall back to default if not available
            font = ImageFont.truetype("arial.ttf", 16)
            title_font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # Draw receipt content
        y_position = 20
        
        # Title
        draw.text((img_width//2, y_position), "TRANSACTION RECEIPT", font=title_font, fill='black', anchor='mm')
        y_position += 40
        
        # Border lines
        draw.line([(40, y_position), (img_width-40, y_position)], fill='black', width=2)
        
        # Content
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
        
        # Draw each line of content
        for line in receipt_content:
            draw.text((50, y_position), line, font=font, fill='black')
            y_position += 30
        
        # Bottom border
        y_position += 10
        draw.line([(40, y_position), (img_width-40, y_position)], fill='black', width=2)
        
        # Thank you message
        y_position += 30
        draw.text((img_width//2, y_position), "Thank you for banking with us!", font=font, fill='black', anchor='mm')
        
        # Save receipt
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"receipts/{account['account_number']}_{transaction_type}_{timestamp_str}.png"
        image.save(filename)
        return filename

    def show_main_menu(self):
        self.clear_frames()
        
        # Center the main menu frame
        self.main_menu_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        ttk.Label(self.main_menu_frame, text="ATM Banking System", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, pady=20)
        
        # Buttons
        for i, (text, command) in enumerate([
            ("Create Account", self.show_create_account),
            ("Login", self.show_login),
            ("Exit", self.root.quit)
        ], 1):
            ttk.Button(self.main_menu_frame, text=text, command=command).grid(
                row=i, column=0, pady=10, padx=50)

    # ... [Previous methods remain the same until deposit/withdraw/transfer] ...

    def deposit(self, amount):
        accounts[current_account_index]['balance'] += amount
        self.add_transaction("DEPOSIT", amount)
        receipt_path = self.generate_receipt_image("DEPOSIT", accounts[current_account_index], amount)
        messagebox.showinfo("Success", f"Deposit successful.\nNew balance: ₱{accounts[current_account_index]['balance']:.2f}\nReceipt saved as: {receipt_path}")

    def withdraw(self, amount):
        if amount > accounts[current_account_index]['balance']:
            messagebox.showerror("Error", "Insufficient funds")
            return False
        
        accounts[current_account_index]['balance'] -= amount
        self.add_transaction("WITHDRAWAL", amount)
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
        
        if self.withdraw(amount):
            accounts[recipient_index]['balance'] += amount
            self.add_transaction("TRANSFER", amount, recipient_acc)
            receipt_path = self.generate_receipt_image("TRANSFER", accounts[current_account_index], 
                                                     amount, accounts[recipient_index])
            messagebox.showinfo("Success", f"Transfer successful.\nReceipt saved as: {receipt_path}")
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

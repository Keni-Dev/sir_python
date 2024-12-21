import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
from PIL import Image, ImageDraw, ImageFont
import os

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
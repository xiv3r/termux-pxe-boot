#!/usr/bin/env python3
"""
Termux PXE Boot GUI - Arch Linux with Kali UI
Main application entry point
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import socket
import subprocess
import os
import sys
import json
from datetime import datetime
import webbrowser

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.main_window import MainWindow
    from pxe.server import PXEServer
    from config.settings import Settings
    from utils.logger import Logger
    from utils.network import NetworkManager
    from arch.customizer import ArchCustomizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all required files are present in the correct directories.")
    sys.exit(1)

class TermuxPXEBootApp:
    def __init__(self):
        self.root = tk.Tk()
        self.settings = Settings()
        self.logger = Logger()
        self.network_manager = NetworkManager()
        self.pxe_server = None
        self.arch_customizer = ArchCustomizer()
        
        # Application state
        self.is_server_running = False
        self.boot_files_ready = False
        
        self.setup_gui()
        self.check_termux_environment()
        
    def setup_gui(self):
        """Initialize the main GUI window"""
        self.main_window = MainWindow(
            root=self.root,
            app=self,
            settings=self.settings,
            logger=self.logger,
            network_manager=self.network_manager,
            pxe_server=self.pxe_server,
            arch_customizer=self.arch_customizer
        )
        
    def check_termux_environment(self):
        """Check if running in Termux environment"""
        try:
            if not os.path.exists('/data/data/com.termux/files/home'):
                messagebox.showwarning(
                    "Termux Environment",
                    "This application is designed for Termux on Android.\n"
                    "Some features may not work in other environments."
                )
        except Exception as e:
            self.logger.error(f"Environment check failed: {e}")
            
    def start_pxe_server(self):
        """Start the PXE server in a separate thread"""
        if self.is_server_running:
            return
            
        def server_thread():
            try:
                self.pxe_server = PXEServer(
                    settings=self.settings,
                    logger=self.logger,
                    network_manager=self.network_manager
                )
                
                # Prepare boot files
                self.main_window.update_status("Preparing boot files...")
                if not self.pxe_server.prepare_boot_files():
                    self.main_window.update_status("Failed to prepare boot files")
                    return
                    
                self.main_window.update_status("Starting PXE server...")
                self.pxe_server.start()
                self.is_server_running = True
                
                self.main_window.update_status("PXE Server is running!")
                self.main_window.update_server_status(True)
                
            except Exception as e:
                self.logger.error(f"Failed to start PXE server: {e}")
                self.main_window.update_status(f"Error: {e}")
                self.main_window.update_server_status(False)
                
        threading.Thread(target=server_thread, daemon=True).start()
        
    def stop_pxe_server(self):
        """Stop the PXE server"""
        if self.pxe_server and self.is_server_running:
            try:
                self.pxe_server.stop()
                self.is_server_running = False
                self.main_window.update_status("PXE Server stopped")
                self.main_window.update_server_status(False)
            except Exception as e:
                self.logger.error(f"Failed to stop PXE server: {e}")
                
    def run(self):
        """Start the application"""
        self.root.title("Termux PXE Boot - Arch Linux Kali Edition")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set application icon and style
        self.setup_styles()
        
        # Center window on screen
        self.center_window()
        
        # Start the GUI
        self.root.mainloop()
        
    def setup_styles(self):
        """Setup custom styles for Kali-like appearance"""
        style = ttk.Style()
        
        # Configure dark theme
        style.theme_use('clam')
        
        # Custom colors for Kali-like appearance
        style.configure('Kali.TFrame', background='#1a1a1a', relief='flat')
        style.configure('Kali.TLabel', background='#1a1a1a', foreground='#00ff00', font=('Monospace', 10))
        style.configure('Kali.TButton', background='#2d2d2d', foreground='#00ff00', 
                       font=('Monospace', 10, 'bold'), relief='flat', borderwidth=1)
        style.configure('Kali.TEntry', fieldbackground='#2d2d2d', foreground='#00ff00', 
                       font=('Monospace', 10), borderwidth=1)
        style.configure('Kali.Horizontal.TProgressbar', background='#00ff00')
        
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def main():
    """Main application entry point"""
    try:
        app = TermuxPXEBootApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")

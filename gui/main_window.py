"""
Main GUI Window for Termux PXE Boot
Cross-platform compatible GUI with modern interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pxe.server import PXEServer
    from config.settings import Settings
    from utils.logger import Logger
    from utils.network import NetworkManager
    from arch.customizer import ArchCustomizer
    from optimizations.performance import PerformanceOptimizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are properly installed.")

class MainWindow:
    def __init__(self, root, app, settings=None, logger=None, network_manager=None, pxe_server=None, arch_customizer=None, performance_optimizer=None):
        self.root = root
        self.app = app
        self.settings = settings or Settings()
        self.logger = logger or Logger()
        self.network_manager = network_manager or NetworkManager()
        self.pxe_server = pxe_server
        self.arch_customizer = arch_customizer or ArchCustomizer(self.settings, self.logger)
        self.performance_optimizer = performance_optimizer or PerformanceOptimizer(self.settings, self.logger)
        
        # Server state
        self.is_server_running = False
        self.server_status = "STOPPED"
        
        # Performance monitoring
        self.monitoring_active = False
        self.performance_data = {}
        
        # Create GUI
        self.setup_styles()
        self.create_interface()
        self.center_window()
        
        # Start background tasks
        self.update_network_info()
        
    def setup_styles(self):
        """Setup modern, Kali-inspired styling"""
        style = ttk.Style()
        
        # Try to use modern theme
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
            
        # Configure custom styles for dark theme
        self.colors = {
            'bg': '#0a0a0a',
            'fg': '#00ff00',
            'secondary': '#1a1a1a',
            'accent': '#00aa00',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'success': '#00ff88'
        }
        
        # Override styles
        style.configure('Dark.TFrame', background=self.colors['bg'], relief='flat', borderwidth=0)
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'], 
                       font=('JetBrains Mono', 10))
        style.configure('Dark.TButton', background=self.colors['secondary'], 
                       foreground=self.colors['fg'], font=('JetBrains Mono', 10, 'bold'),
                       relief='flat', borderwidth=1)
        style.configure('Dark.TButton:active', background=self.colors['accent'])
        style.configure('Dark.TEntry', fieldbackground=self.colors['secondary'], 
                       foreground=self.colors['fg'], font=('JetBrains Mono', 10))
        style.configure('Dark.Horizontal.TProgressbar', background=self.colors['accent'])
        style.configure('Dark.TNotebook', background=self.colors['bg'])
        style.configure('Dark.TNotebook.Tab', background=self.colors['secondary'], 
                       foreground=self.colors['fg'], padding=[10, 5])
        
    def create_interface(self):
        """Create the main interface"""
        # Main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        self.create_title_section(main_container)
        
        # Tab control for different sections
        self.create_notebook(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_title_section(self, parent):
        """Create the title section"""
        title_frame = ttk.Frame(parent, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Main title
        title_label = ttk.Label(
            title_frame,
            text="⚡ TERMUX PXE BOOT - STEROID EDITION ⚡",
            style='Dark.TLabel',
            font=('JetBrains Mono', 20, 'bold')
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            title_frame,
            text="Cross-Platform Network Boot Server - Performance Optimized",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12)
        )
        subtitle_label.pack()
        
        # Version and platform info
        info_text = f"v3.0.0 - Steroid Edition | Platform: {self.detect_platform()} | Python: {sys.version.split()[0]}"
        info_label = ttk.Label(
            title_frame,
            text=info_text,
            style='Dark.TLabel',
            font=('JetBrains Mono', 9)
        )
        info_label.pack()
        
    def detect_platform(self):
        """Detect the current platform"""
        import platform
        system = platform.system()
        if system == "Linux":
            if os.path.exists("/data/data/com.termux/files/home"):
                return "Termux (Android)"
            else:
                return "Linux"
        elif system == "Darwin":
            return "macOS"
        elif system == "Windows":
            return "Windows"
        else:
            return system
            
    def create_notebook(self, parent):
        """Create notebook with tabs for different functions"""
        self.notebook = ttk.Notebook(parent, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Server Control Tab
        self.server_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.server_frame, text="🚀 Server Control")
        self.create_server_tab()
        
        # Network Config Tab
        self.network_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.network_frame, text="🌐 Network Config")
        self.create_network_tab()
        
        # Performance Tab
        self.performance_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.performance_frame, text="⚡ Performance")
        self.create_performance_tab()
        
        # Arch Customization Tab
        self.arch_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.arch_frame, text="🎨 Arch Customization")
        self.create_arch_tab()
        
        # Monitoring Tab
        self.monitor_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.monitor_frame, text="📊 Monitoring")
        self.create_monitoring_tab()
        
    def create_server_tab(self):
        """Create server control tab"""
        # Server control section
        control_frame = ttk.LabelFrame(self.server_frame, text="Server Control", style='Dark.TFrame')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start/Stop buttons
        buttons_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = ttk.Button(
            buttons_frame,
            text="▶️ START PXE SERVER",
            command=self.start_server,
            style='Dark.TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            buttons_frame,
            text="⏹️ STOP SERVER",
            command=self.stop_server,
            style='Dark.TButton',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="🖥️ Boot Instructions",
            command=self.show_boot_instructions,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
        # Status display
        status_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(status_frame, text="Status:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.status_label = ttk.Label(
            status_frame,
            text="● STOPPED",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12, 'bold')
        )
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Server information
        info_frame = ttk.LabelFrame(self.server_frame, text="Server Information", style='Dark.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrolled text for server info
        self.server_info = tk.Text(
            info_frame,
            height=10,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['accent'],
            wrap=tk.WORD
        )
        
        # Scrollbar for server info
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.server_info.yview)
        self.server_info.configure(yscrollcommand=info_scrollbar.set)
        
        self.server_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize server info
        self.update_server_info()
        
    def create_network_tab(self):
        """Create network configuration tab"""
        # Network interface selection
        interface_frame = ttk.LabelFrame(self.network_frame, text="Network Interface", style='Dark.TFrame')
        interface_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Interface dropdown
        interface_select_frame = ttk.Frame(interface_frame, style='Dark.TFrame')
        interface_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(interface_select_frame, text="Interface:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(
            interface_select_frame,
            textvariable=self.interface_var,
            style='Dark.TEntry',
            state='readonly'
        )
        self.interface_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # IP Configuration
        ip_frame = ttk.LabelFrame(self.network_frame, text="IP Configuration", style='Dark.TFrame')
        ip_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Server IP
        server_ip_frame = ttk.Frame(ip_frame, style='Dark.TFrame')
        server_ip_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(server_ip_frame, text="Server IP:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.server_ip_var = tk.StringVar(value="192.168.1.100")
        ttk.Entry(server_ip_frame, textvariable=self.server_ip_var, style='Dark.TEntry', width=15).pack(side=tk.LEFT, padx=(10, 0))
        
        # DHCP Range
        dhcp_frame = ttk.Frame(ip_frame, style='Dark.TFrame')
        dhcp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dhcp_frame, text="DHCP Range:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.dhcp_start_var = tk.StringVar(value="192.168.1.50")
        self.dhcp_end_var = tk.StringVar(value="192.168.1.200")
        
        ttk.Entry(dhcp_frame, textvariable=self.dhcp_start_var, style='Dark.TEntry', width=12).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(dhcp_frame, text="to", style='Dark.TLabel').pack(side=tk.LEFT)
        ttk.Entry(dhcp_frame, textvariable=self.dhcp_end_var, style='Dark.TEntry', width=12).pack(side=tk.LEFT, padx=5)
        
        # Apply button
        ttk.Button(
            ip_frame,
            text="💾 Apply Network Config",
            command=self.apply_network_config,
            style='Dark.TButton'
        ).pack(pady=10)
        
    def create_performance_tab(self):
        """Create performance optimization tab"""
        # Performance profile selection
        profile_frame = ttk.LabelFrame(self.performance_frame, text="Performance Profile", style='Dark.TFrame')
        profile_frame.pack(fill=tk.X, padx=10, pady=10)
        
        profile_select_frame = ttk.Frame(profile_frame, style='Dark.TFrame')
        profile_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(profile_select_frame, text="Profile:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.performance_var = tk.StringVar(value="Maximum")
        profile_combo = ttk.Combobox(
            profile_select_frame,
            textvariable=self.performance_var,
            values=["Maximum", "Gaming", "Balanced", "Minimal"],
            style='Dark.TEntry',
            state='readonly'
        )
        profile_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Performance controls
        controls_frame = ttk.Frame(profile_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            controls_frame,
            text="⚡ Apply Performance",
            command=self.apply_performance,
            style='Dark.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="📊 Benchmark",
            command=self.run_benchmark,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
        # Performance description
        self.performance_desc = tk.Text(
            profile_frame,
            height=6,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.performance_desc.pack(fill=tk.X, padx=10, pady=10)
        
    def create_arch_tab(self):
        """Create Arch Linux customization tab"""
        # Theme selection
        theme_frame = ttk.LabelFrame(self.arch_frame, text="Theme & Customization", style='Dark.TFrame')
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        theme_select_frame = ttk.Frame(theme_frame, style='Dark.TFrame')
        theme_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(theme_select_frame, text="Theme:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value="Kali Dark")
        theme_combo = ttk.Combobox(
            theme_select_frame,
            textvariable=self.theme_var,
            values=["Kali Dark", "Cyberpunk", "Matrix", "Neon Green"],
            style='Dark.TEntry',
            state='readonly'
        )
        theme_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Tool selection
        tools_frame = ttk.LabelFrame(self.arch_frame, text="Tool Package", style='Dark.TFrame')
        tools_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tools_select_frame = ttk.Frame(tools_frame, style='Dark.TFrame')
        tools_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(tools_select_frame, text="Tools:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.tools_var = tk.StringVar(value="Kali Tools + Performance")
        tools_combo = ttk.Combobox(
            tools_select_frame,
            textvariable=self.tools_var,
            values=["Kali Tools + Performance", "Full Kali Suite", "Pentesting Essentials", "Custom Selection"],
            style='Dark.TEntry',
            state='readonly'
        )
        tools_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Customization controls
        controls_frame = ttk.Frame(theme_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            controls_frame,
            text="🎨 Apply Customization",
            command=self.apply_customization,
            style='Dark.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="📋 Preview Config",
            command=self.preview_config,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
    def create_monitoring_tab(self):
        """Create monitoring tab"""
        # System information
        info_frame = ttk.LabelFrame(self.monitor_frame, text="System Information", style='Dark.TFrame')
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # System info display
        self.system_info = tk.Text(
            info_frame,
            height=8,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.system_info.pack(fill=tk.X, padx=10, pady=10)
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(self.monitor_frame, text="Performance Metrics", style='Dark.TFrame')
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Metrics display
        self.metrics_display = tk.Text(
            metrics_frame,
            height=10,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.metrics_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_bar = ttk.Frame(parent, style='Dark.TFrame')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status text
        self.status_text = ttk.Label(
            self.status_bar,
            text="Ready",
            style='Dark.TLabel',
            font=('JetBrains Mono', 9)
        )
        self.status_text.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Performance indicator
        self.perf_indicator = ttk.Label(
            self.status_bar,
            text="⚡",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12)
        )
        self.perf_indicator.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def update_status(self, message):
        """Update the status bar"""
        self.status_text.config(text=message)
        self.root.update()
        
    def update_server_info(self):
        """Update server information display"""
        if hasattr(self, 'server_info'):
            info_text = f"""Server Information:
═══════════════════════════════════════════════════════════

Platform: {self.detect_platform()}
Python: {sys.version.split()[0]}
Server Status: {self.server_status}

Network Interfaces:
{self.get_network_info()}

Performance Profile: {self.performance_var.get() if hasattr(self, 'performance_var') else 'Maximum'}
Theme: {self.theme_var.get() if hasattr(self, 'theme_var') else 'Kali Dark'}

Ready to start PXE server...
Click 'START PXE SERVER' to begin.
            """
            
            self.server_info.config(state=tk.NORMAL)
            self.server_info.delete(1.0, tk.END)
            self.server_info.insert(1.0, info_text)
            self.server_info.config(state=tk.DISABLED)
            
    def get_network_info(self):
        """Get network interface information"""
        try:
            interfaces = self.network_manager.get_interfaces()
            info_lines = []
            for interface in interfaces:
                ip = self.network_manager.get_interface_ip(interface)
                if ip:
                    info_lines.append(f"  {interface}: {ip}")
            return '\n'.join(info_lines) if info_lines else "  No active interfaces found"
        except Exception as e:
            return f"  Error getting network info: {e}"
            
    def update_network_info(self):
        """Update network interface dropdown"""
        try:
            interfaces = self.network_manager.get_interfaces()
            self.interface_combo['values'] = interfaces
            if interfaces:
                self.interface_var.set(interfaces[0])
        except Exception as e:
            self.update_status(f"Network error: {e}")
            
    def start_server(self):
        """Start the PXE server"""
        if self.is_server_running:
            return
            
        def server_thread():
            try:
                self.update_status("Starting PXE server...")
                self.logger.start_session()
                
                # Create server instance
                self.pxe_server = PXEServer(
                    settings=self.settings,
                    logger=self.logger,
                    network_manager=self.network_manager
                )
                
                # Prepare boot files
                self.update_status("Preparing boot files...")
                if not self.pxe_server.prepare_boot_files():
                    self.update_status("Failed to prepare boot files")
                    return
                    
                # Start server
                self.update_status("Starting servers...")
                self.pxe_server.start()
                self.is_server_running = True
                
                # Update UI
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.status_label.config(text="● RUNNING", foreground=self.colors['success'])
                self.server_status = "RUNNING"
                
                self.update_status("PXE Server is running!")
                self.logger.success("PXE Server started successfully")
                self.update_server_info()
                
                # Start monitoring
                self.start_monitoring()
                
            except Exception as e:
                self.update_status(f"Server error: {e}")
                self.logger.error(f"Failed to start server: {e}")
                
        threading.Thread(target=server_thread, daemon=True).start()
        
    def stop_server(self):
        """Stop the PXE server"""
        if not self.is_server_running:
            return
            
        try:
            self.update_status("Stopping PXE server...")
            if self.pxe_server:
                self.pxe_server.stop()
                
            self.is_server_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="● STOPPED", foreground=self.colors['error'])
            self.server_status = "STOPPED"
            
            self.update_status("PXE Server stopped")
            self.logger.info("PXE Server stopped")
            self.update_server_info()
            
            # Stop monitoring
            self.stop_monitoring()
            
        except Exception as e:
            self.update_status(f"Stop error: {e}")
            self.logger.error(f"Error stopping server: {e}")
            
    def show_boot_instructions(self):
        """Show boot instructions"""
        instructions = """
🖥️ PXE BOOT INSTRUCTIONS

1. Ensure target PC is connected to the same network
2. Enter BIOS/UEFI settings (F2, F12, or Del key)
3. Enable PXE boot or Network Boot
4. Set Network Boot as first boot priority
5. Save changes and reboot
6. The PC will connect to our PXE server

⚠️ IMPORTANT NOTES:
• Make sure no other DHCP servers are running
• The target PC must be on the same network
• Some BIOS require specific PXE settings
• This server works across platforms (Termux, Linux, macOS, Windows)

The PXE server is now running and ready to serve boot files!
        """
        messagebox.showinfo("Boot Instructions", instructions)
        
    def apply_network_config(self):
        """Apply network configuration"""
        try:
            config = {
                'interface': self.interface_var.get(),
                'server_ip': self.server_ip_var.get(),
                'dhcp_start': self.dhcp_start_var.get(),
                'dhcp_end': self.dhcp_end_var.get()
            }
            self.settings.save_config(config)
            self.update_status("Network configuration saved")
        except Exception as e:
            self.update_status(f"Config error: {e}")
            
    def apply_performance(self):
        """Apply performance profile"""
        try:
            profile = self.performance_var.get()
            self.settings.set('performance', profile)
            
            # Update description
            descriptions = {
                'Maximum': 'Ultimate performance for gaming and intensive tasks. CPU governor set to performance, maximum memory allocation, no power saving.',
                'Gaming': 'Optimized for gaming with real-time scheduling, maximum GPU acceleration, and high network performance.',
                'Balanced': 'Balanced performance for general use with moderate power management and system responsiveness.',
                'Minimal': 'Power-saving configuration for battery life and minimal resource usage.'
            }
            
            desc = descriptions.get(profile, profile)
            self.performance_desc.config(state=tk.NORMAL)
            self.performance_desc.delete(1.0, tk.END)
            self.performance_desc.insert(1.0, desc)
            self.performance_desc.config(state=tk.DISABLED)
            
            self.update_status(f"Performance profile '{profile}' applied")
        except Exception as e:
            self.update_status(f"Performance error: {e}")
            
    def run_benchmark(self):
        """Run performance benchmark"""
        def benchmark_thread():
            try:
                self.update_status("Running performance benchmark...")
                
                # Create optimization script
                profile = self.performance_var.get()
                script_path = self.performance_optimizer.create_system_optimization_script(profile.lower())
                
                self.update_status("Benchmark completed - optimization script created")
                self.logger.info(f"Performance benchmark completed for {profile} profile")
                
            except Exception as e:
                self.update_status(f"Benchmark error: {e}")
                self.logger.error(f"Benchmark failed: {e}")
                
        threading.Thread(target=benchmark_thread, daemon=True).start()
        
    def apply_customization(self):
        """Apply Arch customization"""
        try:
            theme = self.theme_var.get()
            tools = self.tools_var.get()
            
            self.settings.set('ui_theme', theme)
            self.settings.set('tools', tools)
            
            # Create customization
            result = self.arch_customizer.create_all_customizations(theme, self.performance_var.get())
            
            if result:
                self.update_status(f"Customization applied: {theme} theme with {tools}")
                self.logger.success(f"Arch customizations created for {theme} theme")
            else:
                self.update_status("Customization failed")
                
        except Exception as e:
            self.update_status(f"Customization error: {e}")
            
    def preview_config(self):
        """Preview configuration"""
        try:
            config = {
                'Theme': self.theme_var.get(),
                'Performance': self.performance_var.get(),
                'Tools': self.tools_var.get(),
                'Interface': self.interface_var.get(),
                'Server IP': self.server_ip_var.get()
            }
            
            preview = "Configuration Preview:\n" + "="*30 + "\n"
            for key, value in config.items():
                preview += f"{key}: {value}\n"
                
            messagebox.showinfo("Configuration Preview", preview)
            
        except Exception as e:
            self.update_status(f"Preview error: {e}")
            
    def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring_active = True
        self.update_monitoring()
        
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        
    def update_monitoring(self):
        """Update monitoring display"""
        if not self.monitoring_active:
            return
            
        try:
            import psutil
            import platform
            
            # System information
            system_info = f"""System Information:
═══════════════════════════════════════
Platform: {platform.platform()}
Python: {python_version}
CPU: {platform.processor() or 'Unknown'}
Memory: {psutil.virtual_memory().total // (1024**3)} GB total

Network Interfaces: {len(self.network_manager.get_interfaces())}
PXE Server: {self.server_status}
Performance Profile: {self.performance_var.get() if hasattr(self, 'performance_var') else 'Maximum'}
            """
            
            # Performance metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = f"""Performance Metrics:
═══════════════════════════════════════
CPU Usage: {cpu_percent}%
CPU Cores: {psutil.cpu_count()}

Memory: {memory.percent}% used
  Total: {memory.total // (1024**3)} GB
  Available: {memory.available // (1024**3)} GB

Disk: {disk.percent}% used
  Total: {disk.total // (1024**3)} GB
  Free: {disk.free // (1024**3)} GB

Network: {len(psutil.net_if_addrs())} interfaces
Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Update displays
            self.system_info.config(state=tk.NORMAL)
            self.system_info.delete(1.0, tk.END)
            self.system_info.insert(1.0, system_info)
            self.system_info.config(state=tk.DISABLED)
            
            self.metrics_display.config(state=tk.NORMAL)
            self.metrics_display.delete(1.0, tk.END)
            self.metrics_display.insert(1.0, metrics)
            self.metrics_display.config(state=tk.DISABLED)
            
            # Update performance indicator
            if cpu_percent > 80:
                self.perf_indicator.config(text="🔥", foreground=self.colors['error'])
            elif cpu_percent > 50:
                self.perf_indicator.config(text="⚡", foreground=self.colors['warning'])
            else:
                self.perf_indicator.config(text="✅", foreground=self.colors['success'])
                
        except Exception as e:
            self.update_status(f"Monitoring error: {e}")
            
        # Schedule next update
        if self.monitoring_active:
            self.root.after(2000, self.update_monitoring)  # Update every 2 secondsMain GUI Window for Termux PXE Boot
Cross-platform compatible GUI with modern interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pxe.server import PXEServer
    from config.settings import Settings
    from utils.logger import Logger
    from utils.network import NetworkManager
    from arch.customizer import ArchCustomizer
    from optimizations.performance import PerformanceOptimizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are properly installed.")

class MainWindow:
    def __init__(self, root, app, settings=None, logger=None, network_manager=None, pxe_server=None, arch_customizer=None, performance_optimizer=None):
        self.root = root
        self.app = app
        self.settings = settings or Settings()
        self.logger = logger or Logger()
        self.network_manager = network_manager or NetworkManager()
        self.pxe_server = pxe_server
        self.arch_customizer = arch_customizer or ArchCustomizer(self.settings, self.logger)
        self.performance_optimizer = performance_optimizer or PerformanceOptimizer(self.settings, self.logger)
        
        # Server state
        self.is_server_running = False
        self.server_status = "STOPPED"
        
        # Performance monitoring
        self.monitoring_active = False
        self.performance_data = {}
        
        # Create GUI
        self.setup_styles()
        self.create_interface()
        self.center_window()
        
        # Start background tasks
        self.update_network_info()
        
    def setup_styles(self):
        """Setup modern, Kali-inspired styling"""
        style = ttk.Style()
        
        # Try to use modern theme
        try:
            style.theme_use('clam')
        except:
            style.theme_use('default')
            
        # Configure custom styles for dark theme
        self.colors = {
            'bg': '#0a0a0a',
            'fg': '#00ff00',
            'secondary': '#1a1a1a',
            'accent': '#00aa00',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'success': '#00ff88'
        }
        
        # Override styles
        style.configure('Dark.TFrame', background=self.colors['bg'], relief='flat', borderwidth=0)
        style.configure('Dark.TLabel', background=self.colors['bg'], foreground=self.colors['fg'], 
                       font=('JetBrains Mono', 10))
        style.configure('Dark.TButton', background=self.colors['secondary'], 
                       foreground=self.colors['fg'], font=('JetBrains Mono', 10, 'bold'),
                       relief='flat', borderwidth=1)
        style.configure('Dark.TButton:active', background=self.colors['accent'])
        style.configure('Dark.TEntry', fieldbackground=self.colors['secondary'], 
                       foreground=self.colors['fg'], font=('JetBrains Mono', 10))
        style.configure('Dark.Horizontal.TProgressbar', background=self.colors['accent'])
        style.configure('Dark.TNotebook', background=self.colors['bg'])
        style.configure('Dark.TNotebook.Tab', background=self.colors['secondary'], 
                       foreground=self.colors['fg'], padding=[10, 5])
        
    def create_interface(self):
        """Create the main interface"""
        # Main container
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        self.create_title_section(main_container)
        
        # Tab control for different sections
        self.create_notebook(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_title_section(self, parent):
        """Create the title section"""
        title_frame = ttk.Frame(parent, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Main title
        title_label = ttk.Label(
            title_frame,
            text="⚡ TERMUX PXE BOOT - STEROID EDITION ⚡",
            style='Dark.TLabel',
            font=('JetBrains Mono', 20, 'bold')
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            title_frame,
            text="Cross-Platform Network Boot Server - Performance Optimized",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12)
        )
        subtitle_label.pack()
        
        # Version and platform info
        info_text = f"v3.0.0 - Steroid Edition | Platform: {self.detect_platform()} | Python: {sys.version.split()[0]}"
        info_label = ttk.Label(
            title_frame,
            text=info_text,
            style='Dark.TLabel',
            font=('JetBrains Mono', 9)
        )
        info_label.pack()
        
    def detect_platform(self):
        """Detect the current platform"""
        import platform
        system = platform.system()
        if system == "Linux":
            if os.path.exists("/data/data/com.termux/files/home"):
                return "Termux (Android)"
            else:
                return "Linux"
        elif system == "Darwin":
            return "macOS"
        elif system == "Windows":
            return "Windows"
        else:
            return system
            
    def create_notebook(self, parent):
        """Create notebook with tabs for different functions"""
        self.notebook = ttk.Notebook(parent, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Server Control Tab
        self.server_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.server_frame, text="🚀 Server Control")
        self.create_server_tab()
        
        # Network Config Tab
        self.network_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.network_frame, text="🌐 Network Config")
        self.create_network_tab()
        
        # Performance Tab
        self.performance_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.performance_frame, text="⚡ Performance")
        self.create_performance_tab()
        
        # Arch Customization Tab
        self.arch_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.arch_frame, text="🎨 Arch Customization")
        self.create_arch_tab()
        
        # Monitoring Tab
        self.monitor_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.monitor_frame, text="📊 Monitoring")
        self.create_monitoring_tab()
        
    def create_server_tab(self):
        """Create server control tab"""
        # Server control section
        control_frame = ttk.LabelFrame(self.server_frame, text="Server Control", style='Dark.TFrame')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Start/Stop buttons
        buttons_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_button = ttk.Button(
            buttons_frame,
            text="▶️ START PXE SERVER",
            command=self.start_server,
            style='Dark.TButton'
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            buttons_frame,
            text="⏹️ STOP SERVER",
            command=self.stop_server,
            style='Dark.TButton',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="🖥️ Boot Instructions",
            command=self.show_boot_instructions,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
        # Status display
        status_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(status_frame, text="Status:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.status_label = ttk.Label(
            status_frame,
            text="● STOPPED",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12, 'bold')
        )
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Server information
        info_frame = ttk.LabelFrame(self.server_frame, text="Server Information", style='Dark.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrolled text for server info
        self.server_info = tk.Text(
            info_frame,
            height=10,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['accent'],
            wrap=tk.WORD
        )
        
        # Scrollbar for server info
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.server_info.yview)
        self.server_info.configure(yscrollcommand=info_scrollbar.set)
        
        self.server_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize server info
        self.update_server_info()
        
    def create_network_tab(self):
        """Create network configuration tab"""
        # Network interface selection
        interface_frame = ttk.LabelFrame(self.network_frame, text="Network Interface", style='Dark.TFrame')
        interface_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Interface dropdown
        interface_select_frame = ttk.Frame(interface_frame, style='Dark.TFrame')
        interface_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(interface_select_frame, text="Interface:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.interface_var = tk.StringVar()
        self.interface_combo = ttk.Combobox(
            interface_select_frame,
            textvariable=self.interface_var,
            style='Dark.TEntry',
            state='readonly'
        )
        self.interface_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # IP Configuration
        ip_frame = ttk.LabelFrame(self.network_frame, text="IP Configuration", style='Dark.TFrame')
        ip_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Server IP
        server_ip_frame = ttk.Frame(ip_frame, style='Dark.TFrame')
        server_ip_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(server_ip_frame, text="Server IP:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.server_ip_var = tk.StringVar(value="192.168.1.100")
        ttk.Entry(server_ip_frame, textvariable=self.server_ip_var, style='Dark.TEntry', width=15).pack(side=tk.LEFT, padx=(10, 0))
        
        # DHCP Range
        dhcp_frame = ttk.Frame(ip_frame, style='Dark.TFrame')
        dhcp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dhcp_frame, text="DHCP Range:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.dhcp_start_var = tk.StringVar(value="192.168.1.50")
        self.dhcp_end_var = tk.StringVar(value="192.168.1.200")
        
        ttk.Entry(dhcp_frame, textvariable=self.dhcp_start_var, style='Dark.TEntry', width=12).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(dhcp_frame, text="to", style='Dark.TLabel').pack(side=tk.LEFT)
        ttk.Entry(dhcp_frame, textvariable=self.dhcp_end_var, style='Dark.TEntry', width=12).pack(side=tk.LEFT, padx=5)
        
        # Apply button
        ttk.Button(
            ip_frame,
            text="💾 Apply Network Config",
            command=self.apply_network_config,
            style='Dark.TButton'
        ).pack(pady=10)
        
    def create_performance_tab(self):
        """Create performance optimization tab"""
        # Performance profile selection
        profile_frame = ttk.LabelFrame(self.performance_frame, text="Performance Profile", style='Dark.TFrame')
        profile_frame.pack(fill=tk.X, padx=10, pady=10)
        
        profile_select_frame = ttk.Frame(profile_frame, style='Dark.TFrame')
        profile_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(profile_select_frame, text="Profile:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.performance_var = tk.StringVar(value="Maximum")
        profile_combo = ttk.Combobox(
            profile_select_frame,
            textvariable=self.performance_var,
            values=["Maximum", "Gaming", "Balanced", "Minimal"],
            style='Dark.TEntry',
            state='readonly'
        )
        profile_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Performance controls
        controls_frame = ttk.Frame(profile_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            controls_frame,
            text="⚡ Apply Performance",
            command=self.apply_performance,
            style='Dark.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="📊 Benchmark",
            command=self.run_benchmark,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
        # Performance description
        self.performance_desc = tk.Text(
            profile_frame,
            height=6,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.performance_desc.pack(fill=tk.X, padx=10, pady=10)
        
    def create_arch_tab(self):
        """Create Arch Linux customization tab"""
        # Theme selection
        theme_frame = ttk.LabelFrame(self.arch_frame, text="Theme & Customization", style='Dark.TFrame')
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        theme_select_frame = ttk.Frame(theme_frame, style='Dark.TFrame')
        theme_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(theme_select_frame, text="Theme:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.theme_var = tk.StringVar(value="Kali Dark")
        theme_combo = ttk.Combobox(
            theme_select_frame,
            textvariable=self.theme_var,
            values=["Kali Dark", "Cyberpunk", "Matrix", "Neon Green"],
            style='Dark.TEntry',
            state='readonly'
        )
        theme_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Tool selection
        tools_frame = ttk.LabelFrame(self.arch_frame, text="Tool Package", style='Dark.TFrame')
        tools_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tools_select_frame = ttk.Frame(tools_frame, style='Dark.TFrame')
        tools_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(tools_select_frame, text="Tools:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.tools_var = tk.StringVar(value="Kali Tools + Performance")
        tools_combo = ttk.Combobox(
            tools_select_frame,
            textvariable=self.tools_var,
            values=["Kali Tools + Performance", "Full Kali Suite", "Pentesting Essentials", "Custom Selection"],
            style='Dark.TEntry',
            state='readonly'
        )
        tools_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Customization controls
        controls_frame = ttk.Frame(theme_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            controls_frame,
            text="🎨 Apply Customization",
            command=self.apply_customization,
            style='Dark.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="📋 Preview Config",
            command=self.preview_config,
            style='Dark.TButton'
        ).pack(side=tk.LEFT)
        
    def create_monitoring_tab(self):
        """Create monitoring tab"""
        # System information
        info_frame = ttk.LabelFrame(self.monitor_frame, text="System Information", style='Dark.TFrame')
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # System info display
        self.system_info = tk.Text(
            info_frame,
            height=8,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.system_info.pack(fill=tk.X, padx=10, pady=10)
        
        # Performance metrics
        metrics_frame = ttk.LabelFrame(self.monitor_frame, text="Performance Metrics", style='Dark.TFrame')
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Metrics display
        self.metrics_display = tk.Text(
            metrics_frame,
            height=10,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('JetBrains Mono', 9),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.metrics_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_bar = ttk.Frame(parent, style='Dark.TFrame')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status text
        self.status_text = ttk.Label(
            self.status_bar,
            text="Ready",
            style='Dark.TLabel',
            font=('JetBrains Mono', 9)
        )
        self.status_text.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Performance indicator
        self.perf_indicator = ttk.Label(
            self.status_bar,
            text="⚡",
            style='Dark.TLabel',
            font=('JetBrains Mono', 12)
        )
        self.perf_indicator.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def update_status(self, message):
        """Update the status bar"""
        self.status_text.config(text=message)
        self.root.update()
        
    def update_server_info(self):
        """Update server information display"""
        if hasattr(self, 'server_info'):
            info_text = f"""Server Information:
═══════════════════════════════════════════════════════════

Platform: {self.detect_platform()}
Python: {sys.version.split()[0]}
Server Status: {self.server_status}

Network Interfaces:
{self.get_network_info()}

Performance Profile: {self.performance_var.get() if hasattr(self, 'performance_var') else 'Maximum'}
Theme: {self.theme_var.get() if hasattr(self, 'theme_var') else 'Kali Dark'}

Ready to start PXE server...
Click 'START PXE SERVER' to begin.
            """
            
            self.server_info.config(state=tk.NORMAL)
            self.server_info.delete(1.0, tk.END)
            self.server_info.insert(1.0, info_text)
            self.server_info.config(state=tk.DISABLED)
            
    def get_network_info(self):
        """Get network interface information"""
        try:
            interfaces = self.network_manager.get_interfaces()
            info_lines = []
            for interface in interfaces:
                ip = self.network_manager.get_interface_ip(interface)
                if ip:
                    info_lines.append(f"  {interface}: {ip}")
            return '\n'.join(info_lines) if info_lines else "  No active interfaces found"
        except Exception as e:
            return f"  Error getting network info: {e}"
            
    def update_network_info(self):
        """Update network interface dropdown"""
        try:
            interfaces = self.network_manager.get_interfaces()
            self.interface_combo['values'] = interfaces
            if interfaces:
                self.interface_var.set(interfaces[0])
        except Exception as e:
            self.update_status(f"Network error: {e}")
            
    def start_server(self):
        """Start the PXE server"""
        if self.is_server_running:
            return
            
        def server_thread():
            try:
                self.update_status("Starting PXE server...")
                self.logger.start_session()
                
                # Create server instance
                self.pxe_server = PXEServer(
                    settings=self.settings,
                    logger=self.logger,
                    network_manager=self.network_manager
                )
                
                # Prepare boot files
                self.update_status("Preparing boot files...")
                if not self.pxe_server.prepare_boot_files():
                    self.update_status("Failed to prepare boot files")
                    return
                    
                # Start server
                self.update_status("Starting servers...")
                self.pxe_server.start()
                self.is_server_running = True
                
                # Update UI
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.status_label.config(text="● RUNNING", foreground=self.colors['success'])
                self.server_status = "RUNNING"
                
                self.update_status("PXE Server is running!")
                self.logger.success("PXE Server started successfully")
                self.update_server_info()
                
                # Start monitoring
                self.start_monitoring()
                
            except Exception as e:
                self.update_status(f"Server error: {e}")
                self.logger.error(f"Failed to start server: {e}")
                
        threading.Thread(target=server_thread, daemon=True).start()
        
    def stop_server(self):
        """Stop the PXE server"""
        if not self.is_server_running:
            return
            
        try:
            self.update_status("Stopping PXE server...")
            if self.pxe_server:
                self.pxe_server.stop()
                
            self.is_server_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="● STOPPED", foreground=self.colors['error'])
            self.server_status = "STOPPED"
            
            self.update_status("PXE Server stopped")
            self.logger.info("PXE Server stopped")
            self.update_server_info()
            
            # Stop monitoring
            self.stop_monitoring()
            
        except Exception as e:
            self.update_status(f"Stop error: {e}")
            self.logger.error(f"Error stopping server: {e}")
            
    def show_boot_instructions(self):
        """Show boot instructions"""
        instructions = """
🖥️ PXE BOOT INSTRUCTIONS

1. Ensure target PC is connected to the same network
2. Enter BIOS/UEFI settings (F2, F12, or Del key)
3. Enable PXE boot or Network Boot
4. Set Network Boot as first boot priority
5. Save changes and reboot
6. The PC will connect to our PXE server

⚠️ IMPORTANT NOTES:
• Make sure no other DHCP servers are running
• The target PC must be on the same network
• Some BIOS require specific PXE settings
• This server works across platforms (Termux, Linux, macOS, Windows)

The PXE server is now running and ready to serve boot files!
        """
        messagebox.showinfo("Boot Instructions", instructions)
        
    def apply_network_config(self):
        """Apply network configuration"""
        try:
            config = {
                'interface': self.interface_var.get(),
                'server_ip': self.server_ip_var.get(),
                'dhcp_start': self.dhcp_start_var.get(),
                'dhcp_end': self.dhcp_end_var.get()
            }
            self.settings.save_config(config)
            self.update_status("Network configuration saved")
        except Exception as e:
            self.update_status(f"Config error: {e}")
            
    def apply_performance(self):
        """Apply performance profile"""
        try:
            profile = self.performance_var.get()
            self.settings.set('performance', profile)
            
            # Update description
            descriptions = {
                'Maximum': 'Ultimate performance for gaming and intensive tasks. CPU governor set to performance, maximum memory allocation, no power saving.',
                'Gaming': 'Optimized for gaming with real-time scheduling, maximum GPU acceleration, and high network performance.',
                'Balanced': 'Balanced performance for general use with moderate power management and system responsiveness.',
                'Minimal': 'Power-saving configuration for battery life and minimal resource usage.'
            }
            
            desc = descriptions.get(profile, profile)
            self.performance_desc.config(state=tk.NORMAL)
            self.performance_desc.delete(1.0, tk.END)
            self.performance_desc.insert(1.0, desc)
            self.performance_desc.config(state=tk.DISABLED)
            
            self.update_status(f"Performance profile '{profile}' applied")
        except Exception as e:
            self.update_status(f"Performance error: {e}")
            
    def run_benchmark(self):
        """Run performance benchmark"""
        def benchmark_thread():
            try:
                self.update_status("Running performance benchmark...")
                
                # Create optimization script
                profile = self.performance_var.get()
                script_path = self.performance_optimizer.create_system_optimization_script(profile.lower())
                
                self.update_status("Benchmark completed - optimization script created")
                self.logger.info(f"Performance benchmark completed for {profile} profile")
                
            except Exception as e:
                self.update_status(f"Benchmark error: {e}")
                self.logger.error(f"Benchmark failed: {e}")
                
        threading.Thread(target=benchmark_thread, daemon=True).start()
        
    def apply_customization(self):
        """Apply Arch customization"""
        try:
            theme = self.theme_var.get()
            tools = self.tools_var.get()
            
            self.settings.set('ui_theme', theme)
            self.settings.set('tools', tools)
            
            # Create customization
            result = self.arch_customizer.create_all_customizations(theme, self.performance_var.get())
            
            if result:
                self.update_status(f"Customization applied: {theme} theme with {tools}")
                self.logger.success(f"Arch customizations created for {theme} theme")
            else:
                self.update_status("Customization failed")
                
        except Exception as e:
            self.update_status(f"Customization error: {e}")
            
    def preview_config(self):
        """Preview configuration"""
        try:
            config = {
                'Theme': self.theme_var.get(),
                'Performance': self.performance_var.get(),
                'Tools': self.tools_var.get(),
                'Interface': self.interface_var.get(),
                'Server IP': self.server_ip_var.get()
            }
            
            preview = "Configuration Preview:\n" + "="*30 + "\n"
            for key, value in config.items():
                preview += f"{key}: {value}\n"
                
            messagebox.showinfo("Configuration Preview", preview)
            
        except Exception as e:
            self.update_status(f"Preview error: {e}")
            
    def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring_active = True
        self.update_monitoring()
        
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        
    def update_monitoring(self):
        """Update monitoring display"""
        if not self.monitoring_active:
            return
            
        try:
            import psutil
            import platform
            
            # System information
            system_info = f"""System Information:
═══════════════════════════════════════
Platform: {platform.platform()}
Python: {python_version}
CPU: {platform.processor() or 'Unknown'}
Memory: {psutil.virtual_memory().total // (1024**3)} GB total

Network Interfaces: {len(self.network_manager.get_interfaces())}
PXE Server: {self.server_status}
Performance Profile: {self.performance_var.get() if hasattr(self, 'performance_var') else 'Maximum'}
            """
            
            # Performance metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = f"""Performance Metrics:
═══════════════════════════════════════
CPU Usage: {cpu_percent}%
CPU Cores: {psutil.cpu_count()}

Memory: {memory.percent}% used
  Total: {memory.total // (1024**3)} GB
  Available: {memory.available // (1024**3)} GB

Disk: {disk.percent}% used
  Total: {disk.total // (1024**3)} GB
  Free: {disk.free // (1024**3)} GB

Network: {len(psutil.net_if_addrs())} interfaces
Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Update displays
            self.system_info.config(state=tk.NORMAL)
            self.system_info.delete(1.0, tk.END)
            self.system_info.insert(1.0, system_info)
            self.system_info.config(state=tk.DISABLED)
            
            self.metrics_display.config(state=tk.NORMAL)
            self.metrics_display.delete(1.0, tk.END)
            self.metrics_display.insert(1.0, metrics)
            self.metrics_display.config(state=tk.DISABLED)
            
            # Update performance indicator
            if cpu_percent > 80:
                self.perf_indicator.config(text="🔥", foreground=self.colors['error'])
            elif cpu_percent > 50:
                self.perf_indicator.config(text="⚡", foreground=self.colors['warning'])
            else:
                self.perf_indicator.config(text="✅", foreground=self.colors['success'])
                
        except Exception as e:
            self.update_status(f"Monitoring error: {e}")
            
        # Schedule next update
        if self.monitoring_active:
            self.root.after(2000, self.update_monitoring)  # Update every 2 seconds

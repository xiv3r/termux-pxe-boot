#!/usr/bin/env python3
"""
Enhanced Installation and Deployment Script
Termux PXE Boot - Multi-Platform Support
"""

import os
import sys
import subprocess
import platform
import json
import argparse
from pathlib import Path

class EnhancedInstaller:
    def __init__(self):
        self.system = platform.system()
        self.architecture = platform.machine()
        self.is_termux = self._check_termux()
        
        # Color codes for terminal output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'end': '\033[0m',
            'bold': '\033[1m'
        }
        
    def _print_colored(self, message, color='white'):
        """Print colored message to terminal"""
        print(f"{self.colors[color]}{message}{self.colors['end']}")
        
    def _check_termux(self):
        """Check if running in Termux environment"""
        return os.path.exists('/data/data/com.termux/files/home')
        
    def _get_python_version(self):
        """Get Python version info"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
    def _check_requirements(self):
        """Check system requirements"""
        self._print_colored("🔍 Checking system requirements...", 'cyan')
        
        # Check Python version
        python_version = self._get_python_version()
        if sys.version_info >= (3, 8):
            self._print_colored(f"✅ Python {python_version} (compatible)", 'green')
        else:
            self._print_colored(f"❌ Python {python_version} - requires 3.8+", 'red')
            return False
            
        # Check network tools
        network_tools = ['ip', 'curl', 'wget']
        missing_tools = []
        
        for tool in network_tools:
            if not subprocess.run(['which', tool], capture_output=True).returncode == 0:
                missing_tools.append(tool)
                
        if missing_tools:
            self._print_colored(f"⚠️ Missing tools: {', '.join(missing_tools)}", 'yellow')
            return False
        else:
            self._print_colored("✅ Network tools available", 'green')
            
        return True
        
    def _install_python_packages(self):
        """Install required Python packages"""
        self._print_colored("📦 Installing Python packages...", 'cyan')
        
        # Read requirements
        requirements_file = Path(__file__).parent / 'requirements.txt'
        if requirements_file.exists():
            try:
                cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    self._print_colored("✅ Python packages installed successfully", 'green')
                    return True
                else:
                    self._print_colored(f"❌ Package installation failed: {result.stderr}", 'red')
                    return False
            except Exception as e:
                self._print_colored(f"❌ Error installing packages: {e}", 'red')
                return False
        else:
            self._print_colored("⚠️ requirements.txt not found, installing basic packages", 'yellow')
            # Install basic packages manually
            basic_packages = ['requests', 'psutil', 'pyyaml', 'colorama']
            for package in basic_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
                except subprocess.CalledProcessError:
                    self._print_colored(f"⚠️ Failed to install {package}", 'yellow')
            return True
            
    def _create_directories(self):
        """Create necessary directories"""
        self._print_colored("📁 Creating directory structure...", 'cyan')
        
        directories = [
            '~/.termux_pxe_boot',
            '~/.termux_pxe_boot/configs',
            '~/.termux_pxe_boot/logs',
            '~/.termux_pxe_boot/boot',
            '~/.termux_pxe_boot/tftp',
            '~/.termux_pxe_boot/assets',
            '~/.termux_pxe_boot/performance',
            '~/.termux_pxe_boot/themes'
        ]
        
        for directory in directories:
            path = Path(os.path.expanduser(directory))
            path.mkdir(parents=True, exist_ok=True)
            
        self._print_colored("✅ Directory structure created", 'green')
        
    def _setup_permissions(self):
        """Set proper file permissions"""
        self._print_colored("🔐 Setting permissions...", 'cyan')
        
        # Make scripts executable
        script_files = ['run.sh', 'install.sh', 'termux_pxe_boot.py', 'working_pxe_boot.py']
        
        for script in script_files:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                try:
                    script_path.chmod(0o755)
                    self._print_colored(f"✅ Made {script} executable", 'green')
                except Exception as e:
                    self._print_colored(f"⚠️ Could not set permissions for {script}: {e}", 'yellow')
                    
    def _create_desktop_shortcuts(self):
        """Create desktop shortcuts if available"""
        if self.is_termux:
            return
            
        self._print_colored("🖥️ Creating desktop shortcuts...", 'cyan')
        
        # Create shortcuts for different platforms
        if self.system == "Linux":
            shortcuts_dir = Path.home() / ".local/share/applications"
            shortcuts_dir.mkdir(parents=True, exist_ok=True)
            
            # Create desktop entry
            desktop_entry = f"""[Desktop Entry]
Name=Termux PXE Boot
Comment=Network Boot Server for Arch Linux
Exec={sys.executable} {Path(__file__).parent / 'termux_pxe_boot.py'}
Icon=applications-system
Terminal=true
Type=Application
Categories=System;Network;
"""
            
            shortcut_path = shortcuts_dir / "termux-pxe-boot.desktop"
            with open(shortcut_path, 'w') as f:
                f.write(desktop_entry)
                
            self._print_colored("✅ Desktop shortcut created", 'green')
            
    def _create_launcher_scripts(self):
        """Create platform-specific launcher scripts"""
        self._print_colored("🚀 Creating launcher scripts...", 'cyan')
        
        # Enhanced run.sh
        run_script = f'''#!/bin/bash
# Termux PXE Boot Enhanced Launcher
# Multi-platform support with performance optimizations

set -e

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Function to print colored output
print_status() {{
    echo -e "${{GREEN}}✅ $1${{NC}}"
}}

print_warning() {{
    echo -e "${{YELLOW}}⚠️  $1${{NC}}"
}}

print_error() {{
    echo -e "${{RED}}❌ $1${{NC}}"
}}

print_info() {{
    echo -e "${{BLUE}}ℹ️  $1${{NC}}"
}}

# Check environment
SYSTEM="{self.system}"
ARCH="{self.architecture}"
IS_TERMUX={str(self.is_termux).lower()}

print_info "System: $SYSTEM ($ARCH)"
print_info "Termux: $IS_TERMUX"

# Set up environment
export PYTHONPATH="${{PYTHONPATH}}:$(pwd)"

# Performance optimizations
if [ "$IS_TERMUX" = "true" ]; then
    export ANDROID_ROOT="/data/data/com.termux/files"
    export TERMUX_VERSION="0.118.0"
    
    # Android-specific optimizations
    if [ -d "/proc/sys/vm" ]; then
        echo 1 > /proc/sys/vm/swappiness 2>/dev/null || true
    fi
else
    # Linux/macOS optimizations
    ulimit -n 65536 2>/dev/null || true
fi

# Set Python optimizations
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONASYNCIODEBUG=0

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{{sys.version_info.major}}.{{sys.version_info.minor}}')")
print_status "Python version: $PYTHON_VERSION"

# Check required modules
REQUIRED_MODULES=("tkinter" "socket" "threading" "subprocess" "json" "os")
MISSING_MODULES=()

for module in "${{REQUIRED_MODULES[@]}}"; do
    if ! python3 -c "import $module" 2>/dev/null; then
        MISSING_MODULES+=("$module")
    fi
done

if [ ${{#MISSING_MODULES[@]}} -gt 0 ]; then
    print_error "Missing required modules: ${{MISSING_MODULES[*]}}"
    print_info "Please install missing modules or run install.sh"
    exit 1
fi

# Check main application
if [ ! -f "termux_pxe_boot.py" ]; then
    if [ -f "working_pxe_boot.py" ]; then
        print_warning "Using working_pxe_boot.py as main application"
        MAIN_APP="working_pxe_boot.py"
    else
        print_error "No main application found!"
        exit 1
    fi
else
    MAIN_APP="termux_pxe_boot.py"
fi

# Create log directory
mkdir -p ~/.termux_pxe_boot/logs

# Show startup banner
clear
echo -e "${{GREEN}}╔══════════════════════════════════════════════════════════════════════════════╗${{NC}}"
echo -e "${{GREEN}}║                    ⚡ TERMUX PXE BOOT - ENHANCED EDITION ⚡                    ║${{NC}}"
echo -e "${{GREEN}}║                       Arch Linux with Performance Optimizations                 ║${{NC}}"
echo -e "${{GREEN}}║                         Cross-Platform Network Boot Server                     ║${{NC}}"
echo -e "${{GREEN}}╚══════════════════════════════════════════════════════════════════════════════╝${{NC}}"
echo ""

# Performance information
echo -e "${{BLUE}}🚀 Performance Mode: Enhanced ${{NC}}"
echo -e "${{BLUE}}🔧 Platform: $SYSTEM ($ARCH) ${{NC}}"
echo -e "${{BLUE}}🐍 Python: $PYTHON_VERSION ${{NC}}"

# Check network
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo -e "${{GREEN}}🌐 Network: Connected ${{NC}}"
else
    echo -e "${{RED}}🌐 Network: Offline ${{NC}}"
fi

echo ""

# Set performance environment variables
export MALLOC_ARENA_MAX=2
export PYTHONMALLOC=malloc
export PTHREAD_NUM_THREADS=4

# Start the application
print_info "Starting Termux PXE Boot..."
python3 "$MAIN_APP"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    print_status "Application exited normally"
else
    echo ""
    print_error "Application exited with error"
    print_info "Check logs at: ~/.termux_pxe_boot/logs/pxe_boot.log"
fi
'''
        
        run_path = Path(__file__).parent / 'run_enhanced.sh'
        with open(run_path, 'w') as f:
            f.write(run_script)
        run_path.chmod(0o755)
        
        self._print_colored("✅ Enhanced launcher created", 'green')
        
    def _test_installation(self):
        """Test the installation"""
        self._print_colored("🧪 Testing installation...", 'cyan')
        
        # Test Python imports
        test_modules = [
            'tkinter', 'socket', 'threading', 'subprocess', 
            'json', 'os', 'sys', 'pathlib'
        ]
        
        for module in test_modules:
            try:
                __import__(module)
                self._print_colored(f"✅ {module} import OK", 'green')
            except ImportError as e:
                self._print_colored(f"❌ {module} import failed: {e}", 'red')
                return False
                
        # Test main application
        main_files = ['termux_pxe_boot.py', 'working_pxe_boot.py', 'termux_pxe_boot_complete.py']
        for file in main_files:
            if Path(file).exists():
                self._print_colored(f"✅ {file} found", 'green')
                
        self._print_colored("✅ Installation test completed", 'green')
        return True
        
    def install(self, verbose=False):
        """Run the complete installation process"""
        self._print_colored("⚡ Termux PXE Boot - Enhanced Installation", 'bold')
        self._print_colored("=" * 60, 'cyan')
        
        # System info
        self._print_colored(f"Operating System: {self.system}", 'cyan')
        self._print_colored(f"Architecture: {self.architecture}", 'cyan')
        self._print_colored(f"Termux Environment: {self.is_termux}", 'cyan')
        self._print_colored(f"Python Version: {self._get_python_version()}", 'cyan')
        print()
        
        # Installation steps
        steps = [
            ("Checking requirements", self._check_requirements),
            ("Installing Python packages", self._install_python_packages),
            ("Creating directories", self._create_directories),
            ("Setting permissions", self._setup_permissions),
            ("Creating launcher scripts", self._create_launcher_scripts),
            ("Creating desktop shortcuts", self._create_desktop_shortcuts),
            ("Testing installation", self._test_installation)
        ]
        
        for step_name, step_func in steps:
            self._print_colored(f"\n📋 {step_name}...", 'cyan')
            if verbose:
                print(f"   Running: {step_func.__name__}")
                
            try:
                if not step_func():
                    self._print_colored(f"❌ {step_name} failed", 'red')
                    return False
            except Exception as e:
                self._print_colored(f"❌ {step_name} failed: {e}", 'red')
                if verbose:
                    import traceback
                    traceback.print_exc()
                return False
                
        self._print_colored("\n🎉 Installation completed successfully!", 'bold')
        self._print_colored("\n📖 Quick Start:", 'cyan')
        self._print_colored("   ./run_enhanced.sh        # Start with enhanced features", 'white')
        self._print_colored("   ./run.sh                 # Start with standard features", 'white')
        self._print_colored("   python3 working_pxe_boot.py    # Start working version", 'white')
        self._print_colored("\n🌟 Features installed:", 'cyan')
        self._print_colored("   • Cross-platform compatibility", 'white')
        self._print_colored("   • Performance optimizations", 'white')
        self._print_colored("   • Enhanced error handling", 'white')
        self._print_colored("   • Desktop shortcuts", 'white')
        self._print_colored("   • Comprehensive logging", 'white')
        
        return True
        
    def uninstall(self):
        """Uninstall the application"""
        self._print_colored("🗑️  Uninstalling Termux PXE Boot...", 'cyan')
        
        # Remove directories
        directories = [
            '~/.termux_pxe_boot',
            '~/.config/termux_pxe_boot'
        ]
        
        for directory in directories:
            path = Path(os.path.expanduser(directory))
            if path.exists():
                import shutil
                shutil.rmtree(path)
                self._print_colored(f"✅ Removed {directory}", 'green')
                
        # Remove launcher scripts
        scripts = ['run_enhanced.sh', 'run.sh', 'install.sh']
        for script in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                script_path.unlink()
                self._print_colored(f"✅ Removed {script}", 'green')
                
        # Remove desktop shortcuts
        if self.system == "Linux":
            shortcut = Path.home() / ".local/share/applications/termux-pxe-boot.desktop"
            if shortcut.exists():
                shortcut.unlink()
                self._print_colored("✅ Removed desktop shortcut", 'green')
                
        self._print_colored("🎉 Uninstallation completed", 'green')

def main():
    parser = argparse.ArgumentParser(description='Termux PXE Boot Enhanced Installer')
    parser.add_argument('--install', action='store_true', help='Install the application')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the application')
    parser.add_argument('--test', action='store_true', help='Test installation only')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='Termux PXE Boot Enhanced 1.0.0')
    
    args = parser.parse_args()
    
    installer = EnhancedInstaller()
    
    if args.test:
        installer._check_requirements()
        installer._test_installation()
    elif args.uninstall:
        installer.uninstall()
    elif args.install or not any([args.uninstall, args.test]):
        installer.install(verbose=args.verbose)

if __name__ == "__main__":
    main()"""
Enhanced Installation and Deployment Script
Termux PXE Boot - Multi-Platform Support
"""

import os
import sys
import subprocess
import platform
import json
import argparse
from pathlib import Path

class EnhancedInstaller:
    def __init__(self):
        self.system = platform.system()
        self.architecture = platform.machine()
        self.is_termux = self._check_termux()
        
        # Color codes for terminal output
        self.colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'end': '\033[0m',
            'bold': '\033[1m'
        }
        
    def _print_colored(self, message, color='white'):
        """Print colored message to terminal"""
        print(f"{self.colors[color]}{message}{self.colors['end']}")
        
    def _check_termux(self):
        """Check if running in Termux environment"""
        return os.path.exists('/data/data/com.termux/files/home')
        
    def _get_python_version(self):
        """Get Python version info"""
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
    def _check_requirements(self):
        """Check system requirements"""
        self._print_colored("🔍 Checking system requirements...", 'cyan')
        
        # Check Python version
        python_version = self._get_python_version()
        if sys.version_info >= (3, 8):
            self._print_colored(f"✅ Python {python_version} (compatible)", 'green')
        else:
            self._print_colored(f"❌ Python {python_version} - requires 3.8+", 'red')
            return False
            
        # Check network tools
        network_tools = ['ip', 'curl', 'wget']
        missing_tools = []
        
        for tool in network_tools:
            if not subprocess.run(['which', tool], capture_output=True).returncode == 0:
                missing_tools.append(tool)
                
        if missing_tools:
            self._print_colored(f"⚠️ Missing tools: {', '.join(missing_tools)}", 'yellow')
            return False
        else:
            self._print_colored("✅ Network tools available", 'green')
            
        return True
        
    def _install_python_packages(self):
        """Install required Python packages"""
        self._print_colored("📦 Installing Python packages...", 'cyan')
        
        # Read requirements
        requirements_file = Path(__file__).parent / 'requirements.txt'
        if requirements_file.exists():
            try:
                cmd = [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    self._print_colored("✅ Python packages installed successfully", 'green')
                    return True
                else:
                    self._print_colored(f"❌ Package installation failed: {result.stderr}", 'red')
                    return False
            except Exception as e:
                self._print_colored(f"❌ Error installing packages: {e}", 'red')
                return False
        else:
            self._print_colored("⚠️ requirements.txt not found, installing basic packages", 'yellow')
            # Install basic packages manually
            basic_packages = ['requests', 'psutil', 'pyyaml', 'colorama']
            for package in basic_packages:
                try:
                    subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
                except subprocess.CalledProcessError:
                    self._print_colored(f"⚠️ Failed to install {package}", 'yellow')
            return True
            
    def _create_directories(self):
        """Create necessary directories"""
        self._print_colored("📁 Creating directory structure...", 'cyan')
        
        directories = [
            '~/.termux_pxe_boot',
            '~/.termux_pxe_boot/configs',
            '~/.termux_pxe_boot/logs',
            '~/.termux_pxe_boot/boot',
            '~/.termux_pxe_boot/tftp',
            '~/.termux_pxe_boot/assets',
            '~/.termux_pxe_boot/performance',
            '~/.termux_pxe_boot/themes'
        ]
        
        for directory in directories:
            path = Path(os.path.expanduser(directory))
            path.mkdir(parents=True, exist_ok=True)
            
        self._print_colored("✅ Directory structure created", 'green')
        
    def _setup_permissions(self):
        """Set proper file permissions"""
        self._print_colored("🔐 Setting permissions...", 'cyan')
        
        # Make scripts executable
        script_files = ['run.sh', 'install.sh', 'termux_pxe_boot.py', 'working_pxe_boot.py']
        
        for script in script_files:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                try:
                    script_path.chmod(0o755)
                    self._print_colored(f"✅ Made {script} executable", 'green')
                except Exception as e:
                    self._print_colored(f"⚠️ Could not set permissions for {script}: {e}", 'yellow')
                    
    def _create_desktop_shortcuts(self):
        """Create desktop shortcuts if available"""
        if self.is_termux:
            return
            
        self._print_colored("🖥️ Creating desktop shortcuts...", 'cyan')
        
        # Create shortcuts for different platforms
        if self.system == "Linux":
            shortcuts_dir = Path.home() / ".local/share/applications"
            shortcuts_dir.mkdir(parents=True, exist_ok=True)
            
            # Create desktop entry
            desktop_entry = f"""[Desktop Entry]
Name=Termux PXE Boot
Comment=Network Boot Server for Arch Linux
Exec={sys.executable} {Path(__file__).parent / 'termux_pxe_boot.py'}
Icon=applications-system
Terminal=true
Type=Application
Categories=System;Network;
"""
            
            shortcut_path = shortcuts_dir / "termux-pxe-boot.desktop"
            with open(shortcut_path, 'w') as f:
                f.write(desktop_entry)
                
            self._print_colored("✅ Desktop shortcut created", 'green')
            
    def _create_launcher_scripts(self):
        """Create platform-specific launcher scripts"""
        self._print_colored("🚀 Creating launcher scripts...", 'cyan')
        
        # Enhanced run.sh
        run_script = f'''#!/bin/bash
# Termux PXE Boot Enhanced Launcher
# Multi-platform support with performance optimizations

set -e

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Function to print colored output
print_status() {{
    echo -e "${{GREEN}}✅ $1${{NC}}"
}}

print_warning() {{
    echo -e "${{YELLOW}}⚠️  $1${{NC}}"
}}

print_error() {{
    echo -e "${{RED}}❌ $1${{NC}}"
}}

print_info() {{
    echo -e "${{BLUE}}ℹ️  $1${{NC}}"
}}

# Check environment
SYSTEM="{self.system}"
ARCH="{self.architecture}"
IS_TERMUX={str(self.is_termux).lower()}

print_info "System: $SYSTEM ($ARCH)"
print_info "Termux: $IS_TERMUX"

# Set up environment
export PYTHONPATH="${{PYTHONPATH}}:$(pwd)"

# Performance optimizations
if [ "$IS_TERMUX" = "true" ]; then
    export ANDROID_ROOT="/data/data/com.termux/files"
    export TERMUX_VERSION="0.118.0"
    
    # Android-specific optimizations
    if [ -d "/proc/sys/vm" ]; then
        echo 1 > /proc/sys/vm/swappiness 2>/dev/null || true
    fi
else
    # Linux/macOS optimizations
    ulimit -n 65536 2>/dev/null || true
fi

# Set Python optimizations
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONASYNCIODEBUG=0

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{{sys.version_info.major}}.{{sys.version_info.minor}}')")
print_status "Python version: $PYTHON_VERSION"

# Check required modules
REQUIRED_MODULES=("tkinter" "socket" "threading" "subprocess" "json" "os")
MISSING_MODULES=()

for module in "${{REQUIRED_MODULES[@]}}"; do
    if ! python3 -c "import $module" 2>/dev/null; then
        MISSING_MODULES+=("$module")
    fi
done

if [ ${{#MISSING_MODULES[@]}} -gt 0 ]; then
    print_error "Missing required modules: ${{MISSING_MODULES[*]}}"
    print_info "Please install missing modules or run install.sh"
    exit 1
fi

# Check main application
if [ ! -f "termux_pxe_boot.py" ]; then
    if [ -f "working_pxe_boot.py" ]; then
        print_warning "Using working_pxe_boot.py as main application"
        MAIN_APP="working_pxe_boot.py"
    else
        print_error "No main application found!"
        exit 1
    fi
else
    MAIN_APP="termux_pxe_boot.py"
fi

# Create log directory
mkdir -p ~/.termux_pxe_boot/logs

# Show startup banner
clear
echo -e "${{GREEN}}╔══════════════════════════════════════════════════════════════════════════════╗${{NC}}"
echo -e "${{GREEN}}║                    ⚡ TERMUX PXE BOOT - ENHANCED EDITION ⚡                    ║${{NC}}"
echo -e "${{GREEN}}║                       Arch Linux with Performance Optimizations                 ║${{NC}}"
echo -e "${{GREEN}}║                         Cross-Platform Network Boot Server                     ║${{NC}}"
echo -e "${{GREEN}}╚══════════════════════════════════════════════════════════════════════════════╝${{NC}}"
echo ""

# Performance information
echo -e "${{BLUE}}🚀 Performance Mode: Enhanced ${{NC}}"
echo -e "${{BLUE}}🔧 Platform: $SYSTEM ($ARCH) ${{NC}}"
echo -e "${{BLUE}}🐍 Python: $PYTHON_VERSION ${{NC}}"

# Check network
if ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    echo -e "${{GREEN}}🌐 Network: Connected ${{NC}}"
else
    echo -e "${{RED}}🌐 Network: Offline ${{NC}}"
fi

echo ""

# Set performance environment variables
export MALLOC_ARENA_MAX=2
export PYTHONMALLOC=malloc
export PTHREAD_NUM_THREADS=4

# Start the application
print_info "Starting Termux PXE Boot..."
python3 "$MAIN_APP"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    print_status "Application exited normally"
else
    echo ""
    print_error "Application exited with error"
    print_info "Check logs at: ~/.termux_pxe_boot/logs/pxe_boot.log"
fi
'''
        
        run_path = Path(__file__).parent / 'run_enhanced.sh'
        with open(run_path, 'w') as f:
            f.write(run_script)
        run_path.chmod(0o755)
        
        self._print_colored("✅ Enhanced launcher created", 'green')
        
    def _test_installation(self):
        """Test the installation"""
        self._print_colored("🧪 Testing installation...", 'cyan')
        
        # Test Python imports
        test_modules = [
            'tkinter', 'socket', 'threading', 'subprocess', 
            'json', 'os', 'sys', 'pathlib'
        ]
        
        for module in test_modules:
            try:
                __import__(module)
                self._print_colored(f"✅ {module} import OK", 'green')
            except ImportError as e:
                self._print_colored(f"❌ {module} import failed: {e}", 'red')
                return False
                
        # Test main application
        main_files = ['termux_pxe_boot.py', 'working_pxe_boot.py', 'termux_pxe_boot_complete.py']
        for file in main_files:
            if Path(file).exists():
                self._print_colored(f"✅ {file} found", 'green')
                
        self._print_colored("✅ Installation test completed", 'green')
        return True
        
    def install(self, verbose=False):
        """Run the complete installation process"""
        self._print_colored("⚡ Termux PXE Boot - Enhanced Installation", 'bold')
        self._print_colored("=" * 60, 'cyan')
        
        # System info
        self._print_colored(f"Operating System: {self.system}", 'cyan')
        self._print_colored(f"Architecture: {self.architecture}", 'cyan')
        self._print_colored(f"Termux Environment: {self.is_termux}", 'cyan')
        self._print_colored(f"Python Version: {self._get_python_version()}", 'cyan')
        print()
        
        # Installation steps
        steps = [
            ("Checking requirements", self._check_requirements),
            ("Installing Python packages", self._install_python_packages),
            ("Creating directories", self._create_directories),
            ("Setting permissions", self._setup_permissions),
            ("Creating launcher scripts", self._create_launcher_scripts),
            ("Creating desktop shortcuts", self._create_desktop_shortcuts),
            ("Testing installation", self._test_installation)
        ]
        
        for step_name, step_func in steps:
            self._print_colored(f"\n📋 {step_name}...", 'cyan')
            if verbose:
                print(f"   Running: {step_func.__name__}")
                
            try:
                if not step_func():
                    self._print_colored(f"❌ {step_name} failed", 'red')
                    return False
            except Exception as e:
                self._print_colored(f"❌ {step_name} failed: {e}", 'red')
                if verbose:
                    import traceback
                    traceback.print_exc()
                return False
                
        self._print_colored("\n🎉 Installation completed successfully!", 'bold')
        self._print_colored("\n📖 Quick Start:", 'cyan')
        self._print_colored("   ./run_enhanced.sh        # Start with enhanced features", 'white')
        self._print_colored("   ./run.sh                 # Start with standard features", 'white')
        self._print_colored("   python3 working_pxe_boot.py    # Start working version", 'white')
        self._print_colored("\n🌟 Features installed:", 'cyan')
        self._print_colored("   • Cross-platform compatibility", 'white')
        self._print_colored("   • Performance optimizations", 'white')
        self._print_colored("   • Enhanced error handling", 'white')
        self._print_colored("   • Desktop shortcuts", 'white')
        self._print_colored("   • Comprehensive logging", 'white')
        
        return True
        
    def uninstall(self):
        """Uninstall the application"""
        self._print_colored("🗑️  Uninstalling Termux PXE Boot...", 'cyan')
        
        # Remove directories
        directories = [
            '~/.termux_pxe_boot',
            '~/.config/termux_pxe_boot'
        ]
        
        for directory in directories:
            path = Path(os.path.expanduser(directory))
            if path.exists():
                import shutil
                shutil.rmtree(path)
                self._print_colored(f"✅ Removed {directory}", 'green')
                
        # Remove launcher scripts
        scripts = ['run_enhanced.sh', 'run.sh', 'install.sh']
        for script in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                script_path.unlink()
                self._print_colored(f"✅ Removed {script}", 'green')
                
        # Remove desktop shortcuts
        if self.system == "Linux":
            shortcut = Path.home() / ".local/share/applications/termux-pxe-boot.desktop"
            if shortcut.exists():
                shortcut.unlink()
                self._print_colored("✅ Removed desktop shortcut", 'green')
                
        self._print_colored("🎉 Uninstallation completed", 'green')

def main():
    parser = argparse.ArgumentParser(description='Termux PXE Boot Enhanced Installer')
    parser.add_argument('--install', action='store_true', help='Install the application')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the application')
    parser.add_argument('--test', action='store_true', help='Test installation only')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='Termux PXE Boot Enhanced 1.0.0')
    
    args = parser.parse_args()
    
    installer = EnhancedInstaller()
    
    if args.test:
        installer._check_requirements()
        installer._test_installation()
    elif args.uninstall:
        installer.uninstall()
    elif args.install or not any([args.uninstall, args.test]):
        installer.install(verbose=args.verbose)

if __name__ == "__main__":
    main()

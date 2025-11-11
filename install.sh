#!/bin/bash
# Termux PXE Boot Installation Script
# Arch Linux with Kali UI - No Root Required Installation

set -e

echo "⚡ Termux PXE Boot - Arch Linux Enhanced Edition ⚡"
echo "====================================================="
echo "📱 Android Termux Network Boot Server"
echo "🐧 Arch Linux with Kali-like UI"
echo "🎨 Performance Optimized"
echo "====================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running in Termux
check_termux() {
    if [[ ! -d "/data/data/com.termux/files" ]]; then
        print_error "This application must be run in Termux!"
        print_info "Please install Termux from F-Droid or Google Play Store"
        exit 1
    fi
    print_status "Termux environment detected"
}

# Check Python installation
check_python() {
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed!"
        print_info "Installing Python in Termux..."
        pkg update -y
        pkg install -y python python-dev
    fi
    print_status "Python installation confirmed"
    
    # Check Python version
    python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(python -c "import sys; print(sys.version_info >= (3, 6))") == "True" ]]; then
        print_status "Python version: $python_version (compatible)"
    else
        print_error "Python 3.6+ is required, found: $python_version"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Installing required packages..."
    
    # Update package list
    pkg update -y
    
    # Install Python dependencies
    pkg install -y python python-dev
    pkg install -y python-tkinter  # GUI support
    pkg install -y python-pip
    
    # Install network tools
    pkg install -y iproute2  # For network interface detection
    pkg install -y net-tools  # For ifconfig
    pkg install -y openssh    # For secure connections
    
    # Optional but recommended
    pkg install -y curl wget  # For downloading files
    pkg install -y git       # For version control
    
    print_status "Dependencies installed successfully"
}

# Install Python packages
install_python_packages() {
    print_info "Installing Python packages..."
    
    # Upgrade pip first
    python -m pip install --upgrade pip
    
    # Install required packages
    python -m pip install --user \
        tkinter \
        requests \
        configparser \
        pyyaml \
        psutil
    
    # Install GUI-related packages if needed
    python -m pip install --user \
        pillow \
        customtkinter  # Modern UI framework
    
    print_status "Python packages installed"
}

# Create directory structure
create_directories() {
    print_info "Creating application directories..."
    
    # Create main directories
    mkdir -p ~/.termux_pxe_boot/{configs,logs,boot,tftp,assets}
    mkdir -p ~/pxe_assets/{arch,customizer,scripts}
    mkdir -p ~/pxe_boot/{configs,logs}
    mkdir -p ~/pxe_tftp/{pxelinux.cfg,boot}
    
    print_status "Directory structure created"
}

# Set permissions
set_permissions() {
    print_info "Setting file permissions..."
    
    # Make scripts executable
    chmod +x termux_pxe_boot.py
    chmod +x run.sh
    chmod +x install.sh
    chmod +x uninstall.sh
    
    # Set proper permissions
    chmod 755 termux_pxe_boot.py
    chmod 755 run.sh
    
    print_status "Permissions set correctly"
}

# Create launcher script
create_launcher() {
    print_info "Creating launcher script..."
    
    cat > run.sh << 'EOF'
#!/bin/bash
# Termux PXE Boot Launcher
# Arch Linux with Kali UI

# Set up environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Change to script directory
cd "$(dirname "$0")"

# Check if Python GUI is available
if ! python -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter not found. Please install it:"
    echo "   pkg install python-tkinter"
    exit 1
fi

# Start the application
echo "⚡ Starting Termux PXE Boot..."
echo "🐧 Arch Linux with Kali UI"
echo "================================"
python termux_pxe_boot.py
EOF
    
    chmod +x run.sh
    print_status "Launcher script created"
}

# Create uninstall script
create_uninstaller() {
    print_info "Creating uninstaller script..."
    
    cat > uninstall.sh << 'EOF'
#!/bin/bash
# Termux PXE Boot Uninstaller

echo "🗑️  Termux PXE Boot Uninstaller"
echo "================================"
echo "This will remove all application files and configurations."
read -p "Are you sure? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Remove application directories
    rm -rf ~/.termux_pxe_boot
    rm -rf ~/pxe_assets
    rm -rf ~/pxe_boot
    rm -rf ~/pxe_tftp
    
    # Remove launcher scripts
    rm -f run.sh install.sh uninstall.sh
    rm -f termux_pxe_boot.py
    
    echo "✅ Termux PXE Boot has been uninstalled"
else
    echo "❌ Uninstallation cancelled"
fi
EOF
    
    chmod +x uninstall.sh
    print_status "Uninstaller script created"
}

# Test installation
test_installation() {
    print_info "Testing installation..."
    
    # Test Python import
    if python -c "import tkinter, sys, os, json, socket, threading, subprocess" 2>/dev/null; then
        print_status "Python modules imported successfully"
    else
        print_error "Python module import failed"
        return 1
    fi
    
    # Test file permissions
    if [[ -x "termux_pxe_boot.py" ]]; then
        print_status "Application file is executable"
    else
        print_error "Application file permission issue"
        return 1
    fi
    
    # Test directories
    if [[ -d "gui" && -d "pxe" && -d "config" && -d "utils" ]]; then
        print_status "Application structure verified"
    else
        print_error "Application structure incomplete"
        return 1
    fi
    
    return 0
}

# Create desktop shortcut (if termux:widget is available)
create_shortcut() {
    if [[ -d "$HOME/.shortcuts" ]]; then
        print_info "Creating desktop shortcut..."
        
        cat > ~/.shortcuts/termux-pxe-boot << EOF
#!/data/data/com.termux/files/usr/bin/bash
cd \$PWD
./run.sh
EOF
        
        chmod +x ~/.shortcuts/termux-pxe-boot
        print_status "Desktop shortcut created"
    fi
}

# Main installation function
main() {
    echo ""
    print_info "Starting installation process..."
    echo ""
    
    # Check environment
    check_termux
    check_python
    
    # Install dependencies
    install_dependencies
    install_python_packages
    
    # Setup application
    create_directories
    set_permissions
    create_launcher
    create_uninstaller
    create_shortcut
    
    # Test installation
    if test_installation; then
        echo ""
        echo "🎉 Installation completed successfully!"
        echo ""
        print_status "Termux PXE Boot is ready to use"
        echo ""
        echo "🚀 To start the application:"
        echo "   ./run.sh"
        echo ""
        print_info "Features included:"
        echo "   • Arch Linux with Kali-like UI"
        echo "   • Performance optimization profiles"
        echo "   • Network interface detection"
        echo "   • PXE boot server (DHCP + TFTP)"
        echo "   • Multiple theme support"
        echo "   • No root required"
        echo ""
        print_info "Next steps:"
        echo "   1. Connect your Android device to WiFi"
        echo "   2. Run: ./run.sh"
        echo "   3. Configure your network settings"
        echo "   4. Start the PXE server"
        echo "   5. Boot target PCs via network"
        echo ""
    else
        echo ""
        print_error "Installation test failed!"
        print_info "Please check the errors above and try again"
        exit 1
    fi
}

# Check for command line arguments
case "${1:-}" in
    --help|-h)
        echo "Termux PXE Boot Installation Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --test         Test installation without installing"
        echo "  --force        Force installation even if Termux not detected"
        echo ""
        exit 0
        ;;
    --test)
        print_info "Running installation test..."
        check_termux
        check_python
        test_installation
        exit $?
        ;;
    --force)
        print_warning "Bypassing Termux check (--force flag used)"
        ;;
esac

# Run main installation
main "$@"

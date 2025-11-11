#!/bin/bash
# Termux PXE Boot Launcher
# Arch Linux with Kali UI - No Root Required

# Set up environment
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Add current directory to path
PATH="$(pwd):$PATH"

# Change to script directory
cd "$(dirname "$0")"

# Check if Python GUI is available
if ! python -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter not found. Please install it:"
    echo "   pkg install python-tkinter"
    echo ""
    echo "📱 Run the installer to set up dependencies:"
    echo "   ./install.sh"
    exit 1
fi

# Check Python version
python_version=$(python -c "import sys; print(sys.version_info[:2])")
if [[ $(python -c "import sys; print(sys.version_info >= (3, 6))") == "False" ]]; then
    echo "❌ Python 3.6+ is required, found: ${python_version[0]}.${python_version[1]}"
    echo "   Please update Python in Termux"
    exit 1
fi

# Check if main application exists
if [[ ! -f "termux_pxe_boot.py" ]]; then
    echo "❌ Main application file not found!"
    echo "   Please ensure termux_pxe_boot.py is in the current directory"
    exit 1
fi

# Check if required modules exist
if [[ ! -d "gui" || ! -d "pxe" || ! -d "config" || ! -d "utils" ]]; then
    echo "❌ Application structure incomplete!"
    echo "   Please run the installer: ./install.sh"
    exit 1
fi

# Show startup banner
clear
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    ⚡ TERMUX PXE BOOT - ENHANCED EDITION ⚡                    ║"
echo "║                       Arch Linux with Kali-like UI                          ║"
echo "║                         Network Boot Server                                 ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starting application..."
echo "📱 Termux Environment: $(if [[ -d "/data/data/com.termux/files" ]]; then echo "✓ Detected"; else echo "⚠️  Not detected"; fi)"
echo "🐍 Python Version: $(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
echo "🌐 Network Status: $(if ping -c 1 8.8.8.8 >/dev/null 2>&1; then echo "✓ Connected"; else echo "✗ Offline"; fi)"
echo ""

# Set up logging
mkdir -p ~/.termux_pxe_boot/logs

# Start the application
echo "⚡ Launching Termux PXE Boot GUI..."
python termux_pxe_boot.py

# Check exit code
if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Application exited normally"
else
    echo ""
    echo "❌ Application exited with error"
    echo "📋 Check logs at: ~/.termux_pxe_boot/pxe_boot.log"
fi

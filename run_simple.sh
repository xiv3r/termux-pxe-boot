#!/bin/bash
# Simple Run Script for Termux PXE Boot
# No complex setup, just run the working application

echo "⚡ Termux PXE Boot - Working Edition ⚡"
echo "========================================"

# Check if Python GUI is available
if ! python -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter not found!"
    echo "Please install it with: pkg install python-tkinter"
    exit 1
fi

# Check if main application exists
if [[ ! -f "working_pxe_boot.py" ]]; then
    echo "❌ working_pxe_boot.py not found!"
    echo "Please ensure you have the main application file"
    exit 1
fi

# Show startup info
echo "🐍 Python version: $(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
echo "🌐 Network status: $(if ping -c 1 8.8.8.8 >/dev/null 2>&1; then echo "Connected"; else echo "Offline"; fi)"
echo ""

# Start the application
echo "🚀 Starting Termux PXE Boot..."
python working_pxe_boot.py

# Check exit status
if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Application exited normally"
else
    echo ""
    echo "❌ Application encountered an error"
    echo "Check the logs above for details"
fi# Simple Run Script for Termux PXE Boot
# No complex setup, just run the working application

echo "⚡ Termux PXE Boot - Working Edition ⚡"
echo "========================================"

# Check if Python GUI is available
if ! python -c "import tkinter" 2>/dev/null; then
    echo "❌ tkinter not found!"
    echo "Please install it with: pkg install python-tkinter"
    exit 1
fi

# Check if main application exists
if [[ ! -f "working_pxe_boot.py" ]]; then
    echo "❌ working_pxe_boot.py not found!"
    echo "Please ensure you have the main application file"
    exit 1
fi

# Show startup info
echo "🐍 Python version: $(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
echo "🌐 Network status: $(if ping -c 1 8.8.8.8 >/dev/null 2>&1; then echo "Connected"; else echo "Offline"; fi)"
echo ""

# Start the application
echo "🚀 Starting Termux PXE Boot..."
python working_pxe_boot.py

# Check exit status
if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Application exited normally"
else
    echo ""
    echo "❌ Application encountered an error"
    echo "Check the logs above for details"
fi

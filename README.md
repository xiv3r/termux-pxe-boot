# Termux PXE Boot - Arch Linux with Kali UI

![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![Platform](https://img.shields.io/badge/platform-Termux-orange)
![License](https://img.shields.io/badge/license-MIT-red)

**⚡ The Ultimate Termux PXE Boot Solution for Arch Linux with Kali-like UI ⚡**

A comprehensive Python-based GUI application that transforms your Android device running Termux into a powerful PXE boot server, enabling network installation of Arch Linux with a stunning Kali-inspired interface and performance optimizations.

## 🚀 Features

### Core Features
- **📱 Termux-Native GUI** - Beautiful, responsive interface designed for Termux
- **🌐 PXE Boot Server** - Complete DHCP and TFTP server implementation
- **🐧 Arch Linux Integration** - Automated installation and configuration
- **🎨 Kali-Like UI** - Stunning themes with Matrix, Cyberpunk, Neon Green, and Kali Dark
- **⚡ Performance Optimized** - Maximum, Balanced, Gaming, and Minimal profiles
- **🛠️ No Root Required** - Runs entirely within Termux environment
- **📊 Real-time Monitoring** - Live system status and performance metrics

### Customization Options
- **Multiple Themes**: Kali Dark, Cyberpunk, Matrix, Neon Green
- **Desktop Environments**: i3, Awesome WM, Openbox
- **Terminals**: Kitty, Alacritty, URxvt
- **Shells**: ZSH, Bash, Fish
- **Performance Profiles**: Maximum, Balanced, Gaming, Minimal

### Network Capabilities
- **Automatic Interface Detection** - Finds all network interfaces
- **IP Address Management** - Automatic IP suggestion and configuration
- **DHCP Range Configuration** - Customizable IP ranges
- **TFTP File Transfer** - Secure file serving for boot images
- **Network Monitoring** - Real-time connection status

### Arch Linux Customizations
- **Pre-configured i3** - Modern tiling window manager
- **Enhanced Shells** - ZSH with Oh-My-Zsh and plugins
- **Vim Configuration** - Programming-optimized editor setup
- **Performance Scripts** - System optimization automation
- **Kali-Style Aliases** - Familiar command shortcuts
- **Custom MOTD** - Themed welcome messages

## 🛠️ Installation

### Prerequisites
- Android device with Termux installed
- Python 3.6 or higher
- Network connection (WiFi or mobile data)
- Target PC on the same network

### Quick Installation

1. **Clone or Download the Repository**
```bash
# If you have git installed in Termux
git clone https://github.com/your-repo/termux-pxe-boot.git
cd termux-pxe-boot

# Or download and extract the zip file
```

2. **Run the Installation Script**
```bash
chmod +x install.sh
./install.sh
```

3. **Launch the Application**
```bash
chmod +x run.sh
./run.sh
```

### Manual Installation

1. **Install Python Dependencies**
```bash
pkg update && pkg upgrade
pkg install python python-dev
pkg install tkinter  # For GUI support
pip install -r requirements.txt
```

2. **Make Scripts Executable**
```bash
chmod +x termux_pxe_boot.py
chmod +x run.sh
```

3. **Run the Application**
```bash
python termux_pxe_boot.py
```

## 🎮 Usage Guide

### Starting the Application

1. **Launch**:
   ```bash
   ./run.sh
   # or
   python termux_pxe_boot.py
   ```

2. **Network Configuration**:
   - Select your network interface from the dropdown
   - Configure PXE server IP (auto-suggested)
   - Adjust DHCP range if needed

3. **Customization Settings**:
   - Choose your preferred theme
   - Select performance profile
   - Pick tool package

### Boot Process

1. **Start PXE Server**:
   - Click "START PXE SERVER" in the GUI
   - Wait for server status to show "RUNNING"
   - Note the server IP address

2. **Configure Target PC**:
   - Ensure PC is connected to same network
   - Enter BIOS/UEFI settings
   - Enable PXE boot
   - Set network boot as first priority

3. **Boot the Target**:
   - Power on the target PC
   - It will automatically detect your PXE server
   - Arch Linux installation will begin

4. **Post-Installation**:
   - System will auto-configure with selected theme
   - Performance optimizations will be applied
   - Kali-style aliases and tools will be installed

## 🎨 Themes and Customization

### Available Themes

#### Kali Dark (Default)
- **Colors**: Green on dark background
- **Style**: Professional, Kali-inspired
- **Best for**: Security professionals, general use

#### Cyberpunk
- **Colors**: Magenta/Purple neon
- **Style**: Futuristic, high-tech
- **Best for**: Gaming, programming, aesthetic appeal

#### Matrix
- **Colors**: Green matrix-style
- **Style**: Classic hacker aesthetic
- **Best for**: Retro computing, thematic appearance

#### Neon Green
- **Colors**: Bright green on black
- **Style**: High contrast, eye-catching
- **Best for**: Maximum visibility, performance monitoring

### Performance Profiles

#### Maximum Performance
- CPU governor: Performance mode
- Memory: No limits
- I/O: NOOP scheduler
- Preloading: Enabled
- Power management: Disabled

#### Balanced Performance
- CPU governor: Balanced
- Memory: 80% limit with 2GB swap
- I/O: MQ-Deadline scheduler
- Preloading: Enabled
- Battery optimization: Moderate

#### Gaming Optimized
- CPU governor: Performance
- Memory: 90% limit with 4GB swap
- I/O: NOOP scheduler
- Real-time scheduling: Enabled
- Graphics: Maximum acceleration

#### Minimal Power
- CPU governor: Powersave
- Memory: 60% limit, no swap
- I/O: BFQ scheduler
- Preloading: Disabled
- Battery optimization: Maximum

## 🔧 Configuration

### Settings File
Configuration is stored in `~/.termux_pxe_boot/config.json`:

```json
{
  "interface": "wlan0",
  "pxe_ip": "192.168.1.100",
  "ui_theme": "Kali Dark",
  "performance": "Maximum",
  "tools": "Kali Tools + Performance"
}
```

### Customization Files
- **i3 Config**: `~/.termux_pxe_boot/customizer/configs/i3/`
- **ZSH Config**: `~/.termux_pxe_boot/customizer/configs/zsh/`
- **Vim Config**: `~/.termux_pxe_boot/customizer/configs/vim/`
- **Performance Scripts**: `~/.termux_pxe_boot/optimizations/`

## 🐛 Troubleshooting

### Common Issues

#### GUI Not Starting
```bash
# Check if tkinter is installed
python -c "import tkinter"

# If not installed, install it
pkg install python-tkinter
```

#### Network Interface Not Found
```bash
# Check available interfaces
ip addr show

# Refresh interfaces in the GUI
# Click the "Refresh" button in Network Configuration
```

#### PXE Server Not Starting
1. Check if ports 67 and 69 are available
2. Ensure you're connected to a network
3. Check logs for specific error messages
4. Try restarting the application

#### Installation Fails
1. Ensure target PC is on the same network
2. Check if another DHCP server exists
3. Verify BIOS settings allow PXE boot
4. Check firewall settings

### Debug Mode
```bash
# Run with verbose logging
python termux_pxe_boot.py --debug

# Check log files
cat ~/.termux_pxe_boot/pxe_boot.log
```

## 📊 Performance Monitoring

### Built-in Monitor
Run the performance monitor after installation:
```bash
perf-monitor
```

### Key Metrics
- **CPU**: Frequency, governor, load average
- **Memory**: Usage, swap, cache pressure
- **Network**: Connection status, throughput
- **Storage**: Disk usage, I/O scheduler
- **Temperature**: CPU and system sensors

### Optimization Verification
```bash
# Check active optimizations
sysctl vm.swappiness
cat /proc/sys/vm/vfs_cache_pressure
cat /sys/kernel/mm/transparent_hugepage/enabled
```

## 🔒 Security Considerations

### Network Security
- PXE server uses standard ports (67, 69)
- No authentication required (by design)
- Only serve on trusted networks
- Consider firewall rules for production use

### Data Security
- All configurations stored locally
- No data transmitted to external servers
- Boot files served from local filesystem
- Logs contain only system information

## 🛡️ Kali Tools Integration

### Pre-installed Tools
- **Network Scanning**: Nmap, Masscan
- **Web Testing**: Nikto, Gobuster
- **Password Cracking**: Hashcat, John
- **Wireless**: Aircrack-ng suite
- **Development**: Git, Vim, Python tools

### Kali-Style Commands
```bash
# System commands
kali-update    # Update system
kali-clean     # Clean package cache
kali-install   # Install packages
kali-search    # Search packages

# Network commands
net-scan       # Network discovery
port-scan      # Port scanning
myip           # Show external IP
```

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes (if using git)
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Backup Configuration
```bash
# Export settings
cp ~/.termux_pxe_boot/config.json ~/backup_config.json

# Backup boot files
tar -czf pxe_boot_backup.tar.gz ~/.termux_pxe_boot/
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black *.py
flake8 *.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Termux Team** - For the amazing Android terminal emulator
- **Arch Linux** - For the flexible and powerful Linux distribution
- **Kali Linux** - For inspiration in security tool integration
- **Python Community** - For the excellent GUI and networking libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/termux-pxe-boot/issues)
- **Documentation**: [Wiki](https://github.com/your-repo/termux-pxe-boot/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/termux-pxe-boot/discussions)

## 📈 Roadmap

### Upcoming Features
- [ ] **Live ISO Support** - Boot live Arch Linux without installation
- [ ] **Multiple Distro Support** - Ubuntu, Fedora, Debian
- [ ] **GUI Boot Menu** - Visual boot selection interface
- [ ] **Remote Management** - Web-based administration
- [ ] **Custom Themes** - User-created theme support
- [ ] **Performance Profiling** - Automatic hardware detection
- [ ] **Network Discovery** - Automatic client detection

---

**⚡ Made with ❤️ for the Linux and Android community ⚡**

*Transform your Android device into a powerful network boot server and experience Arch Linux like never before!*
![Version](https://img.shields.io/badge/version-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.6+-blue)
![Platform](https://img.shields.io/badge/platform-Termux-orange)
![License](https://img.shields.io/badge/license-MIT-red)

**⚡ The Ultimate Termux PXE Boot Solution for Arch Linux with Kali-like UI ⚡**

A comprehensive Python-based GUI application that transforms your Android device running Termux into a powerful PXE boot server, enabling network installation of Arch Linux with a stunning Kali-inspired interface and performance optimizations.

## 🚀 Features

### Core Features
- **📱 Termux-Native GUI** - Beautiful, responsive interface designed for Termux
- **🌐 PXE Boot Server** - Complete DHCP and TFTP server implementation
- **🐧 Arch Linux Integration** - Automated installation and configuration
- **🎨 Kali-Like UI** - Stunning themes with Matrix, Cyberpunk, Neon Green, and Kali Dark
- **⚡ Performance Optimized** - Maximum, Balanced, Gaming, and Minimal profiles
- **🛠️ No Root Required** - Runs entirely within Termux environment
- **📊 Real-time Monitoring** - Live system status and performance metrics

### Customization Options
- **Multiple Themes**: Kali Dark, Cyberpunk, Matrix, Neon Green
- **Desktop Environments**: i3, Awesome WM, Openbox
- **Terminals**: Kitty, Alacritty, URxvt
- **Shells**: ZSH, Bash, Fish
- **Performance Profiles**: Maximum, Balanced, Gaming, Minimal

### Network Capabilities
- **Automatic Interface Detection** - Finds all network interfaces
- **IP Address Management** - Automatic IP suggestion and configuration
- **DHCP Range Configuration** - Customizable IP ranges
- **TFTP File Transfer** - Secure file serving for boot images
- **Network Monitoring** - Real-time connection status

### Arch Linux Customizations
- **Pre-configured i3** - Modern tiling window manager
- **Enhanced Shells** - ZSH with Oh-My-Zsh and plugins
- **Vim Configuration** - Programming-optimized editor setup
- **Performance Scripts** - System optimization automation
- **Kali-Style Aliases** - Familiar command shortcuts
- **Custom MOTD** - Themed welcome messages

## 🛠️ Installation

### Prerequisites
- Android device with Termux installed
- Python 3.6 or higher
- Network connection (WiFi or mobile data)
- Target PC on the same network

### Quick Installation

1. **Clone or Download the Repository**
```bash
# If you have git installed in Termux
git clone https://github.com/your-repo/termux-pxe-boot.git
cd termux-pxe-boot

# Or download and extract the zip file
```

2. **Run the Installation Script**
```bash
chmod +x install.sh
./install.sh
```

3. **Launch the Application**
```bash
chmod +x run.sh
./run.sh
```

### Manual Installation

1. **Install Python Dependencies**
```bash
pkg update && pkg upgrade
pkg install python python-dev
pkg install tkinter  # For GUI support
pip install -r requirements.txt
```

2. **Make Scripts Executable**
```bash
chmod +x termux_pxe_boot.py
chmod +x run.sh
```

3. **Run the Application**
```bash
python termux_pxe_boot.py
```

## 🎮 Usage Guide

### Starting the Application

1. **Launch**:
   ```bash
   ./run.sh
   # or
   python termux_pxe_boot.py
   ```

2. **Network Configuration**:
   - Select your network interface from the dropdown
   - Configure PXE server IP (auto-suggested)
   - Adjust DHCP range if needed

3. **Customization Settings**:
   - Choose your preferred theme
   - Select performance profile
   - Pick tool package

### Boot Process

1. **Start PXE Server**:
   - Click "START PXE SERVER" in the GUI
   - Wait for server status to show "RUNNING"
   - Note the server IP address

2. **Configure Target PC**:
   - Ensure PC is connected to same network
   - Enter BIOS/UEFI settings
   - Enable PXE boot
   - Set network boot as first priority

3. **Boot the Target**:
   - Power on the target PC
   - It will automatically detect your PXE server
   - Arch Linux installation will begin

4. **Post-Installation**:
   - System will auto-configure with selected theme
   - Performance optimizations will be applied
   - Kali-style aliases and tools will be installed

## 🎨 Themes and Customization

### Available Themes

#### Kali Dark (Default)
- **Colors**: Green on dark background
- **Style**: Professional, Kali-inspired
- **Best for**: Security professionals, general use

#### Cyberpunk
- **Colors**: Magenta/Purple neon
- **Style**: Futuristic, high-tech
- **Best for**: Gaming, programming, aesthetic appeal

#### Matrix
- **Colors**: Green matrix-style
- **Style**: Classic hacker aesthetic
- **Best for**: Retro computing, thematic appearance

#### Neon Green
- **Colors**: Bright green on black
- **Style**: High contrast, eye-catching
- **Best for**: Maximum visibility, performance monitoring

### Performance Profiles

#### Maximum Performance
- CPU governor: Performance mode
- Memory: No limits
- I/O: NOOP scheduler
- Preloading: Enabled
- Power management: Disabled

#### Balanced Performance
- CPU governor: Balanced
- Memory: 80% limit with 2GB swap
- I/O: MQ-Deadline scheduler
- Preloading: Enabled
- Battery optimization: Moderate

#### Gaming Optimized
- CPU governor: Performance
- Memory: 90% limit with 4GB swap
- I/O: NOOP scheduler
- Real-time scheduling: Enabled
- Graphics: Maximum acceleration

#### Minimal Power
- CPU governor: Powersave
- Memory: 60% limit, no swap
- I/O: BFQ scheduler
- Preloading: Disabled
- Battery optimization: Maximum

## 🔧 Configuration

### Settings File
Configuration is stored in `~/.termux_pxe_boot/config.json`:

```json
{
  "interface": "wlan0",
  "pxe_ip": "192.168.1.100",
  "ui_theme": "Kali Dark",
  "performance": "Maximum",
  "tools": "Kali Tools + Performance"
}
```

### Customization Files
- **i3 Config**: `~/.termux_pxe_boot/customizer/configs/i3/`
- **ZSH Config**: `~/.termux_pxe_boot/customizer/configs/zsh/`
- **Vim Config**: `~/.termux_pxe_boot/customizer/configs/vim/`
- **Performance Scripts**: `~/.termux_pxe_boot/optimizations/`

## 🐛 Troubleshooting

### Common Issues

#### GUI Not Starting
```bash
# Check if tkinter is installed
python -c "import tkinter"

# If not installed, install it
pkg install python-tkinter
```

#### Network Interface Not Found
```bash
# Check available interfaces
ip addr show

# Refresh interfaces in the GUI
# Click the "Refresh" button in Network Configuration
```

#### PXE Server Not Starting
1. Check if ports 67 and 69 are available
2. Ensure you're connected to a network
3. Check logs for specific error messages
4. Try restarting the application

#### Installation Fails
1. Ensure target PC is on the same network
2. Check if another DHCP server exists
3. Verify BIOS settings allow PXE boot
4. Check firewall settings

### Debug Mode
```bash
# Run with verbose logging
python termux_pxe_boot.py --debug

# Check log files
cat ~/.termux_pxe_boot/pxe_boot.log
```

## 📊 Performance Monitoring

### Built-in Monitor
Run the performance monitor after installation:
```bash
perf-monitor
```

### Key Metrics
- **CPU**: Frequency, governor, load average
- **Memory**: Usage, swap, cache pressure
- **Network**: Connection status, throughput
- **Storage**: Disk usage, I/O scheduler
- **Temperature**: CPU and system sensors

### Optimization Verification
```bash
# Check active optimizations
sysctl vm.swappiness
cat /proc/sys/vm/vfs_cache_pressure
cat /sys/kernel/mm/transparent_hugepage/enabled
```

## 🔒 Security Considerations

### Network Security
- PXE server uses standard ports (67, 69)
- No authentication required (by design)
- Only serve on trusted networks
- Consider firewall rules for production use

### Data Security
- All configurations stored locally
- No data transmitted to external servers
- Boot files served from local filesystem
- Logs contain only system information

## 🛡️ Kali Tools Integration

### Pre-installed Tools
- **Network Scanning**: Nmap, Masscan
- **Web Testing**: Nikto, Gobuster
- **Password Cracking**: Hashcat, John
- **Wireless**: Aircrack-ng suite
- **Development**: Git, Vim, Python tools

### Kali-Style Commands
```bash
# System commands
kali-update    # Update system
kali-clean     # Clean package cache
kali-install   # Install packages
kali-search    # Search packages

# Network commands
net-scan       # Network discovery
port-scan      # Port scanning
myip           # Show external IP
```

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes (if using git)
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Backup Configuration
```bash
# Export settings
cp ~/.termux_pxe_boot/config.json ~/backup_config.json

# Backup boot files
tar -czf pxe_boot_backup.tar.gz ~/.termux_pxe_boot/
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black *.py
flake8 *.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Termux Team** - For the amazing Android terminal emulator
- **Arch Linux** - For the flexible and powerful Linux distribution
- **Kali Linux** - For inspiration in security tool integration
- **Python Community** - For the excellent GUI and networking libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/termux-pxe-boot/issues)
- **Documentation**: [Wiki](https://github.com/your-repo/termux-pxe-boot/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/termux-pxe-boot/discussions)

## 📈 Roadmap

### Upcoming Features
- [ ] **Live ISO Support** - Boot live Arch Linux without installation
- [ ] **Multiple Distro Support** - Ubuntu, Fedora, Debian
- [ ] **GUI Boot Menu** - Visual boot selection interface
- [ ] **Remote Management** - Web-based administration
- [ ] **Custom Themes** - User-created theme support
- [ ] **Performance Profiling** - Automatic hardware detection
- [ ] **Network Discovery** - Automatic client detection

---

**⚡ Made with ❤️ for the Linux and Android community ⚡**

*Transform your Android device into a powerful network boot server and experience Arch Linux like never before!*

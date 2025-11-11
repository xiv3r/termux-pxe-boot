# Universal Network Bridge System

Enhanced network interface detection system specifically designed for mixed network scenarios, built for PC on ethernet + Phone on WiFi configurations and beyond.

## 🚀 Key Features

### 1. **Advanced Network Topology Detection**
- Detects all network interfaces with their types (ethernet, wifi, usb, virtual)
- Identifies which interfaces are on the same network segment
- Maps network paths and potential bridging requirements
- Cross-platform compatibility (Linux, Windows, macOS, Android/Termux)

### 2. **Cross-Network Interface Identification**
- Detects when phone has both WiFi and USB tethering
- Identifies bridge candidates between different network segments
- Analyzes router behavior (isolation vs. bridge mode)
- Detects multicast/broadcast reachability between interfaces

### 3. **Universal Network Bridge Creator**
- **UDP Tunnels**: Software-defined bridge using UDP tunnels without root privileges
- **WiFi Direct**: Creates direct WiFi connections bypassing router isolation
- **USB Tethering**: Leverages USB tethering for guaranteed connectivity
- **Ad-hoc Networks**: Creates temporary ad-hoc bridges
- **Software Bridges**: Uses Linux bridge tools when available

### 4. **Mixed Network PXE Configuration**
- Interface-specific DHCP responses
- Cross-network TFTP relay capabilities
- Broadcast domain extension across interfaces
- Automatic network conflict resolution

### 5. **Zero-Configuration Operation**
- Automatic detection and configuration
- Router-agnostic design
- Works in ANY network configuration
- Automatic fallback chains

## 🛠️ Installation & Usage

### Quick Start
```bash
# Run the Universal Network Bridge System
python3 UNIVERSAL_NETWORK_BRIDGE.py

# Show network topology
python3 UNIVERSAL_NETWORK_BRIDGE.py --topology

# Show PXE configuration
python3 UNIVERSAL_NETWORK_BRIDGE.py --pxe-config

# Enable debug mode
python3 UNIVERSAL_NETWORK_BRIDGE.py --debug
```

### Programmatic Usage
```python
from UNIVERSAL_NETWORK_BRIDGE import UniversalNetworkBridge

# Initialize bridge system
bridge = UniversalNetworkBridge()

# Start the system
if bridge.start():
    print("Bridge system started successfully!")
    
    # Get current topology
    topology = bridge.get_network_topology()
    print(f"Detected {topology['active_tunnels']} active tunnels")
    
    # Get PXE configuration
    pxe_config = bridge.get_pxe_server_config()
    print(f"PXE enabled on {len(pxe_config['interfaces'])} interfaces")
```

## 📋 Supported Network Scenarios

### Primary Scenarios
- **PC on Ethernet + Phone on WiFi** (same router) - ✅ Detected
- **Router Isolation** - ✅ Automatically bridges
- **USB Tethering** - ✅ Supported
- **WiFi Direct** - ✅ Supported

### Secondary Scenarios
- **VPN Networks** - ✅ Detected and handled
- **Multiple Network Adapters** - ✅ Automatic bridging
- **Ad-hoc Networks** - ✅ Support via fallback chains
- **Mixed Interface Types** - ✅ Smart routing

## 🔧 Configuration

### Configuration File (Optional)
Create `bridge_config.json`:
```json
{
  "bridge_base_port": 9000,
  "max_bridges": 4,
  "auto_bridge": true,
  "zero_config": true,
  "pxe_server_integration": true,
  "fallback_enabled": true,
  "router_agnostic": true,
  "cross_platform": true
}
```

### Command Line Options
- `--config FILE`: Load configuration from file
- `--auto-bridge`: Enable automatic bridge creation
- `--debug`: Enable debug logging
- `--pxe-config`: Display PXE configuration
- `--topology`: Display network topology

## 🏗️ Architecture

### Core Components

1. **NetworkManager**: Enhanced network interface detection
2. **PXEServer**: Integrated PXE boot server
3. **Logger**: Comprehensive logging system
4. **BridgeSystem**: Universal bridge creation and management

### Data Structures

- **NetworkInterface**: Enhanced interface representation
- **NetworkSegment**: Network topology mapping
- **BridgeEndpoint**: UDP tunnel endpoints
- **Configuration**: System configuration management

### Bridge Creation Methods

1. **UDP Tunnel Bridge** (Primary)
   - Cross-platform compatibility
   - No root privileges required
   - Automatic tunnel management

2. **WiFi Direct Bridge** (Primary for mobile)
   - Direct device-to-device connection
   - Bypasses router isolation
   - Platform-specific implementation

3. **USB Tethering Bridge** (Fallback)
   - Reliable when available
   - USB-based connection
   - Automatic detection

4. **Ad-hoc Bridge** (Legacy support)
   - Traditional wireless bridging
   - Compatible with older devices
   - Platform-dependent

5. **Software Bridge** (Linux only)
   - Native Linux bridge tools
   - High performance
   - Requires elevated privileges

## 🔍 Detection Capabilities

### Network Topology Detection
- Interface types: ethernet, wireless, usb, virtual, loopback
- Network segments and gateway detection
- Router isolation level analysis
- Cross-segment connectivity testing

### Mixed Scenario Detection
- PC-on-ethernet + Phone-on-WiFi patterns
- USB tethering scenarios
- WiFi Direct configurations
- VPN and virtual interface scenarios

### Bridge Candidate Analysis
- Interface capabilities assessment
- PXE boot compatibility
- Bridging support detection
- Performance scoring system

## 🔒 Security Features

- **No Root Required**: Runs without elevated privileges
- **Isolated Tunnels**: UDP tunnels with unique IDs
- **Router Agnostic**: Works regardless of router configuration
- **Fallback Chains**: Multiple connection methods for reliability

## 🚀 Performance Features

- **Parallel Interface Analysis**: Concurrent detection for speed
- **Intelligent Caching**: Reduces redundant network operations
- **Smart Monitoring**: Automatic health checks and cleanup
- **Resource Management**: Efficient thread and socket handling

## 📊 Monitoring & Logging

- **Comprehensive Logging**: All operations logged with timestamps
- **Health Monitoring**: Bridge health and connectivity monitoring
- **Automatic Cleanup**: Stale connection cleanup
- **Performance Metrics**: Interface scoring and optimization

## 🔄 Fallback Chain System

The system implements a comprehensive fallback chain:

1. **UDP Tunnel** → Cross-platform, no root required
2. **WiFi Direct** → Direct device connection
3. **USB Tethering** → Reliable USB connection
4. **Ad-hoc Bridge** → Legacy wireless bridging
5. **Software Bridge** → Native Linux bridging

Each method is tried in order until successful.

## 🎯 Integration with Existing Systems

### PXE Server Integration
- Automatic interface-specific PXE configuration
- Cross-network TFTP relay capabilities
- DHCP range management per interface
- Broadcast domain extension

### Network Manager Integration
- Extends existing NetworkManager capabilities
- Maintains compatibility with termux_pxe_boot.py
- Enhanced interface detection and analysis

## 🐛 Troubleshooting

### Common Issues

1. **No Interfaces Detected**
   ```bash
   # Check interface permissions
   ip link show
   # Ensure interfaces are up
   sudo ip link set eth0 up
   ```

2. **Bridge Creation Failed**
   ```bash
   # Enable debug mode
   python3 UNIVERSAL_NETWORK_BRIDGE.py --debug
   # Check specific error messages
   ```

3. **PXE Integration Issues**
   ```bash
   # Verify PXE configuration
   python3 UNIVERSAL_NETWORK_BRIDGE.py --pxe-config
   # Check existing PXE server
   ```

### Debug Mode
```bash
python3 UNIVERSAL_NETWORK_BRIDGE.py --debug
```

### Log Analysis
- Logs are timestamped and categorized
- Debug level for detailed troubleshooting
- Error level for critical issues only

## 📈 Performance Optimization

### For Maximum Performance
```python
bridge = UniversalNetworkBridge()
bridge.config['performance_mode'] = True
bridge.optimize_for_performance()
```

### For Maximum Compatibility
```python
bridge = UniversalNetworkBridge()
bridge.config['performance_mode'] = False
bridge.optimize_for_compatibility()
```

## 🔮 Advanced Usage

### Manual Bridge Creation
```python
# Create bridge between specific interfaces
bridge.create_bridge('eth0', 'wlan0')

# Get topology for external processing
topology = bridge.get_network_topology()

# Configure PXE for specific network
pxe_config = bridge.get_pxe_server_config()
```

### Custom Configuration
```python
# Create with custom config file
bridge = UniversalNetworkBridge('custom_config.json')

# Modify configuration at runtime
bridge.config['bridge_base_port'] = 8080
bridge.config['max_bridges'] = 8
```

## 📝 Requirements

- Python 3.7+
- Network interfaces (any type)
- Operating System: Linux, Windows, macOS, Android (Termux)

### Optional Dependencies
- `psutil`: For enhanced interface detection
- `iw`: For wireless interface analysis (Linux)
- `ip`: For network interface management (Linux/Unix)

## 🤝 Contributing

The Universal Network Bridge System is designed to be extensible:

1. **Add New Bridge Types**: Implement additional bridge creation methods
2. **Platform Support**: Add platform-specific optimizations
3. **Enhanced Detection**: Improve topology detection algorithms
4. **Performance**: Optimize detection and monitoring speed

## 📄 License

This system integrates with the existing termux_pxe_boot project infrastructure and follows the same licensing terms.

## 🎉 Success Stories

The Universal Network Bridge System has been validated to:

✅ **Detect Complex Network Topologies**
- Successfully identifies mixed ethernet/wireless configurations
- Maps network segments and isolation levels
- Detects VPN and virtual interface scenarios

✅ **Handle Router Isolation**
- Automatically bridges isolated network segments
- Provides multiple fallback methods
- Works regardless of router configuration

✅ **Enable PXE Boot Across Networks**
- Interface-specific DHCP configuration
- Cross-network TFTP relay capabilities
- Broadcast domain extension

✅ **Zero-Configuration Operation**
- Automatic detection and bridge creation
- Smart defaults for all scenarios
- Router-agnostic design

The system is ready for deployment and production use in mixed network environments!
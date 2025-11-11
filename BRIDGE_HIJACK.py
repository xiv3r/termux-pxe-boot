#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE PXE E53 FIX - WIFI-TO-ETHERNET BRIDGE HIJACKER
==============================================================

This script creates a software bridge that hijacks ethernet traffic using promiscuous 
mode to capture all ethernet traffic and inject DHCP responses directly into ethernet 
frames, bypassing router filtering entirely.

REQUIREMENTS:
- root/sudo privileges
- Both WiFi and ethernet interfaces available
- bridge-utils (apt install bridge-utils)
- scapy for packet manipulation

USAGE: sudo python3 BRIDGE_HIJACK.py <wifi_interface> <eth_interface> <boot_filename>
"""

import sys
import os
import socket
import subprocess
import threading
import time
import logging
import struct
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from scapy.all import *
    from scapy.layers.dhcp import DHCP, BOOTP
    from scapy.layers.l2 import ARP, Ether, Bridge
except ImportError:
    print("ERROR: scapy not installed. Install with: pip install scapy")
    sys.exit(1)

class BridgeHijacker:
    """Ultra-aggressive bridge hijacker that intercepts ethernet traffic."""
    
    def __init__(self, wifi_interface, eth_interface, boot_filename="pxelinux.0"):
        self.wifi_interface = wifi_interface
        self.eth_interface = eth_interface
        self.boot_filename = boot_filename
        self.bridge_name = "pxe_bridge"
        self.attacker_mac = self.get_interface_mac(wifi_interface)
        self.server_ip = "192.168.1.100"
        self.yiaddr = "192.168.1.150"
        self.subnet_mask = "255.255.255.0"
        self.router = "192.168.1.1"
        self.dns_servers = ["8.8.8.8", "8.8.4.4"]
        self.broadcast = "192.168.1.255"
        self.hijacking_active = False
        
        logger.info(f"🌉 Bridge Hijacker initialized")
        logger.info(f"📶 WiFi Interface: {wifi_interface}")
        logger.info(f"🔌 Ethernet Interface: {eth_interface}")
        logger.info(f"🎭 Attacker MAC: {self.attacker_mac}")
        logger.info(f"🔧 Boot filename: {boot_filename}")

    def get_interface_mac(self, interface):
        """Get MAC address of network interface."""
        try:
            result = subprocess.check_output(['ip', 'link', 'show', interface])
            lines = result.decode().split('\n')
            for line in lines:
                if 'link/ether' in line:
                    return line.split('link/ether')[1].split()[0]
        except:
            return "00:11:22:33:44:55"
        return "00:11:22:33:44:55"

    def check_interface_requirements(self):
        """Check if interfaces meet requirements."""
        logger.info(f"🔍 Checking interface requirements...")
        
        # Check if interfaces exist
        interfaces = subprocess.check_output(['ip', 'link', 'show']).decode()
        if self.wifi_interface not in interfaces:
            logger.error(f"❌ WiFi interface {self.wifi_interface} not found")
            return False
        
        if self.eth_interface not in interfaces:
            logger.error(f"❌ Ethernet interface {self.eth_interface} not found")
            return False
        
        # Check if interfaces are up
        for interface in [self.wifi_interface, self.eth_interface]:
            try:
                result = subprocess.check_output(['ip', 'link', 'show', interface])
                if 'UP' not in result.decode():
                    logger.info(f"⚡ Bringing up interface {interface}")
                    subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
            except subprocess.CalledProcessError:
                pass
        
        logger.info(f"✅ Interface requirements met")
        return True

    def create_software_bridge(self):
        """Create software bridge between WiFi and ethernet interfaces."""
        logger.info(f"🌉 Creating software bridge: {self.bridge_name}")
        
        try:
            # Remove existing bridge if it exists
            subprocess.run(['ip', 'link', 'del', self.bridge_name], stderr=subprocess.DEVNULL)
            
            # Create bridge
            subprocess.run(['ip', 'link', 'add', 'name', self.bridge_name, 'type', 'bridge'], check=True)
            
            # Add interfaces to bridge
            subprocess.run(['ip', 'link', 'set', self.wifi_interface, 'master', self.bridge_name], check=True)
            subprocess.run(['ip', 'link', 'set', self.eth_interface, 'master', self.bridge_name], check=True)
            
            # Bring up bridge
            subprocess.run(['ip', 'link', 'set', self.bridge_name, 'up'], check=True)
            
            logger.info(f"✅ Software bridge created successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to create bridge: {e}")
            return False

    def enable_promiscuous_mode(self, interface):
        """Enable promiscuous mode on interface."""
        try:
            # Set interface to promiscuous mode
            subprocess.run(['ip', 'link', 'set', interface, 'promisc', 'on'], check=True)
            logger.info(f"📡 Promiscuous mode enabled on {interface}")
            return True
        except subprocess.CalledProcessError:
            logger.warning(f"⚠️  Could not enable promiscuous mode on {interface}")
            return False

    def setup_bridge_forwarding(self):
        """Setup bridge forwarding to hijack traffic."""
        logger.info(f"🔄 Setting up bridge forwarding...")
        
        try:
            # Enable IP forwarding
            subprocess.run(['sysctl', '-w', 'net.ipv4.ip_forward=1'], check=True)
            
            # Setup iptables rules to redirect DHCP traffic
            subprocess.run(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', self.bridge_name, '-j', 'MASQUERADE'], check=True)
            subprocess.run(['iptables', '-A', 'FORWARD', '-i', self.bridge_name, '-j', 'ACCEPT'], check=True)
            subprocess.run(['iptables', '-A', 'FORWARD', '-o', self.bridge_name, '-j', 'ACCEPT'], check=True)
            
            logger.info(f"✅ Bridge forwarding configured")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"⚠️  Bridge forwarding setup warning: {e}")
            return False

    def hijack_dhcp_requests(self, packet):
        """Hijack DHCP requests and inject malicious responses."""
        if not packet.haslayer(BOOTP) or not packet.haslayer(DHCP):
            return
        
        dhcp_layer = packet[DHCP]
        bootp_layer = packet[BOOTP]
        
        # Detect DHCP Discover or Request
        if b'\x01\x03\x06' in dhcp_layer.options:  # DHCP Discover
            target_mac = packet[Ether].src
            logger.info(f"🔥 DHCP DISCOVER hijacked from {target_mac}")
            self.inject_hijacked_dhcp_response(target_mac, bootp_layer.xid)
            
        elif b'\x01\x01\x06' in dhcp_layer.options:  # DHCP Request
            target_mac = packet[Ether].src
            logger.info(f"🔥 DHCP REQUEST hijacked from {target_mac}")
            self.inject_hijacked_dhcp_response(target_mac, bootp_layer.xid)

    def inject_hijacked_dhcp_response(self, target_mac, transaction_id):
        """Inject hijacked DHCP response."""
        try:
            # Create DHCP response
            dhcp_response = IP(src=self.server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(
                op=2,
                xid=transaction_id,
                yiaddr=self.yiaddr,
                siaddr=self.server_ip,
                chaddr=target_mac.replace(':', '').encode()
            )/DHCP(
                options=[
                    ("message-type", "offer"),
                    ("server_id", self.server_ip),
                    ("subnet_mask", self.subnet_mask),
                    ("router", self.router),
                    ("dns_server", self.dns_servers),
                    ("broadcast", self.broadcast),
                    ("lease_time", 86400),
                    ("boot_filename", self.boot_filename),
                    ("end", "")
                ]
            )
            
            # Send via bridge
            sendp(Ether(dst=target_mac, src=self.attacker_mac)/dhcp_response, 
                  iface=self.bridge_name, verbose=0)
            
            # Also broadcast
            sendp(Ether(dst="ff:ff:ff:ff:ff:ff", src=self.attacker_mac)/dhcp_response,
                  iface=self.bridge_name, verbose=0)
            
            logger.info(f"💉 Hijacked DHCP response injected: {self.yiaddr} -> {self.boot_filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to inject hijacked DHCP response: {e}")

    def start_bridge_hijacking(self):
        """Start bridge hijacking operation."""
        logger.info(f"🚀 Starting BRIDGE HIJACKING OPERATION")
        logger.info(f"🎯 Method: Software Bridge + Traffic Hijacking")
        logger.info(f"🌉 WiFi: {self.wifi_interface} → Ethernet: {self.eth_interface}")
        
        # Check if running as root
        if os.geteuid() != 0:
            logger.error("❌ This script must be run as root (sudo)")
            return False
        
        # Check interface requirements
        if not self.check_interface_requirements():
            return False
        
        self.hijacking_active = True
        
        try:
            # Create software bridge
            if not self.create_software_bridge():
                return False
            
            # Enable promiscuous modes
            self.enable_promiscuous_mode(self.wifi_interface)
            self.enable_promiscuous_mode(self.eth_interface)
            
            # Setup bridge forwarding
            self.setup_bridge_forwarding()
            
            logger.info(f"🔥 Bridge hijacking active - Capturing all ethernet traffic")
            
            # Start packet capture on bridge
            sniff(iface=self.bridge_name, 
                  filter="udp and port 67 and port 68",
                  prn=self.hijack_dhcp_requests,
                  store=0)
            
        except KeyboardInterrupt:
            logger.info(f"🛑 Bridge hijacking stopped by user")
        except Exception as e:
            logger.error(f"❌ Bridge hijacking error: {e}")
        finally:
            self.hijacking_active = False
            self.cleanup_bridge()
        
        return True

    def cleanup_bridge(self):
        """Clean up bridge and restore interfaces."""
        logger.info(f"🧹 Cleaning up bridge...")
        
        try:
            # Remove bridge
            subprocess.run(['ip', 'link', 'del', self.bridge_name], stderr=subprocess.DEVNULL)
            
            # Remove iptables rules
            subprocess.run(['iptables', '-t', 'nat', '-D', 'POSTROUTING', '-o', self.bridge_name, '-j', 'MASQUERADE'], stderr=subprocess.DEVNULL)
            subprocess.run(['iptables', '-D', 'FORWARD', '-i', self.bridge_name, '-j', 'ACCEPT'], stderr=subprocess.DEVNULL)
            subprocess.run(['iptables', '-D', 'FORWARD', '-o', self.bridge_name, '-j', 'ACCEPT'], stderr=subprocess.DEVNULL)
            
            logger.info(f"✅ Bridge cleanup completed")
            
        except Exception as e:
            logger.warning(f"⚠️  Bridge cleanup warning: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: sudo python3 BRIDGE_HIJACK.py <wifi_interface> <eth_interface> <boot_filename>")
        print("Example: sudo python3 BRIDGE_HIJACK.py wlan0 eth0 pxelinux.0")
        sys.exit(1)
    
    wifi_interface = sys.argv[1]
    eth_interface = sys.argv[2]
    boot_filename = sys.argv[3]
    
    try:
        hijacker = BridgeHijacker(wifi_interface, eth_interface, boot_filename)
        hijacker.start_bridge_hijacking()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
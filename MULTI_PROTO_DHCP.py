#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE PXE E53 FIX - MULTI-PROTOCOL DHCP INJECTOR
==========================================================

This script sends DHCP responses via multiple protocols simultaneously, using UDP port 67 
directly with raw sockets, broadcast DHCP responses using ethernet broadcast, and 
including boot filename in ALL possible DHCP options.

REQUIREMENTS:
- root/sudo privileges for raw sockets
- scapy for packet manipulation
- Network interface access

USAGE: sudo python3 MULTI_PROTO_DHCP.py <interface> <boot_filename>
"""

import sys
import os
import socket
import struct
import time
import threading
import logging
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from scapy.all import *
    from scapy.layers.dhcp import DHCP, BOOTP
    from scapy.layers.l2 import Ether, ARP
    from scapy.layers.inet import IP, UDP
except ImportError:
    print("ERROR: scapy not installed. Install with: pip install scapy")
    sys.exit(1)

class MultiProtocolDHCPInjector:
    """Ultra-aggressive multi-protocol DHCP injector."""
    
    def __init__(self, interface="eth0", boot_filename="pxelinux.0"):
        self.interface = interface
        self.boot_filename = boot_filename
        self.attacker_mac = self.get_interface_mac(interface)
        self.attacker_ip = self.get_interface_ip(interface)
        self.server_ip = "192.168.1.100"
        self.yiaddr = "192.168.1.150"
        self.subnet_mask = "255.255.255.0"
        self.router = "192.168.1.1"
        self.dns_servers = ["8.8.8.8", "8.8.4.4"]
        self.broadcast = "192.168.1.255"
        self.lease_time = 86400  # 24 hours
        self.transaction_id = 0x12345678
        
        # Multiple injection methods
        self.injection_methods = []
        
        logger.info(f"🎯 Multi-Protocol DHCP Injector initialized")
        logger.info(f"🌐 Interface: {interface}")
        logger.info(f"🎭 Attacker MAC: {self.attacker_mac}")
        logger.info(f"🎭 Attacker IP: {self.attacker_ip}")
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

    def get_interface_ip(self, interface):
        """Get IP address of network interface."""
        try:
            result = subprocess.check_output(['ip', '-4', 'addr', 'show', interface])
            lines = result.decode().split('\n')
            for line in lines:
                if 'inet ' in line and 'scope global' in line:
                    return line.strip().split()[1].split('/')[0]
        except:
            return "192.168.1.100"
        return "192.168.1.100"

    def create_comprehensive_dhcp_options(self):
        """Create DHCP options with boot filename in ALL possible locations."""
        options = []
        
        # Primary DHCP options
        options.extend([("message-type", "offer")])                    # DHCP Message Type = Offer
        options.extend([("server_id", self.server_ip)])                # Server Identifier
        options.extend([("subnet_mask", self.subnet_mask)])            # Subnet Mask
        options.extend([("router", self.router)])                      # Router/Gateway
        options.extend([("dns_server", self.dns_servers)])            # DNS Servers
        options.extend([("broadcast", self.broadcast)])                # Broadcast Address
        options.extend([("lease_time", self.lease_time)])              # Lease Time
        
        # Boot filename in ALL possible DHCP options
        options.extend([("boot_filename", self.boot_filename)])        # Option 67: Bootfile Name
        options.extend([67, len(self.boot_filename), self.boot_filename])  # Alternative format
        
        # Additional boot-related options
        options.extend([("bootfile", self.boot_filename)])             # Option 66: TFTP Server Name
        options.extend([66, len(self.boot_filename), self.boot_filename.encode()])  # Alternative
        
        # PXE-specific options
        options.extend([("pxe_bootfile", self.boot_filename)])         # Custom PXE option
        options.extend([("pxe_filename", self.boot_filename)])         # Alternative PXE option
        
        # Legacy boot options
        options.extend([("filename", self.boot_filename)])             # Legacy filename option
        options.extend([("root_path", f"/tftpboot/{self.boot_filename}")])  # Root path with boot file
        options.extend([("boot_path", f"/pxe/{self.boot_filename}")])  # Boot path option
        
        # Additional PXE options with filename
        options.extend([("vendor_class", f"PXEClient:Arch:{self.boot_filename}")])
        options.extend([("vendor_specific", f"bootfile={self.boot_filename}".encode())])
        
        # Network configuration with embedded boot filename
        options.extend([("network_config", f"netboot:{self.boot_filename}".encode())])
        
        # Multiple format of boot filename for compatibility
        options.extend([
            ("bootfile1", self.boot_filename),     # Alternative boot file 1
            ("bootfile2", self.boot_filename),     # Alternative boot file 2  
            ("bootfile3", self.boot_filename),     # Alternative boot file 3
            ("pxe_file", self.boot_filename),      # PXE-specific filename
        ])
        
        options.extend([("end", "")])              # End options marker
        
        return options

    def method_1_udp_broadcast(self):
        """Method 1: UDP broadcast DHCP injection."""
        logger.info(f"📡 Method 1: UDP Broadcast DHCP Injection")
        
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(5)
            
            # Create DHCP packet with scapy
            dhcp_packet = IP(src=self.server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(
                op=2,
                xid=self.transaction_id,
                yiaddr=self.yiaddr,
                siaddr=self.server_ip,
                chaddr=self.attacker_mac.replace(':', '').encode()
            )/DHCP(
                options=self.create_comprehensive_dhcp_options()
            )
            
            # Convert to bytes and send
            raw_packet = bytes(dhcp_packet)
            sock.sendto(raw_packet, ("255.255.255.255", 68))
            
            logger.info(f"✅ UDP Broadcast DHCP packet sent")
            sock.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ UDP Broadcast failed: {e}")
            return False

    def method_2_ethernet_broadcast(self):
        """Method 2: Ethernet broadcast DHCP injection."""
        logger.info(f"🔌 Method 2: Ethernet Broadcast DHCP Injection")
        
        try:
            # Create ethernet broadcast DHCP packet
            eth_frame = Ether(
                dst="ff:ff:ff:ff:ff:ff",  # Broadcast MAC
                src=self.attacker_mac,
                type=0x0800  # IPv4
            )/IP(src=self.server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(
                op=2,
                xid=self.transaction_id + 1,
                yiaddr=self.yiaddr,
                siaddr=self.server_ip,
                chaddr=b'\x00' * 16  # Empty MAC for broadcast
            )/DHCP(
                options=self.create_comprehensive_dhcp_options()
            )
            
            # Send via scapy
            sendp(eth_frame, iface=self.interface, verbose=0)
            
            logger.info(f"✅ Ethernet Broadcast DHCP packet sent")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ethernet Broadcast failed: {e}")
            return False

    def method_3_unicast_injection(self):
        """Method 3: Unicast DHCP injection to specific targets."""
        logger.info(f"🎯 Method 3: Unicast DHCP Injection")
        
        try:
            # Scan for active MAC addresses in network
            target_macs = self.scan_network_macs()
            
            for mac in target_macs:
                try:
                    # Create unicast DHCP packet
                    unicast_frame = Ether(
                        dst=mac,
                        src=self.attacker_mac,
                        type=0x0800
                    )/IP(src=self.server_ip, dst=self.yiaddr)/UDP(sport=67, dport=68)/BOOTP(
                        op=2,
                        xid=self.transaction_id + 2,
                        yiaddr=self.yiaddr,
                        siaddr=self.server_ip,
                        chaddr=mac.replace(':', '').encode()
                    )/DHCP(
                        options=self.create_comprehensive_dhcp_options()
                    )
                    
                    sendp(unicast_frame, iface=self.interface, verbose=0)
                    logger.info(f"💉 Unicast DHCP packet sent to {mac}")
                    
                except Exception as e:
                    logger.warning(f"⚠️  Unicast failed for {mac}: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Unicast injection failed: {e}")
            return False

    def method_4_raw_socket_injection(self):
        """Method 4: Raw socket DHCP injection."""
        logger.info(f"⚡ Method 4: Raw Socket DHCP Injection")
        
        try:
            # Create raw socket
            raw_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
            raw_sock.bind((self.interface, 0))
            
            # Create manual DHCP packet
            dhcp_options = b''.join([
                bytes([53, 1, 2]) +           # Message Type = Offer
                bytes([54, 4]) +              # Server Identifier
                socket.inet_aton(self.server_ip) +
                bytes([51, 4]) +              # Lease Time
                struct.pack('!I', self.lease_time) +
                bytes([1, 4]) +               # Subnet Mask
                socket.inet_aton(self.subnet_mask) +
                bytes([3, 4]) +               # Router
                socket.inet_aton(self.router) +
                bytes([67]) + bytes([len(self.boot_filename)]) + self.boot_filename.encode() +
                bytes([255])                  # End Option
            ])
            
            # Create full ethernet frame manually
            eth_header = bytes.fromhex("ffffffffffff") + bytes.fromhex(self.attacker_mac.replace(':', ''))
            eth_header += struct.pack('!H', 0x0800)  # IPv4
            
            # IP header
            ip_header = self.create_ip_header_manual(len(dhcp_options) + 8)  # +8 for UDP
            # UDP header
            udp_header = struct.pack('!HHHH', 67, 68, len(dhcp_options) + 8, 0)
            
            # BOOTP header
            bootp_header = struct.pack('!BLLBBBB', 2, 2, self.transaction_id + 3, 0, 0)  # Reply, Broadcast
            bootp_header += socket.inet_aton(self.yiaddr) + socket.inet_aton(self.server_ip)
            bootp_header += socket.inet_aton("0.0.0.0")  # Gateway
            bootp_header += b'\x00' * 64  # Client hardware address
            bootp_header += b'\x00' * 128  # Server hostname
            bootp_header += b'\x00' * 312  # Bootstrap file
            bootp_header += struct.pack('L', 0x63825363)  # Magic cookie
            
            # Complete packet
            full_packet = eth_header + ip_header + udp_header + bootp_header + dhcp_options
            
            # Send via raw socket
            raw_sock.send(full_packet)
            
            logger.info(f"✅ Raw Socket DHCP packet sent")
            raw_sock.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Raw Socket injection failed: {e}")
            return False

    def create_ip_header_manual(self, payload_length):
        """Create manual IP header for raw socket."""
        version_ihl = 0x45
        tos = 0
        total_length = 20 + 8 + payload_length  # IP + UDP + DHCP
        identification = 0x1234
        flags_fragment = 0
        ttl = 64
        protocol = 17  # UDP
        checksum = 0
        src_ip = socket.inet_aton(self.server_ip)
        dest_ip = socket.inet_aton("255.255.255.255")
        
        header = struct.pack('!BBHHHBBH4s4s', version_ihl, tos, total_length,
                           identification, flags_fragment, ttl, protocol,
                           checksum, src_ip, dest_ip)
        
        # Calculate checksum
        checksum = sum(struct.unpack('!8H', header))
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
        checksum = ~checksum & 0xFFFF
        
        return struct.pack('!BBHHHBBH4s4s', version_ihl, tos, total_length,
                         identification, flags_fragment, ttl, protocol,
                         checksum, src_ip, dest_ip)

    def scan_network_macs(self):
        """Scan network for active MAC addresses."""
        target_macs = []
        
        try:
            # Use ARP scan to find active hosts
            result = subprocess.check_output(['arp', '-a'], stderr=subprocess.DEVNULL)
            lines = result.decode().split('\n')
            
            for line in lines:
                if 'ether' in line and not 'incomplete' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        mac = parts[3]
                        if mac and len(mac) == 17:  # Valid MAC format
                            target_macs.append(mac)
            
            logger.info(f"🔍 Found {len(target_macs)} active MAC addresses")
            
        except Exception as e:
            logger.warning(f"⚠️  MAC scan failed: {e}")
            # Add common target MACs as fallback
            target_macs = ["aa:bb:cc:dd:ee:ff", "11:22:33:44:55:66"]
        
        return target_macs

    def continuous_multi_proto_injection(self):
        """Continuously inject DHCP packets via multiple protocols."""
        logger.info(f"🚀 Starting CONTINUOUS MULTI-PROTOCOL DHCP INJECTION")
        logger.info(f"🎯 Methods: UDP + Ethernet + Unicast + Raw Socket")
        logger.info(f"🔧 Boot filename in ALL options: {self.boot_filename}")
        
        # Check if running as root
        if os.geteuid() != 0:
            logger.error("❌ This script must be run as root (sudo)")
            return False
        
        try:
            injection_count = 0
            while True:
                injection_count += 1
                logger.info(f"🔥 Injection cycle {injection_count}")
                
                # Method 1: UDP Broadcast
                if self.method_1_udp_broadcast():
                    self.injection_methods.append("UDP_Broadcast")
                
                time.sleep(0.1)
                
                # Method 2: Ethernet Broadcast  
                if self.method_2_ethernet_broadcast():
                    self.injection_methods.append("Ethernet_Broadcast")
                
                time.sleep(0.1)
                
                # Method 3: Unicast Injection
                if self.method_3_unicast_injection():
                    self.injection_methods.append("Unicast_Injection")
                
                time.sleep(0.1)
                
                # Method 4: Raw Socket
                if self.method_4_raw_socket_injection():
                    self.injection_methods.append("Raw_Socket")
                
                logger.info(f"✅ Multi-protocol injection cycle {injection_count} completed")
                logger.info(f"📊 Active methods: {len(set(self.injection_methods[-4:]))}/4")
                
                # Wait before next cycle
                time.sleep(3)
                
        except KeyboardInterrupt:
            logger.info(f"🛑 Multi-protocol injection stopped by user")
        except Exception as e:
            logger.error(f"❌ Multi-protocol injection error: {e}")
        
        return True

def main():
    if len(sys.argv) != 3:
        print("Usage: sudo python3 MULTI_PROTO_DHCP.py <interface> <boot_filename>")
        print("Example: sudo python3 MULTI_PROTO_DHCP.py eth0 pxelinux.0")
        sys.exit(1)
    
    interface = sys.argv[1]
    boot_filename = sys.argv[2]
    
    try:
        injector = MultiProtocolDHCPInjector(interface, boot_filename)
        injector.continuous_multi_proto_injection()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
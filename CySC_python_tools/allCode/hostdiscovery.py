import ipaddress
from scapy.all import *
from colorama import init, Fore
from colorama import Fore, Style

init(autoreset=True)  # Renklerin otomatik olarak sıfırlanmasını sağlar

def validate_ip_range(ip_range):
    try:
        # IP aralığını doğrudan kontrol et
        ip, mask = ip_range.split("/")
        network = ipaddress.IPv4Network(ip_range, strict=False)
        
        # Maskenin uygun bir değer olup olmadığını kontrol et
        if int(mask) < 0 or int(mask) > 32:
            return False
        
        return True
        
    except ValueError:
        return False

def get_user_input():
    while True:
        try:
            ip_range = input("[+]: İp aralığınızı giriniz: ")
            if not ip_range:
                print(Fore.RED +"İp aralığı giriniz\nÖrnek: 10.100.0.1/24")
                continue
            
            if validate_ip_range(ip_range):
                return ip_range
            else:
                print(Fore.RED +"Geçersiz IP aralığı. Lütfen geçerli bir IP aralığı girin.")
                
        except KeyboardInterrupt:
            print("\nProgramdan çıkılıyor...")
            exit()

def sending_packet(ip_range):
    arp_packet = ARP(pdst=ip_range)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = ether_frame / arp_packet

    answered_list, unanswered_list = srp(combined_packet, timeout=1, verbose=False)
    
    if not answered_list:
        print(Fore.RED + "Cevap alınamadı Please İp adresini kontrol edin.")
        return False
    else:
        print(f"{' IP ADDRESS':<17}{' MAC ADDRESS':<20}")
        print("=" * 35)
        for cevaplanan in answered_list:
            print(" ",f"{cevaplanan[1].psrc:<17}{cevaplanan[1].src:<20}")
        print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
        return True

def main():
    while True:
        ip_range = get_user_input()
        if sending_packet(ip_range):
            break

if __name__ == "__main__":
    main()

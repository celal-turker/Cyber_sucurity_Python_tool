import re
import random
import subprocess
import sys
from colorama import Fore, init

# Colorama'nın başlatılması
init(autoreset=True)

def get_user_inputs():
    while True:
        print("[1] Manuel değiştirme:")
        print("[2] Rastgele değiştirme:")
        
        choice = input("Seçiminiz: ")
        if choice not in ['1', '2']:
            print(Fore.RED + "Lütfen 1 veya 2 girin.")
            continue

        interface = input("Lütfen arayüzü girin (interface): ")
        if not interface:
            print(Fore.RED + "Lütfen bir arayüz adı girin.")
            continue
        elif not is_valid_interface(interface):
            print(Fore.RED + "Geçersiz arayüz adı. Lütfen doğru bir arayüz adı girin.")
            continue

        mac_address = None
        if choice == '1':
            mac_address = input("Yeni MAC adresini girin: ")
            if not is_valid_mac(mac_address):
                print(Fore.RED + "Geçersiz MAC adresi. Lütfen doğru bir MAC adresi girin.")
                continue

        return interface, choice, mac_address

def is_valid_interface(interface):
    interfaces = subprocess.run(["ifconfig", "-s"], capture_output=True, text=True).stdout
    return interface in interfaces.split()[1:]

def is_valid_mac(mac_address):
    return re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac_address)

def generate_random_mac():
    mac = [0x00, 0x50, 0x56]  # İlk 3 octet sabit olarak belirlendi
    
    # Rastgele olarak son 3 octet oluşturuluyor
    for _ in range(3):
        mac.append(random.randint(0x00, 0xff))
    
    # MAC adresi formatına uygun hale getirme
    mac_address = ':'.join(map(lambda x: f"{x:02x}", mac))
    return mac_address

def get_old_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)
    return old_mac

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def print_macs(interface, old_mac):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)
    print(Fore.CYAN + "MAC adresi değiştirildi")
    if old_mac != new_mac:
        print(Fore.YELLOW + "Old MAC:", old_mac)
        print(Fore.YELLOW + "New MAC:", new_mac)
    else:
        print(Fore.YELLOW + "MAC adresi değiştirilemedi")

def main():
    try:
        while True:
            interface, choice, mac_address = get_user_inputs()
            
            if choice == '2':
                random_mac = generate_random_mac()
                old_mac = get_old_mac(interface)
                change_mac(interface, random_mac)
                print_macs(interface, old_mac)
            elif choice == '1' and mac_address:
                old_mac = get_old_mac(interface)
                change_mac(interface, mac_address)
                print_macs(interface, old_mac)
            else:
                print(Fore.RED + "Geçersiz seçenek, lütfen 1 veya 2 girin.")
    
    except KeyboardInterrupt:
        print(Fore.RED + "Program kapatıldı.")
        sys.exit(1)

if __name__ == "__main__":
    main()

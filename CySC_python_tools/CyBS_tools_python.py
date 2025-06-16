from colorama import Fore, Style
import sys
import time

# Hoş Geldin ASCII sanatı
welcome_ascii = """
 _   _              ____      _     _ _       
| | | | ___  ___   / ___| ___| | __| (_)_ __  
| |_| |/ _ \/ __| | |  _ / _ \ |/ _` | | '_ \ 
|  _  | (_) \__ \ | |_| |  __/ | (_| | | | | |
|_| |_|\___/|___/  \____|\___|_|\__,_|_|_| |_|
 
"""
from colorama import Fore, Back, Style

def print_custom_boxed_text(text):
    text_lines = text.split("\n")
    max_length = max(len(line) for line in text_lines)
    print("╔" + "═" * (max_length + 2) + "╗")
    for line in text_lines:
        print("║ " + Fore.GREEN + line.center(max_length) + Style.RESET_ALL + " ║")
    print("╚" + "═" * (max_length + 2) + "╝")

welcome_message = """
Bu araç, Bilgisayar Mühendisliği bitirme çalışması kapsamında geliştirilmiştir. 

Herhangi bir yasa dışı amaçla kullanılması halinde sorumluluk kabul edilmemektedir.

Sürüm: 1.0

"""
# Mavi renkte yazdırma
colored_welcome = Fore.YELLOW + welcome_ascii + Style.RESET_ALL

print(colored_welcome)

print_custom_boxed_text(welcome_message)




def main_menu():
    while True:
        print("[1] MAC Değiştirme")
        print("[2] Ağ tarama")
        print("[3] Orta adam saldırısı")
        print("[4] Port Taraması")
        print("[5] Dizin Taraması")
        print("[6] SSH brute force")
        print("[7] Hash kırma")
        print("[8] Çıkış")

        choice = input("Seçiminiz: ")

        if choice == '1':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.mac_changer import main as mac_main
                mac_main()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '2':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.hostdiscovery import main as hostdiscovery
                hostdiscovery()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '3':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.man_in_the_middle import main as man_in_the_middle
                man_in_the_middle()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '4':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.nmap_python_write import main as port_scanner
                port_scanner()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '5':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.directory_scanning import main as directory_scan
                directory_scan()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '6':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.ssh_bruteforce import main as ssh_bruteforce
                ssh_bruteforce()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '7':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            try:
                from allCode.hash_lib_test import main as hash_crack
                hash_crack()
            except ImportError as e:
                print(Fore.RED + f"Modül hatası: {e}" + Style.RESET_ALL)
        elif choice == '8':
            print(Fore.BLUE + f"="*80 + Style.RESET_ALL)
            print("Çıkış yapılıyor...")
            sys.exit(0)
        elif choice.lower() == 'geri':
            print(Fore.BLUE + f"Ana menüye dönülüyor..."+Style.RESET_ALL)
            continue
        else:
            print(Fore.RED + "Geçersiz seçim. Lütfen 1 ile 8 arasında bir sayı girin veya 'geri' yazarak ana menüye dönün." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgramdan çıkılıyor..." + Style.RESET_ALL)
        sys.exit(0)

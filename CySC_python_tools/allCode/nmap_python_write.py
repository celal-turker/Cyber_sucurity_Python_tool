import nmap
import socket
import termcolor 
from colorama import Fore, Style
def is_valid_target(target):
    try:
        # Hedefi çözümle (DNS sorgusu yap)
        socket.gethostbyname(target)
        return True  # Gerçek bir adres, geçerli
    except socket.error:
        return False  # Geçersiz adres

def get_target():
    while True:
        try:
            target = input("Hedef IP veya alan adı: ")
            if is_valid_target(target):
                return target
            else:
                print("Geçersiz hedef adresi. Lütfen doğru bir IP veya alan adı girin.")
        except KeyboardInterrupt:
            print(termcolor.colored("\nProgram sonlandırılıyor...","blue"))
            exit()
        except Exception as e:
            print("Bir hata oluştu:", e)
def get_max_port():
    while True:
        try:
            port = int(input("Taranacak maksimum port numarası (örn: 1024): "))
            if port > 65536:
                print(termcolor.colored("Port aralığı 65536'dan fazla olamaz.","red"))
            else:
                return port
        except ValueError:
            print("Geçersiz bir sayı girdiniz. Lütfen bir tam sayı girin.")

        except KeyboardInterrupt:
            print(termcolor.colored("\nProgram sonlandırılıyor...","blue"))
            exit()
def get_scan_type():
    while True:
        try:
            print("Tarama Tipleri:")
            print("=="*30)
            print("1. Tam Tarama")
            print("2. Yarı açık tarama")
            print("3. Versiyon Bilgisi Tarama")
            print("4. İşletim Sistemi Bilgisi Tarama")
            print("5. Versiyon ve İşletim Sistemi Bilgisi Tarama")
            scan_type = int(input("Tarama tipini seçin (1-5): "))
            if 1 <= scan_type <= 5:
                return scan_type
            else:
                print("Geçersiz tarama tipi. Lütfen 1 ile 5 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz bir sayı girdiniz. Lütfen bir tam sayı girin.")
        except KeyboardInterrupt:
            print(termcolor.colored("\nProgram sonlandırılıyor...","blue"))
            exit()


def nmap_scan(scan_type, target, max_port):
    nm = nmap.PortScanner()
    print(termcolor.colored("Tarama işlemi yapılıyor...", "yellow"))

    if scan_type == 1:
        nm.scan(target, arguments=f'-p 1-{max_port} -sS')
    elif scan_type == 2:
        nm.scan(target, arguments=f'-sS -p 1-{max_port}')
    elif scan_type == 3:
        nm.scan(target, arguments=f'-sV -p 1-{max_port}')
    elif scan_type == 4:
        nm.scan(target, arguments=f'-O -A -p 1-{max_port}')
    elif scan_type == 5:
        nm.scan(target, arguments=f'-sV -O -p 1-{max_port}')
    else:
        raise ValueError("Geçersiz tarama tipi")

    for host in nm.all_hosts():
        print(termcolor.colored(f"Ana Bilgisayar: {host} ({nm[host].hostname()})", "green"))
        print(termcolor.colored("Durum: açık", "green"))

        if 'tcp' in nm[host]:
            print("PORT\tDURUM\tSERVİS\t\tVERSİYON")
            for port in nm[host]['tcp']:
                state = 'açık' if nm[host]['tcp'][port]['state'] == 'open' else 'kapalı'
                service = nm[host]['tcp'][port]['name']
                version = nm[host]['tcp'][port].get('version', 'bilinmiyor')
                product = nm[host]['tcp'][port].get('product', '')
                extra_info = nm[host]['tcp'][port].get('extrainfo', '')
                print(f"{port}/tcp\t{state}\t{service}\t\t{product} {version} {extra_info}")
        print(Fore.BLUE + f"="*80 + Style.RESET_ALL)

        if scan_type == 4 or scan_type == 5:
            if 'osclass' in nm[host]:
                for osclass in nm[host]['osclass']:
                    os_type = osclass.get('type', 'bilinmiyor')
                    os_vendor = osclass.get('vendor', 'bilinmiyor')
                    os_family = osclass.get('osfamily', 'bilinmiyor')
                    os_gen = osclass.get('osgen', 'bilinmiyor')
                    accuracy = osclass.get('accuracy', 'bilinmiyor')
                    print(f"İşletim Sistemi Türü: {os_type}\tSağlayıcı: {os_vendor}\tAile: {os_family}\tSürüm: {os_gen}\tDoğruluk: {accuracy}%")

            if 'osmatch' in nm[host]:
                for osmatch in nm[host]['osmatch']:
                    name = osmatch.get('name', 'bilinmiyor')
                    accuracy = osmatch.get('accuracy', 'bilinmiyor')
                    print(f"OS Match: {name}\tDoğruluk: {accuracy}%")

            if 'mac' in nm[host]['addresses']:
                mac = nm[host]['addresses']['mac']
                print(f"MAC Adresi: {mac}")

def main():
    target = get_target()
    max_port = get_max_port()
    scan_type = get_scan_type()
    nmap_scan(scan_type, target, max_port)
    print("Tarama tamamlandı.")

if __name__ == "__main__":
    main()

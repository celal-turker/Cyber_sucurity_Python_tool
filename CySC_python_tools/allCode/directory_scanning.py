import requests
from colorama import init, Fore
import os
import threading
import time

MAX_THREADS = 10  # Maksimum thread sayısı
MAX_RETRIES = 5   # Maksimum tekrar deneme sayısı
DELAY_BETWEEN_REQUESTS = 1  # Her istek arasındaki gecikme süresi (saniye cinsinden)
TIMEOUT = 10  # Zaman aşımı süresi

def check_directory(url, directory):
    directory_url = "{}/{}".format(url.rstrip('/'), directory.lstrip('/'))
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = requests.get(directory_url, timeout=TIMEOUT)

            if response.status_code == 200:
                print("[{}+ Bulundu: {}{}{}".format(Fore.GREEN, Fore.BLUE, directory_url, Fore.RESET))
                break
            else:
                break  # Bulunamayanları ekrana yazdırmadan pass geç
        except requests.RequestException as e:
            retries += 1
            time.sleep(1)  # Tekrar denemeden önce 1 saniye bekle

def dirbuster(url, directory_list):
    try:
        for directory in directory_list:
            directory = directory.strip()
            check_directory(url, directory)
            time.sleep(DELAY_BETWEEN_REQUESTS)  # Her istek arasına gecikme ekle
    except Exception as e:
        print("{}[!] Bir hata oluştu: {}{}".format(Fore.RED, str(e), Fore.RESET))

def main():
    init(autoreset=True)  # Renkleri otomatik olarak sıfırla
    try:
        while True:
            url = input("Lütfen taramak istediğiniz URL'yi girin: ")
            if not url.startswith("http://") and not url.startswith("https://"):
                print("{}Lütfen URL'yi http veya https ile başlayacak şekilde girin.{}".format(Fore.RED, Fore.RESET))
                continue
            try:
                response = requests.get(url, timeout=TIMEOUT)
                if response.status_code != 200:
                    print("{}Geçersiz URL veya erişilemez. Lütfen geçerli bir URL girin.{}".format(Fore.RED, Fore.RESET))
                    continue
                break  # Geçerli bir URL girdikten sonra döngüden çık
            except requests.RequestException as e:
                print("{}Geçersiz URL veya erişilemez: {}. Lütfen geçerli bir URL girin.{}".format(Fore.RED, str(e), Fore.RESET))
            except KeyboardInterrupt:
                print("\nProgramdan çıkılıyor...")
                return

    except KeyboardInterrupt:
        print("\nProgramdan çıkılıyor...")
        return
    except KeyboardInterrupt:
        print("\nProgramdan çıkılıyor...")
        return
    try:
        directory_list_path = input("Denenecek dizin sözlüğünün yolunu giriniz: ")
        if not os.path.exists(directory_list_path):
            raise FileNotFoundError

        with open(directory_list_path, 'r') as file:
            directories = file.readlines()
        threads = []
        for i in range(0, len(directories), MAX_THREADS):
            thread_list = directories[i:i+MAX_THREADS]
            thread = threading.Thread(target=dirbuster, args=(url, thread_list))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nProgramdan çıkılıyor...")
        exit()
    except KeyboardInterrupt:
        print("\nProgramdan çıkılıyor...")
        exit()
    except FileNotFoundError:
        print("{}Belirtilen dosya bulunamadı. Lütfen geçerli bir dosya yolunu girin.{}".format(Fore.RED, Fore.RESET))
    except Exception as e:
        print("{}[!] Bir hata oluştu: {}{}".format(Fore.RED, str(e), Fore.RESET))

if __name__ == "__main__":
    main()

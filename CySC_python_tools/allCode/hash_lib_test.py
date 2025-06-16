import hashlib
import time
from colorama import init, Fore

init(autoreset=True)  # Renklerin sürekli olarak sıfırlanmasını sağlar

def choice_user():
    while True:
        print("""Lütfen kırmak istediğiniz hash algoritmasını seçin:
                    [1]: MD5
                    [2]: SHA-1
                    [3]: SHA-224
                    [4]: SHA-256
                    [5]: SHA-384
                    [6]: SHA-512
                    [7]: SHA-3-224
                    [8]: SHA-3-256
                    [9]: SHA-3-384
                    [10]: SHA-3-512
              """)

        try:
            algorithm_choice = input("Algoritma seçin (Çıkmak için Enter): ")
            if not algorithm_choice:
                print("Programdan çıkılıyor...")
                exit()
        except KeyboardInterrupt:
            print("\nProgramdan Çıkılıyor...")
            exit()

        algorithms = {
            '1': 'md5',
            '2': 'sha1',
            '3': 'sha224',
            '4': 'sha256',
            '5': 'sha384',
            '6': 'sha512',
            '7': 'sha3_224',
            '8': 'sha3_256',
            '9': 'sha3_384',
            '10': 'sha3_512',
        }
        algorithm = algorithms.get(algorithm_choice)
        if algorithm:
            break
        else:
            print("Geçersiz giriş. Lütfen geçerli bir seçenek belirtin.")

    return algorithm

def get_user_input():   
    try:
        hash_to_crack = input("Kırmak istediğiniz hash'i girin: ")
    except KeyboardInterrupt:
        print("\nProgramdan Çıkılıyor...")
        exit()
    
    while True:
        try:
            wordlist = input("Kullanılacak kelime listesinin yolunu girin: ")
            with open(wordlist, "r"):
                break
        except FileNotFoundError:
            print(Fore.RED + "Belirtilen dosya bulunamadı. Lütfen geçerli bir dosya yolunu girin.")
        except Exception:
            print(Fore.RED + "Bir hata oluştu. Lütfen geçerli bir dosya yolunu girin.")
        except KeyboardInterrupt:
            print("\nProgramdan Çıkılıyor...")
            exit()
    return hash_to_crack, wordlist

def crack_hash(algorithm, hash_to_crack, wordlist):
    start_time = time.time()  # Zamanlayıcıyı başlat
    try:
        with open(wordlist, "r", errors="ignore") as f:
            for word in f:
                word = word.strip()
                hashed_word = hashlib.new(algorithm, word.encode()).hexdigest()
                print(Fore.RED + "Denenen şifre:", word, "==", hashed_word)
                if hashed_word == hash_to_crack:
                    elapsed_time = time.time() - start_time  # Geçen süreyi hesaplar
                    return Fore.GREEN + f"Hash çözüldü! Şifre: {word}\nGeçen süre: {elapsed_time:.2f} saniye"
        elapsed_time = time.time() - start_time  # Geçen süreyi hesaplar
        return Fore.RED + f"Verilen hash değeri kelime listesinde bulunamadı! :( \nGeçen süre: {elapsed_time:.2f} saniye"
    except FileNotFoundError:
        return Fore.RED + "Kelime listesi dosyası bulunamadı!"
    except KeyboardInterrupt:
        print("\nProgramdan Çıkılıyor...")
        exit()
    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")
        return Fore.RED + "Bilinmeyen bir hata oluştu!"
            
def main():
    while True:
        algorithm = choice_user()
        hash_to_crack, wordlist = get_user_input()
        result = crack_hash(algorithm, hash_to_crack, wordlist)
        print(result)
        print("Ana ekrana dönülüyor...")
        print("=" * 30)

if __name__ == "__main__":
    main()

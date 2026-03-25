import requests
import re
import time

def hledej_v_souboru():
    try:
        with open("weby_restauraci.txt", "r") as f:
            weby = f.read().splitlines()
    except FileNotFoundError:
        print("Soubor weby_restauraci.txt nebyl nalezen.")
        return

    vzor = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    for url in weby:
        print(f"Prohledávám: {url}")
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            emaily = set(re.findall(vzor, response.text))
            
            if emaily:
                with open("vsechny_kontakty.txt", "a") as f_out:
                    for email in emaily:
                        print(f"  -> Nalezen: {email}")
                        f_out.write(f"{url} : {email}\n")
            # Pauza, abychom nebyli zablokováni
            time.sleep(1)
        except:
            print(f"  x Web {url} nešel načíst.")

if __name__ == "__main__":
    hledej_v_souboru()


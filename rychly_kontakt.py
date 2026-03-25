import requests
import re

def hledej_emaily_na_google():
    print("\n--- RYCHLÝ SBĚR E-MAILŮ Z GOOGLE ---")
    dotaz = input("Co hledat? (např. restaurace praha kontakt): ").replace(" ", "+")
    
    # Budeme simulovat vyhledávání e-mailů přímo v Googlu
    url = f"https://www.google.com/search?q={dotaz}+email+@gmail.com+OR+@info.cz"
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    print("Hledám kontakty...")
    try:
        r = requests.get(url, headers=h)
        # Regulární výraz pro e-maily
        vzor = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emaily = set(re.findall(vzor, r.text))
        
        if emaily:
            print(f"\nNalezeno {len(emaily)} e-mailů:")
            with open("vsechny_kontakty.txt", "a") as f:
                for email in emaily:
                    print(f"[+] {email}")
                    f.write(email + "\n")
            print("\nUloženo do vsechny_kontakty.txt")
        else:
            print("Google nic neukázal. Zkus jiný dotaz (např. 'instalatéři kontakt').")
            
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    hledej_emaily_na_google()


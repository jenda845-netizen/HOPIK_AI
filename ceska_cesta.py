import requests
import re
import urllib.parse

def hledej_ciste_emaily():
    print("\n--- PROFESIONÁLNÍ SBĚR E-MAILŮ ---")
    dotaz = input("Hledat (např. restaurace praha kontakt): ").strip().replace(" ", "+")
    
    url = f"https://www.google.com/search?q={dotaz}+email+OR+kontakt"
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        r = requests.get(url, headers=h)
        # Dekódujeme URL znaky (změní %2B na + atd.)
        text = urllib.parse.unquote(r.text)
        
        # Přísnější filtr pro e-maily
        vzor = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        nalezeno = re.findall(vzor, text)
        
        emaily = set()
        for e in nalezeno:
            # Ignorujeme systémové e-maily Googlu nebo příliš krátké nesmysly
            if 'google' not in e.lower() and len(e) > 5:
                emaily.add(e.lower())
        
        if emaily:
            print(f"\nNalezeno {len(emaily)} čistých kontaktů:")
            with open("vsechny_kontakty.txt", "a") as f:
                for email in sorted(emaily):
                    print(f"[+] {email}")
                    f.write(email + "\n")
            print("\nUloženo do vsechny_kontakty.txt")
        else:
            print("Žádné čisté e-maily nenalezeny. Zkus jiný dotaz.")
            
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    hledej_ciste_emaily()


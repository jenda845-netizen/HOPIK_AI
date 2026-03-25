import requests
import re

def najdi_emaily():
    url = input("Vlož celou adresu webu (včetně http/https): ")
    
    print(f"Stahuji obsah z: {url}...")
    
    try:
        # Stáhneme zdrojový kód stránky
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        html_text = response.text
        
        # Regulární výraz pro nalezení e-mailů
        vzor = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emaily = set(re.findall(vzor, html_text)) # set() odstraní duplicity
        
        if emaily:
            print(f"\nNalezeno {len(emaily)} e-mailů:")
            with open("kontakty.txt", "a") as soubor:
                for email in emaily:
                    print(f"- {email}")
                    soubor.write(email + "\n")
            print("\nE-maily byly uloženy do souboru kontakty.txt")
        else:
            print("Na této stránce nebyly nalezeny žádné e-maily.")
            
    except Exception as e:
        print(f"Chyba při stahování webu: {e}")

if __name__ == "__main__":
    najdi_emaily()


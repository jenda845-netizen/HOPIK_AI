import http.client
import json

# --- ZDE VLOŽ SVŮJ KLÍČ (sk-proj-...) ---
API_KEY = "TVŮJ_SKUTEČNÝ_KLÍČ"
# -----------------------------------------

def ai_request(system_prompt, user_input):
    conn = http.client.HTTPSConnection("api.openai.com")
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}".encode('ascii', 'ignore').decode('ascii')
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    if res.status == 200:
        return json.loads(data)['choices'][0]['message']['content']
    else:
        return f"Chyba {res.status}: {data}"

def main():
    print("\n=== UNIVERZÁLNÍ AI VÝDĚLEK ===")
    print("1 - Recenze (pro restaurace/firmy)")
    print("2 - Popisky (pro e-shopy)")
    print("3 - Inzeráty (pro realitky)")
    
    volba = input("\nCo chceš dnes dělat? (1/2/3): ")
    
    if volba == "1":
        text = input("\nVlož text recenze z Google Map: ")
        prompt = "Jsi manažer české firmy. Napiš zdvořilou a děkovnou odpověď na tuto recenzi."
    elif volba == "2":
        text = input("\nVlož název produktu a klíčové vlastnosti: ")
        prompt = "Jsi copywriter. Napiš prodejní a lákavý popisek produktu pro e-shop v češtině."
    elif volba == "3":
        text = input("\nVlož parametry bytu/domu (plocha, lokalita, stav): ")
        prompt = "Jsi realitní makléř. Napiš emotivní a profesionální inzerát pro tento objekt."
    else:
        print("Neplatná volba.")
        return

    print("\nGeneruji výsledek skrze AI...\n")
    vysledek = ai_request(prompt, text)
    print("--- VÝSLEDEK ---")
    print(vysledek)
    print("----------------")

if __name__ == "__main__":
    main()


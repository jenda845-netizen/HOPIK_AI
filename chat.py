import openai
import os

# Načtení klíče z Termuxu
openai.api_key = os.getenv("OPENAI_API_KEY")

print("-------------------------------------------")
print("   VÁŠ CHATBOT JE ONLINE (napište 'konec')")
print("-------------------------------------------")

# Paměť pro konverzaci (aby si GPT pamatoval, co jste psali předtím)
history = [{"role": "system", "content": "Jsi užitečný asistent v mobilním terminálu Termux."}]

while True:
    user_input = input("Vy: ")
    
    # Podmínka pro ukončení
    if user_input.lower() in ["konec", "exit", "quit", "stop"]:
        print("Ukončuji chat... Nashledanou!")
        break
        
    history.append({"role": "user", "content": user_input})
    
    try:
        # Volání OpenAI (používáme verzi 0.28, kterou jsme nainstalovali)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history
        )
        
        answer = response.choices[0].message.content
        print(f"\nGPT: {answer}\n")
        
        # Přidání odpovědi do historie
        history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        print(f"Ups, stala se chyba: {e}")


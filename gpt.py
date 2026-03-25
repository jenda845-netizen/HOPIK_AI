import openai
import os

# Načte klíč z prostředí
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "user", "content": "Ahoj, funguješ?"}
        ]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Chyba: {e}")


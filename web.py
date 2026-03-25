from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Tvůj klíč
openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generovat', methods=['POST'])
def generovat():
    vstup = request.form.get('vstup')
    sluzba = request.form.get('sluzba')
    if not vstup:
        return render_template('index.html', odpoved="⚠️ Zadejte prosím zadání.")
    
    # TADY JE TA ZMĚNA - PROFI POPISKY
    prompty = {
        "recenze": f"Napiš diplomatickou odpověď na recenzi: {vstup}",
        "popisky": f"Vytvoř luxusní prodejní popisek produktu: {vstup}. Použij techniku AIDA. Začni háčkem, popiš emoci z používání, přidej technické parametry v odrážkách a zakonči silnou výzvou k akci (CTA).",
        "social": f"Navrhni 3 posty na sítě (včetně emoji): {vstup}",
        "recepty": f"Vytvoř recept a kalkulaci v CZK: {vstup}",
        "prodej": f"Napiš B2B prodejní email pro firmu: {vstup}",
        "reklama": f"Vytvoř 3 úderné verze reklamy na: {vstup}"
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jsi elitní český copywriter a marketér. Píšeš poutavě, moderně a s důrazem na prodej."},
                {"role": "user", "content": prompty.get(sluzba, "Ahoj")}
            ]
        )
        return render_template('index.html', odpoved=response.choices[0].message.content)
    except Exception as e:
        return render_template('index.html', odpoved=f"❌ Chyba: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


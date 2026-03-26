from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# TVŮJ KLÍČ
openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generovat', methods=['POST'])
def generovat():
    vstup = request.form.get('vstup')
    sluzba = request.form.get('sluzba')
    
    prompty = {
        "recenze": f"Odpověz na recenzi: {vstup}",
        "popisky": f"Vytvoř prodejní AIDA popisek: {vstup}",
        "social": f"Navrhni posty na sítě: {vstup}",
        "recepty": f"Vytvoř recept a kalkulaci: {vstup}",
        "prodej": f"Napiš B2B email: {vstup}",
        "reklama": f"Vytvoř reklamu: {vstup}"
    }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jsi expert Blahovec AI, mluvíš česky a profesionálně."},
                {"role": "user", "content": prompty.get(sluzba)}
            ]
        )
        vysledek = response.choices[0].message.content
        return render_template('index.html', odpoved=vysledek)
    except Exception as e:
        return render_template('index.html', odpoved=f"Chyba: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


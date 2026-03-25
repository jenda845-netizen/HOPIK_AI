from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blahovec-ultra-tajemstvi'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

openai.api_key = "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"

# Jednoduchý uživatel bez databáze
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return User("admin")
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Tady jsou tvoje přístupové údaje natvrdo
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin-heslo-123':
            user = User("admin")
            login_user(user)
            return redirect(url_for('index'))
        flash('❌ Špatné jméno nebo heslo')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/generovat', methods=['POST'])
@login_required
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
            messages=[{"role": "system", "content": "Jsi expert Blahovec AI."}, {"role": "user", "content": prompty.get(sluzba)}]
        )
        return render_template('index.html', odpoved=response.choices[0].message.content)
    except Exception as e:
        return render_template('index.html', odpoved=f"Chyba: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


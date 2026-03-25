from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import openai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blahovec-super-tajne-heslo'
# Použijeme SQLite v dočasné složce Renderu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/uzivatele.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

openai.api_key = "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"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
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

# Automatické vytvoření databáze při každém startu
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="admin-heslo-123")
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


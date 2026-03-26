from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import openai
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jenda-ai-ultra-tajemstvi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/databaze.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# TVOJE KLÍČE
openai.api_key = "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"
stripe.api_key = "Sk_test_51TF9vMCZkYz1EmPKHVhK0efWOYz8xz3LyY6DncToW8BaRiko5kyLBbwDmUArjwaH1Ju6pN6kMT1Jl6IlaTa3RySk00HRvdyPlD"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    pokusy = db.Column(db.Integer, default=0)
    is_premium = db.Column(db.Boolean, default=False)

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
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/pay')
@login_required
def pay():
    # Vytvoření Stripe Checkout Session
    session_stripe = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'czk',
                'product_data': {'name': 'Blahovec AI - Neomezený balíček'},
                'unit_amount': 49000, # 490.00 CZK
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('index', _external=True),
    )
    return redirect(session_stripe.url, code=303)

@app.route('/success')
@login_required
def success():
    current_user.is_premium = True
    db.session.commit()
    return render_template('index.html', odpoved="✅ PLATBA ÚSPĚŠNÁ! Nyní máte neomezený přístup.")

@app.route('/generovat', methods=['POST'])
@login_required
def generovat():
    if current_user.pokusy >= 3 and not current_user.is_premium:
        return render_template('index.html', odpoved="⚠️ DOSÁHL JSTE LIMITU. <a href='/pay' style='color:#3b82f6;font-weight:bold;'>KLIKNĚTE ZDE PRO AKTIVACI (490 Kč)</a>")

    vstup = request.form.get('vstup')
    sluzba = request.form.get('sluzba')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Expert: {vstup}"}]
        )
        current_user.pokusy += 1
        db.session.commit()
        return render_template('index.html', odpoved=response.choices[0].message.content)
    except Exception as e:
        return render_template('index.html', odpoved=f"Chyba: {str(e)}")

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='jenda').first():
        db.session.add(User(username='jenda', password='heslo123'))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


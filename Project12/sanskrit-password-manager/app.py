from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from password_generator import SanskritPasswordGenerator
from cryptography.fernet import Fernet
import base64

# Initialize Flask app
app = Flask(__name__)

# Simple configuration (avoiding the import issue)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sanskrit_passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize password generator
generator = SanskritPasswordGenerator()

# Encryption key for passwords
def get_encryption_key():
    key = app.config.get('ENCRYPTION_KEY')
    if not key:
        key = Fernet.generate_key()
        app.config['ENCRYPTION_KEY'] = key
    return key

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    passwords = db.relationship('Password', backref='user', lazy=True, cascade='all, delete-orphan')

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.Text, nullable=False)
    sanskrit_hint = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def set_password(self, password):
        f = Fernet(get_encryption_key())
        self.encrypted_password = f.encrypt(password.encode()).decode()
    
    def get_password(self):
        f = Fernet(get_encryption_key())
        return f.decrypt(self.encrypted_password.encode()).decode()

# Utility functions
def calculate_password_strength(password):
    score = 0
    feedback = []
    
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)
    
    # Length scoring
    if length >= 12:
        score += 25
    elif length >= 8:
        score += 15
    else:
        feedback.append("Use at least 8 characters")
    
    # Character variety
    if has_upper:
        score += 5
    else:
        feedback.append("Add uppercase letters")
    
    if has_lower:
        score += 5
    else:
        feedback.append("Add lowercase letters")
    
    if has_digit:
        score += 10
    else:
        feedback.append("Add numbers")
    
    if has_symbol:
        score += 15
    else:
        feedback.append("Add symbols")
    
    # Determine level
    if score >= 80:
        level = "Very Strong"
        color = "green"
    elif score >= 60:
        level = "Strong"
        color = "blue"
    elif score >= 40:
        level = "Medium"
        color = "yellow"
    elif score >= 20:
        level = "Weak"
        color = "orange"
    else:
        level = "Very Weak"
        color = "red"
    
    return {
        'score': min(100, max(0, score)),
        'level': level,
        'color': color,
        'feedback': feedback[:3]
    }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    passwords = Password.query.filter_by(user_id=current_user.id).order_by(Password.created_at.desc()).all()
    return render_template('dashboard.html', passwords=passwords)

@app.route('/generator')
@login_required
def generate_password_page():
    return render_template('generator.html')

@app.route('/api/generate-password', methods=['POST'])
@login_required
def generate_password():
    try:
        data = request.get_json()
        
        password_type = data.get('type', 'sanskrit')
        length = int(data.get('length', 12))
        include_symbols = data.get('include_symbols', True)
        include_numbers = data.get('include_numbers', True)
        include_uppercase = data.get('include_uppercase', True)
        
        if password_type == 'sanskrit':
            result = generator.generate_sanskrit_password(
                length=length,
                include_symbols=include_symbols,
                include_numbers=include_numbers,
                include_uppercase=include_uppercase
            )
        elif password_type == 'phrase':
            result = generator.generate_phrase_password(
                word_count=data.get('word_count', 4),
                separator=data.get('separator', '-'),
                include_numbers=include_numbers
            )
        elif password_type == 'pin':
            result = generator.generate_pin(length=length)
        else:
            result = generator.generate_memorable_password(
                length=length,
                include_symbols=include_symbols,
                include_numbers=include_numbers
            )
        
        strength = calculate_password_strength(result['password'])
        
        return jsonify({
            'success': True,
            'password': result['password'],
            'strength': strength,
            'metadata': {
                'type': password_type,
                'sanskrit_word': result.get('sanskrit_word'),
                'meaning': result.get('meaning'),
                'entropy': result.get('entropy', 0)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/save-password', methods=['POST'])
@login_required
def save_password():
    try:
        data = request.get_json()
        
        password_entry = Password(
            website=data['website'],
            username=data['username'],
            sanskrit_hint=data.get('sanskrit_hint', ''),
            user_id=current_user.id
        )
        password_entry.set_password(data['password'])
        
        db.session.add(password_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password saved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/get-password/<int:password_id>')
@login_required
def get_password(password_id):
    try:
        password_entry = Password.query.filter_by(
            id=password_id, 
            user_id=current_user.id
        ).first()
        
        if not password_entry:
            return jsonify({
                'success': False,
                'error': 'Password not found'
            }), 404
        
        return jsonify({
            'success': True,
            'password': password_entry.get_password()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/delete-password/<int:password_id>', methods=['DELETE'])
@login_required
def delete_password(password_id):
    try:
        password_entry = Password.query.filter_by(
            id=password_id,
            user_id=current_user.id
        ).first()
        
        if not password_entry:
            return jsonify({
                'success': False,
                'error': 'Password not found'
            }), 404
        
        db.session.delete(password_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password deleted successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

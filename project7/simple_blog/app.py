from flask import Flask, render_template, request, redirect, url_for, session
from model import db, User  # ✅ Import User here
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

# ----------- Initialize DB -----------
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

init_db()

# ----------- ROUTES -----------

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "Post not found", 404
    return render_template('post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

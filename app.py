
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 连接到SQLite数据库
        conn = sqlite3.connect('./users.db')
        c = conn.cursor()
        
        # 检查用户名是否已经存在
        c.execute('SELECT * FROM users WHERE username = ?', (username,))

        if c.fetchone():
            conn.close()
            return '用户已经存在'  # 用户名已经存在
        # 插入新用户
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return "success"
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 连接到SQLite数据库
        conn = sqlite3.connect('./users.db')
        c = conn.cursor()
        
        # 查询用户信息
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        
        # 关闭数据库连接
        conn.close()
        
        # 检查用户是否存在
        if user:
            session['username'] = username
            return "success"
        else:
            return 'failure'
    else:
        return render_template('login.html')
    
@app.route('/submit_score', methods=['POST'])
def submit_score():
    if request.method == 'POST':
        username = session.get('username')  # 从 session 中获取用户名
        score = request.form['score']  # 从表单获取分数
        
        # 连接到数据库
        conn = sqlite3.connect('./users.db')
        c = conn.cursor()
        
        # 将分数插入到 scores 表中
        c.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
        conn.commit()
        conn.close()
        
        return "Score submitted successfully!"

@app.route('/history')
def history():
    username = session.get('username')  # 从 session 中获取用户名
    conn = sqlite3.connect('./users.db')
    c = conn.cursor()
    
    # 查询该用户的历史分数
    c.execute('SELECT score, timestamp FROM scores WHERE username = ?', (username,))
    scores = c.fetchall()
    conn.close()
    
    return render_template('history.html', scores=scores)


@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

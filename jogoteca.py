from flask import Flask, render_template, request, redirect, flash, session, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome =nome
        self.categoria=categoria
        self.console=console

class User:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

user1 = User('Bruno Henrique', 'BrunoH', '123456')
user2 = User('Nayara Lopes', 'NayLop', '654321')

users = {
    user1.nickname : user1,
    user2.nickname : user2
}

app = Flask(__name__)

app.secret_key = 'ShiroeChin'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('login', next=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in users:
        user = users[request.form['usuario']]
        if request.form['senha'] == user.senha:
            flash('login efetuado com sucesso.')
            session['user'] = request.form['usuario']
            next_page = request.form['next']
            print(next_page)
            return redirect(next_page)
    else:
        flash('Usuario ou senhar incorretos.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user'] = None
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('index'))

app.run(debug=True)
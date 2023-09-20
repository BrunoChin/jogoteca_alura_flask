from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.secret_key = 'ShiroeChin'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD=config.SGBD,
        user=config.user,
        password=config.password,
        server=config.server,
        database=config.database
    )

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    console = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nome = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(20), primary_key=True)
    senha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():

    lista = Jogos.query.order_by(Jogos.id)

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

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo ja existe na base de dados")
        return redirect(url_for('criar'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login')
def login():
    next = request.args.get('next')
    return render_template('login.html', next=next)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            flash('login efetuado com sucesso.')
            session['user'] = usuario.nickname
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
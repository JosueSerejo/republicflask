from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Função para obter o nome do usuário logado
def obter_usuario_nome():
    if 'usuario_id' in session:
        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (session['usuario_id'],))
        usuario = cursor.fetchone()
        conn.close()
        if usuario:
            return usuario[0]
    return None

# Página principal
@app.route('/')
def index():
    usuario_nome = obter_usuario_nome()
    return render_template('index.html', usuario_nome=usuario_nome)

@app.route('/sobre')
def sobre():
    usuario_nome = obter_usuario_nome()
    return render_template('sobre.html', usuario_nome=usuario_nome)

@app.route('/pesquisa')
def pesquisa():
    usuario_nome = obter_usuario_nome()
    return render_template('pesquisa.html', usuario_nome=usuario_nome)

@app.route('/apt')
def apt():
    usuario_nome = obter_usuario_nome()
    return render_template('apt.html', usuario_nome=usuario_nome)

@app.route('/termos')
def termos():
    usuario_nome = obter_usuario_nome()
    return render_template('termos.html', usuario_nome=usuario_nome)



# Página de Cadastro/Login (cadastro.html)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem_cadastro = None
    mensagem_login = None

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        celular = request.form['celular']

        try:
            conn = sqlite3.connect('instance/banco.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nome, email, senha, celular) VALUES (?, ?, ?, ?)',
                        (nome, email, senha, celular))
            conn.commit()
            conn.close()

            mensagem_cadastro = 'Cadastro realizado com sucesso!'
        except sqlite3.IntegrityError:
            mensagem_cadastro = 'Email já cadastrado.'

    return render_template('cadastro.html', mensagem_cadastro=mensagem_cadastro, mensagem_login=mensagem_login)

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem_login = None
    mensagem_cadastro = None

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario[0]  # Armazena o ID do usuário na sessão
            return redirect(url_for('index'))
        else:
            mensagem_login = 'Email ou senha inválidos!'

    return render_template('cadastro.html', mensagem_login=mensagem_login, mensagem_cadastro=mensagem_cadastro)

# Página protegida (só pra logados)
@app.route('/index')
def home():
    if 'usuario_id' not in session:
        return redirect(url_for('cadastro'))

    usuario_nome = obter_usuario_nome()  # Recupera o nome do usuário
    return render_template('index.html', usuario_nome=usuario_nome)

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)  # Remove o ID do usuário da sessão
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)

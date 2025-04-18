from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Página inicial (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Página de Sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Página de Termos
@app.route('/sobtermosre')
def termos():
    return render_template('termos.html')

# Página de Pesquisa
@app.route('/pesquisa')
def pesquisa():
    return render_template('pesquisa.html')

# Página de Cadastro/Login (cadastro.html)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = None  # Variável para guardar a mensagem a ser exibida

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        celular = request.form['celular']

        # Conectar ao banco
        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()

        # Verificar se o email já está cadastrado
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()

        if usuario:
            mensagem = 'Este usuário já está cadastrado!'
        else:
            cursor.execute('INSERT INTO usuarios (nome, email, senha, celular) VALUES (?, ?, ?, ?)',
                           (nome, email, senha, celular))
            conn.commit()
            mensagem = 'Cadastro realizado com sucesso!'

        conn.close()

    return render_template('cadastro.html', mensagem=mensagem)


# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensagem_login = None  # Variável para armazenar a mensagem de erro ou sucesso do login

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            return redirect(url_for('semlogin'))
        else:
            mensagem_login = 'Email ou senha inválidos!'  # Exibe a mensagem de erro somente no login

    return render_template('cadastro.html', mensagem_login=mensagem_login)



    
    # Se o método for GET, renderiza a página de login
    return render_template('login.html')


# Página protegida (só pra logados)
@app.route('/semlogin')
def semlogin():
    if 'usuario_id' not in session:
        return redirect(url_for('cadastro'))

    # Recuperar o nome do usuário a partir do banco de dados
    usuario_id = session['usuario_id']
    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (usuario_id,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        usuario_nome = usuario[0]  # Nome do usuário
        return render_template('semlogin.html', usuario_nome=usuario_nome)

    return redirect(url_for('cadastro'))  # Caso o usuário não seja encontrado


# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)

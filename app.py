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

# Torna usuario_nome acessível automaticamente em todos os templates
@app.context_processor
def inject_usuario_nome():
    return dict(usuario_nome=obter_usuario_nome())

# Página principal (home)
@app.route('/')
def index():
    return render_template('index.html')

# Página sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Página de pesquisa de imóveis
@app.route('/pesquisa')
def pesquisa():
    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, tipo, quartos, valor, endereco, inclusos, imagem FROM apartamentos")
    rows = cursor.fetchall()
    conn.close()

    apartamentos = []
    for row in rows:
        apt = {
            'id': row[0],
            'tipo': row[1],
            'quartos': row[2],
            'valor': row[3],
            'endereco': row[4],
            'inclusos': row[5].split(',') if row[5] else [],
            'imagem': row[6]
        }
        apartamentos.append(apt)

    return render_template('pesquisa.html', apartamentos=apartamentos)

# Página de apartamentos (acesso restrito)
@app.route('/apt')
def apt():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('apt.html')

# Página de termos
@app.route('/termos')
def termos():
    return render_template('termos.html')

import os
from werkzeug.utils import secure_filename

@app.route('/cadastro_imovel', methods=['GET', 'POST'])
def cadastro_imovel():
    if request.method == 'POST':
        # Coleta os dados do imóvel
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        numero = request.form['numero']
        cep = request.form['cep']
        complemento = request.form['complemento']
        valor = request.form['valor'].replace(",", ".")
        quartos = request.form['quartos']
        banheiros = request.form['banheiros']
        inclusos = request.form.getlist('inclusos')  # lista
        outros = request.form['outros']
        descricao = request.form['descricao']

        imagens = request.files.getlist('fotos')  # Lista de imagens
        nomes_imagens = []  # Lista para armazenar os nomes das imagens

        for imagem in imagens:
            if imagem.filename != "":
                filename = secure_filename(imagem.filename)
                caminho_imagem = os.path.join('static/img/apts', filename)
                imagem.save(caminho_imagem)
                nomes_imagens.append(filename)

        # Se não houver nenhuma imagem, podemos usar uma imagem padrão
        if not nomes_imagens:
            nomes_imagens.append('default.jpg')

        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO apartamentos (endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, inclusos, outros, descricao, imagem, tipo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, ",".join(inclusos), outros, descricao, ",".join(nomes_imagens), 'apartamento'))
        conn.commit()
        conn.close()

        return redirect(url_for('pesquisa'))  # Redireciona para a página de pesquisa
    else:
        return render_template('cadastro_imovel.html')

@app.route('/detalhes_apartamento/<int:id>')
def detalhes_apartamento(id):
    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM apartamentos WHERE id = ?", (id,))
    apartamento = cursor.fetchone()
    conn.close()

    if apartamento:
        apt = {
            'id': apartamento[0],
            'endereco': apartamento[1],
            'bairro': apartamento[2],
            'numero': apartamento[3],
            'cep': apartamento[4],
            'complemento': apartamento[5],
            'valor': apartamento[6],
            'quartos': apartamento[7],
            'banheiros': apartamento[8],
            'inclusos': apartamento[9].split(',') if apartamento[9] else [],
            'outros': apartamento[10],
            'descricao': apartamento[11],
            'imagem': apartamento[12],
            'tipo': apartamento[13]
        }
        return render_template('apt.html', apartamento=apt)
    else:
        return "Apartamento não encontrado", 404



# Página de Cadastro
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

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)

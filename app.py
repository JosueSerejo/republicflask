from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename

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

@app.context_processor
def inject_usuario_nome():
    return dict(usuario_nome=obter_usuario_nome())

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Página de pesquisa de apartamentos
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
            'imagens': row[6].split(',') if row[6] else ['default.jpg']
        }
        apartamentos.append(apt)

    return render_template('pesquisa.html', apartamentos=apartamentos)

# Página de cadastro de apartamento
@app.route('/apt')
def apt():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('apt.html')

# Página de termos de uso
@app.route('/termos')
def termos():
    return render_template('termos.html')

# Cadastro de imóvel
@app.route('/cadastro_imovel', methods=['GET', 'POST'])
def cadastro_imovel():
    if request.method == 'POST':
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        numero = request.form['numero']
        cep = request.form['cep']
        complemento = request.form['complemento']
        valor = request.form['valor'].replace(",", ".")
        quartos = request.form['quartos']
        banheiros = request.form['banheiros']
        inclusos = request.form.getlist('inclusos')
        outros = request.form['outros']
        descricao = request.form['descricao']

        imagens = request.files.getlist('fotos')
        nomes_imagens = []

        for imagem in imagens:
            if imagem.filename != "":
                filename = secure_filename(imagem.filename)
                caminho = os.path.join('static/img/apts', filename)
                imagem.save(caminho)
                nomes_imagens.append(filename)

        if not nomes_imagens:
            nomes_imagens.append('default.jpg')

        conn = sqlite3.connect('instance/banco.db')
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO apartamentos (endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, inclusos, outros, descricao, imagem, tipo, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            endereco, bairro, numero, cep, complemento, valor, quartos, banheiros,
            ",".join(inclusos), outros, descricao, ",".join(nomes_imagens), 'apartamento', session['usuario_id']
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('pesquisa'))
    return render_template('cadastro_imovel.html')

# Detalhes do apartamento
@app.route('/detalhes_apartamento/<int:id>')
def detalhes_apartamento(id):
    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute("""
       SELECT id, endereco, bairro, numero, cep, complemento, valor, quartos, 
              banheiros, inclusos, outros, descricao, imagem, tipo, usuario_id 
       FROM apartamentos WHERE id = ?
    """, (id,))
    row = cursor.fetchone()

    if row and len(row) >= 15:
        apt = {
            'id': row[0],
            'endereco': row[1],
            'bairro': row[2],
            'numero': row[3],
            'cep': row[4],
            'complemento': row[5],
            'valor': row[6],
            'quartos': row[7],
            'banheiros': row[8],
            'inclusos': row[9].split(',') if row[9] else [],
            'outros': row[10],
            'descricao': row[11],
            'imagens': row[12].split(',') if row[12] else ['default.jpg'],
            'tipo': row[13],
            'usuario_id': row[14]
        }

        # Busca nome do usuário dono
        cursor.execute('SELECT nome FROM usuarios WHERE id = ?', (apt['usuario_id'],))
        dono = cursor.fetchone()
        dono_nome = dono[0] if dono else 'Desconhecido'

        conn.close()

        return render_template('apt.html', apartamento=apt, dono_nome=dono_nome, usuario_logado=session.get('usuario_id'))
    
    conn.close()
    return "Apartamento não encontrado", 404

# Parar anúncio (deletar apartamento)
@app.route('/parar_anuncio/<int:id>', methods=['POST'])
def parar_anuncio(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usuario_id FROM apartamentos WHERE id = ?", (id,))
    apt = cursor.fetchone()

    if not apt or apt[0] != session['usuario_id']:
        conn.close()
        return "Acesso negado", 403

    # Apagar o anúncio
    cursor.execute("DELETE FROM apartamentos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('pesquisa'))

# Verificar estrutura da tabela apartamentos (para debug)
def verificar_estrutura_tabela():
    # Conectar ao banco de dados
    conn = sqlite3.connect('instance/banco.db')
    cursor = conn.cursor()
    
    # Verificar a estrutura da tabela 'apartamentos'
    cursor.execute("PRAGMA table_info(apartamentos);")
    colunas = cursor.fetchall()
    
    # Fechar a conexão
    conn.close()
    
    # Exibir as colunas da tabela 'apartamentos'
    print("Estrutura da tabela 'apartamentos':")
    for col in colunas:
        print(f"Coluna: {col[1]}, Tipo: {col[2]}")

# Rota de cadastro de usuário
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

# Rota de login
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
            session['usuario_id'] = usuario[0]
            return redirect(url_for('index'))
        else:
            mensagem_login = 'Email ou senha inválidos!'

    return render_template('cadastro.html', mensagem_login=mensagem_login, mensagem_cadastro=mensagem_cadastro)

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('cadastro'))

if __name__ == '__main__':
    app.run(debug=True)

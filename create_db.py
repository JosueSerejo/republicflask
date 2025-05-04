import sqlite3
import os

# Caminho do banco de dados
caminho_banco = 'instance/banco.db'

def criar_tabela_usuarios():
    # Garante que o diretório 'instance' exista
    os.makedirs('instance', exist_ok=True)
    
    # Conecta ao banco de dados
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Criação da tabela usuarios (caso ainda não exista)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            celular TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def cadastrar_usuario(nome, email, senha, celular):
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, celular)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, senha, celular))

        conn.commit()
        conn.close()
        return 'Cadastro realizado com sucesso!'
    except sqlite3.IntegrityError:
        conn.close()
        return 'Email já cadastrado.'

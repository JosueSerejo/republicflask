import sqlite3
import os

# Garante que o diretório 'instance' existe
os.makedirs('instance', exist_ok=True)

# Caminho do banco de dados
caminho_banco = 'instance/banco.db'

# Conecta e cria a tabela
conn = sqlite3.connect(caminho_banco)
cursor = conn.cursor()

# Criação da tabela apartamentos
cursor.execute("""
CREATE TABLE IF NOT EXISTS apartamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endereco TEXT,
    bairro TEXT,
    numero TEXT,
    cep TEXT,
    complemento TEXT,
    valor REAL,
    quartos INTEGER,
    banheiros INTEGER,
    inclusos TEXT,
    outros TEXT,
    descricao TEXT,
    imagem TEXT,
    tipo TEXT
)
""")

conn.commit()
conn.close()

print("Tabela 'apartamentos' criada/verificada com sucesso no banco:", caminho_banco)

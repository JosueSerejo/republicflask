import sqlite3
import os

# Caminho onde seu banco está
DATABASE = os.path.join(os.getcwd(), 'instance', 'database.db')

# Conecta no banco
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Cria a tabela usuarios
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

print("Tabela 'usuarios' criada com sucesso!")
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('instance/banco.db')
cursor = conn.cursor()

# Adicionar a coluna 'usuario_id' à tabela 'apartamentos'
cursor.execute('ALTER TABLE apartamentos ADD COLUMN usuario_id INTEGER')

conn.commit()
conn.close()

print("Coluna 'usuario_id' adicionada com sucesso!")

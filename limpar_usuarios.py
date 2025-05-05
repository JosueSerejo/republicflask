import sqlite3

conn = sqlite3.connect('instance/banco.db')
cursor = conn.cursor()

# Excluir todos os imóveis onde usuario_id está vazio ou NULL
cursor.execute("DELETE FROM apartamentos WHERE usuario_id IS NULL")

conn.commit()
conn.close()

print("Imóveis sem usuário foram removidos.")

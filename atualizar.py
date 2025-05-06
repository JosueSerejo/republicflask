import sqlite3

conn = sqlite3.connect('instance/banco.db')
cursor = conn.cursor()

# Seleciona todos os apartamentos
cursor.execute("SELECT id, inclusos FROM apartamentos")
apartamentos = cursor.fetchall()

for apt in apartamentos:
    inclusos = apt[1]
    if inclusos:
        atualizados = inclusos
        atualizados = atualizados.replace("agua", "água")
        atualizados = atualizados.replace("mobilia", "mobília")
        atualizados = atualizados.replace("mobiliado", "mobiliado")  # mantém se já estiver ok
        atualizados = atualizados.replace("gas", "gás")

        if atualizados != inclusos:
            cursor.execute("UPDATE apartamentos SET inclusos = ? WHERE id = ?", (atualizados, apt[0]))

conn.commit()
conn.close()

print("Inclusos atualizados com acentuação correta.")

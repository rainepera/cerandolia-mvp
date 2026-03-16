import sqlite3
conexao = sqlite3.connect('cerandolia.db')
cursor = conexao.cursor()

# Adiciona a coluna 'status' com o valor inicial 'Pendências'
try:
    cursor.execute("ALTER TABLE arquivos ADD COLUMN status TEXT DEFAULT 'Pendências'")
    print("Coluna status adicionada!")
except:
    print("A coluna status já existia.")

conexao.commit()
conexao.close()
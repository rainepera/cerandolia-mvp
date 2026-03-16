import sqlite3
conexao = sqlite3.connect('cerandolia.db')
cursor = conexao.cursor()
cursor.execute("DELETE FROM pastas") # Isso apaga todas as pastas!
conexao.commit()
conexao.close()
print("Banco de pastas limpo!")
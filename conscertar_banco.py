import sqlite3

try:
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # Este comando "fura" a tabela e cria a coluna nova
    cursor.execute("ALTER TABLE arquivos ADD COLUMN status TEXT DEFAULT 'Pendências'")
    
    conexao.commit()
    print("✅ Sucesso! A coluna 'status' foi criada com sucesso.")
except sqlite3.OperationalError:
    print("⚠️ A coluna já existe ou houve um erro de acesso. Tente rodar o app agora!")
finally:
    conexao.close()
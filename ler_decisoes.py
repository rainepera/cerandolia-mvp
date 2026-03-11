import sqlite3

def listar_decisoes():
    # 1. Conecta ao banco de dados onde salvamos a informação
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # 2. O comando SELECT * significa "Selecione TUDO" da tabela decisoes
    cursor.execute("SELECT * FROM decisoes")
    
    # 3. fetchall() pega todas as linhas que o banco encontrou e guarda na variável 'decisoes'
    decisoes = cursor.fetchall()

    print("\n--- 📚 DECISION LEDGER: MEMÓRIA DA EMPRESA ---")
    
    # 4. Um loop para mostrar cada decisão de forma organizada no terminal
    for decisao in decisoes:
        print(f"ID (Registro): {decisao[0]}")
        print(f"Título: {decisao[1]}")
        print(f"Decisão: {decisao[2]}")
        print(f"Contexto: {decisao[3]}")
        print(f"Responsável: {decisao[4]}")
        print(f"Data: {decisao[5]}")
        print(f"Versão: v{decisao[6]}")
        print("-" * 45)

    # 5. Fecha a conexão
    conexao.close()

# Chamando a função para exibir tudo
listar_decisoes()
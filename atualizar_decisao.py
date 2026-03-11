import sqlite3

def atualizar_decisao(id_decisao, nova_decisao):
    # 1. Conecta ao banco
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # 2. Comando UPDATE para alterar a decisão e mudar a versão para 2
    # O "WHERE id = ?" é VITAL! Ele garante que só vamos alterar a decisão certa.
    cursor.execute('''
        UPDATE decisoes 
        SET decisao_tomada = ?, versao = 2 
        WHERE id = ?
    ''', (nova_decisao, id_decisao))

    # 3. Salva e fecha
    conexao.commit()
    conexao.close()
    
    print(f"🔄 Sucesso! A decisão {id_decisao} foi atualizada para a v2.")

# Chamando a função: Vamos atualizar a decisão de ID 1 que criamos antes
atualizar_decisao(
    id_decisao=1, 
    nova_decisao="Utilizar SQLite para o MVP e planejar migração para PostgreSQL no futuro."
)
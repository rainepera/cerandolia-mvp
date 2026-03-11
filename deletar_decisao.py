import sqlite3

def deletar_decisao(id_decisao):
    # 1. Conecta ao banco de dados
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # 2. Comando DELETE para apagar a linha específica
    # O "WHERE id = ?" garante que só vamos apagar a decisão que passarmos o número
    cursor.execute('''
        DELETE FROM decisoes 
        WHERE id = ?
    ''', (id_decisao,)) # Essa vírgula depois do id_decisao é obrigatória no Python quando temos apenas 1 item!

    # 3. Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    
    print(f"🗑️ Sucesso! A decisão {id_decisao} foi excluída permanentemente do Ledger.")

# Chamando a função: Vamos deletar a decisão de ID 2 que acabamos de criar
deletar_decisao(id_decisao=2)
import sqlite3
from datetime import datetime

def adicionar_decisao(titulo, decisao_tomada, descricao, responsavel):
    # Conecta ao banco de dados (cria o arquivo se não existir)
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # GARANTIA: Cria a tabela automaticamente caso ela não exista neste arquivo!
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS decisoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        decisao_tomada TEXT NOT NULL,
        descricao TEXT,
        responsavel TEXT NOT NULL,
        data TEXT NOT NULL,
        versao INTEGER DEFAULT 1
    )
    ''')

    # Pega a data e hora exata de agora
    data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")

    # Comando SQL para inserir os dados na tabela
    cursor.execute('''
        INSERT INTO decisoes (titulo, decisao_tomada, descricao, responsavel, data, versao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, decisao_tomada, descricao, responsavel, data_atual, 1))

    # Salva e fecha a conexão
    conexao.commit()
    conexao.close()
    
    print(f"✅ Sucesso! A decisão '{titulo}' foi registrada no Decision Ledger.")

# Testando a criação da nossa primeira decisão real:
adicionar_decisao(
    titulo="Definição do Banco de Dados do MVP",
    decisao_tomada="Utilizar SQLite",
    descricao="Optamos pelo SQLite por ser nativo do Python e ideal para validar o MVP do Decision Ledger.",
    responsavel="CEO e Dev Fundadora"
)
import sqlite3

# Conecta ao banco de dados (se não existir, ele cria o arquivo automaticamente)
conexao = sqlite3.connect('cerandolia.db')
cursor = conexao.cursor()

# Criando a tabela para o Decision Ledger conforme o seu projeto [cite: 162]
cursor.execute('''
CREATE TABLE IF NOT EXISTS decisoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,          -- [cite: 163]
    decisao_tomada TEXT NOT NULL,  -- [cite: 164]
    descricao TEXT,                -- [cite: 165]
    responsavel TEXT NOT NULL,     -- [cite: 166]
    data TEXT NOT NULL,            -- [cite: 167]
    versao INTEGER DEFAULT 1       -- [cite: 168]
)
''')

# Salva as alterações e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados e tabela 'decisoes' criados com sucesso!")
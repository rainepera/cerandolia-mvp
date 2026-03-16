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

import sqlite3

conexao = sqlite3.connect('cerandolia.db')
cursor = conexao.cursor()

# Criando a tabela para o Knowledge Hub
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pastas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        icone TEXT DEFAULT 'folder',
        data_criacao TEXT
    )
''')

# Vamos inserir duas pastas de exemplo para o seu layout não começar vazio
cursor.execute("INSERT INTO pastas (nome, data_criacao) VALUES ('Estratégia MVP', '12/03/2026')")
cursor.execute("INSERT INTO pastas (nome, data_criacao) VALUES ('Identidade Visual', '12/03/2026')")

conexao.commit()
conexao.close()
print("Tabela de pastas criada com sucesso!")

import sqlite3

conexao = sqlite3.connect('cerandolia.db')
cursor = conexao.cursor()

# Tabela de Arquivos (Knowledge Hub)
# O campo 'id_pasta' é o que liga o arquivo à pasta específica!
cursor.execute('''
    CREATE TABLE IF NOT EXISTS arquivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pasta INTEGER, 
        nome_arquivo TEXT NOT NULL,
        tipo TEXT,
        link_download TEXT,
        data_upload TEXT,
        FOREIGN KEY (id_pasta) REFERENCES pastas (id)
    )
''')

conexao.commit()
conexao.close()
print("Tabela de arquivos pronta para receber documentos!")
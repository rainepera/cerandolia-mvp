from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- 1. ROTA PRINCIPAL (A TELA INICIAL E A BUSCA) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    # Se o usuário está criando uma nova decisão (POST)
    if request.method == 'POST':
        titulo = request.form['titulo']
        decisao_tomada = request.form['decisao_tomada']
        responsavel = request.form['responsavel']
        data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")

        conexao = sqlite3.connect('cerandolia.db')
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO decisoes (titulo, decisao_tomada, responsavel, data, versao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, decisao_tomada, responsavel, data_atual, 1))
        conexao.commit()
        conexao.close()
        return redirect(url_for('home'))

    # Se o usuário está só abrindo a página ou fazendo uma pesquisa (GET)
    termo_busca = request.args.get('busca')
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    if termo_busca:
        # Puxa os resultados filtrados pela barra de busca
        cursor.execute('''
            SELECT * FROM decisoes 
            WHERE titulo LIKE ? OR decisao_tomada LIKE ? OR responsavel LIKE ?
            ORDER BY id DESC
        ''', (f'%{termo_busca}%', f'%{termo_busca}%', f'%{termo_busca}%'))
    else:
        # Puxa tudo normalmente
        cursor.execute("SELECT * FROM decisoes ORDER BY id DESC")
        
    decisoes = cursor.fetchall()
    conexao.close()

    # Calcula as métricas
    total_decisoes = len(decisoes)
    ultima_decisao = decisoes[0] if total_decisoes > 0 else None 

    return render_template('index.html', decisoes=decisoes, total_decisoes=total_decisoes, ultima_decisao=ultima_decisao)


# --- 2. ROTA PARA ATUALIZAR A VERSÃO ---
@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar(id):
    nova_decisao = request.form['nova_decisao']
    data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")

    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()
    
    # Descobre qual é a versão atual para poder somar +1
    cursor.execute("SELECT versao FROM decisoes WHERE id = ?", (id,))
    versao_atual = cursor.fetchone()[0]
    nova_versao = versao_atual + 1

    # Atualiza a decisão
    cursor.execute('''
        UPDATE decisoes 
        SET decisao_tomada = ?, data = ?, versao = ? 
        WHERE id = ?
    ''', (nova_decisao, data_atual, nova_versao, id))
    
    conexao.commit()
    conexao.close()
    return redirect(url_for('home'))


# --- 3. ROTA PARA DELETAR UMA DECISÃO ---
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM decisoes WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for('home'))

@app.route('/knowledge-hub', methods=['GET', 'POST'])
def knowledge_hub():
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    # Se estiver criando uma pasta nova
    if request.method == 'POST':
        nome_pasta = request.form['nome_pasta']
        data_atual = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("INSERT INTO pastas (nome, data_criacao) VALUES (?, ?)", (nome_pasta, data_atual))
        conexao.commit()
        return redirect(url_for('knowledge_hub'))

    # --- LÓGICA DE BUSCA DE PASTAS ---
    termo = request.args.get('busca_pasta')
    
    if termo:
        # Busca pastas que contenham o termo digitado
        cursor.execute("SELECT * FROM pastas WHERE nome LIKE ?", (f'%{termo}%',))
    else:
        # Se não tiver busca, mostra todas as pastas
        cursor.execute("SELECT * FROM pastas")
                
    pastas = cursor.fetchall()
    conexao.close()
    return render_template('knowledge_hub.html', pastas=pastas)

# --- PÁGINA INTERNA DA PASTA (COM MODO KANBAN) ---
@app.route('/pasta/<int:id_pasta>', methods=['GET', 'POST'])
def abrir_pasta(id_pasta):
    # Pega o modo da URL. Se não tiver nada, o padrão é 'lista'
    modo = request.args.get('modo', 'lista') 
    
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = request.form['nome_arquivo']
        tipo = request.form['tipo']
        data = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("INSERT INTO arquivos (id_pasta, nome_arquivo, tipo, data_upload, status) VALUES (?, ?, ?, ?, ?)", 
                       (id_pasta, nome, tipo, data, 'Pendências'))
        conexao.commit()

    cursor.execute("SELECT nome FROM pastas WHERE id = ?", (id_pasta,))
    nome_pasta = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM arquivos WHERE id_pasta = ?", (id_pasta,))
    arquivos = cursor.fetchall()
    conexao.close()
    
    return render_template('pasta.html', nome_pasta=nome_pasta, arquivos=arquivos, id_pasta=id_pasta, modo=modo)

# --- ROTA PARA MOVER O ARQUIVO NO KANBAN ---
@app.route('/mover-arquivo/<int:id_arquivo>/<int:id_pasta>', methods=['POST'])
def mover_arquivo(id_arquivo, id_pasta):
    novo_status = request.form['novo_status']
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()
    cursor.execute("UPDATE arquivos SET status = ? WHERE id = ?", (novo_status, id_arquivo))
    conexao.commit()
    conexao.close()
    # Volta para a pasta mantendo o modo kanban aberto
    return redirect(url_for('abrir_pasta', id_pasta=id_pasta, modo='kanban'))

# --- ROTA PARA DELETAR UMA PASTA ---
@app.route('/deletar-pasta/<int:id>', methods=['POST'])
def deletar_pasta(id):
    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()
    
    # 1. Primeiro, deletamos todos os arquivos que pertencem a essa pasta
    cursor.execute("DELETE FROM arquivos WHERE id_pasta = ?", (id,))
    
    # 2. Depois, deletamos a pasta em si
    cursor.execute("DELETE FROM pastas WHERE id = ?", (id,))
    
    conexao.commit()
    conexao.close()
    return redirect(url_for('knowledge_hub'))

# --- COLOCA O SERVIDOR NO AR ---
if __name__ == '__main__':
    app.run(debug=True)
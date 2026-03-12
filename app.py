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


# --- COLOCA O SERVIDOR NO AR ---
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- ROTA PRINCIPAL (A TELA INICIAL) ---
@app.route('/', methods=['GET', 'POST'])
def home():
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

    # --- NOVA LÓGICA DE BUSCA ---
    # Verifica se o usuário digitou algo na nova barra de pesquisa
    termo_busca = request.args.get('busca')

    conexao = sqlite3.connect('cerandolia.db')
    cursor = conexao.cursor()

    if termo_busca:
        # Se tem busca, o SQL procura a palavra em qualquer um dos campos usando o LIKE
        cursor.execute('''
            SELECT * FROM decisoes 
            WHERE titulo LIKE ? OR decisao_tomada LIKE ? OR responsavel LIKE ?
            ORDER BY id DESC
        ''', (f'%{termo_busca}%', f'%{termo_busca}%', f'%{termo_busca}%'))
    else:
        # Se não tem busca, mostra tudo normal
        cursor.execute("SELECT * FROM decisoes ORDER BY id DESC")
        
    decisoes = cursor.fetchall()
    conexao.close()

    total_decisoes = len(decisoes)
    ultima_decisao = decisoes[0] if total_decisoes > 0 else None 

    return render_template('index.html', decisoes=decisoes, total_decisoes=total_decisoes, ultima_decisao=ultima_decisao)


# --- ROTA PARA DELETAR UMA DECISÃO ---
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
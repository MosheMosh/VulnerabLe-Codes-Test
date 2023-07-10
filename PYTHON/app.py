import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'db'

mysql = MySQL(app)

# Rota para a criação de tickets
@app.route('/criar_ticket', methods=['GET', 'POST'])
def criar_ticket():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        impacto = request.form.get('impacto')
        data = request.form.get('data')
        origem = request.form.get('origem')
        atribuicao = request.form.get('atribuicao')
        
        # Lógica para criar o ticket com os dados recebidos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tickets (titulo, descricao, impacto, data, origem, atribuicao) VALUES (%s, %s, %s, %s, %s, %s)", (titulo, descricao, impacto, data, origem, atribuicao))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('casos'))
    else:
        return render_template('criar_ticket.html')

@app.route('/remover_caso/<int:caso_id>', methods=['POST'])
def remover_caso(caso_id):
    # Lógica para remover o caso do banco de dados
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tickets WHERE id = %s", (caso_id,))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('casos'))

# Rota para exibir a lista de casos/tickets
@app.route('/casos')
def casos():
    # Lógica para obter a lista de casos/tickets do banco de dados
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tickets")
    resultados = cur.fetchall()
    cur.close()
    
    casos = []
    for resultado in resultados:
        caso = {
            'id': resultado[0],
            'titulo': resultado[1],
            'descricao': resultado[2],
            'impacto': resultado[3],
            'data': resultado[4],
            'origem': resultado[5],
            'atribuicao': resultado[6]
        }
        casos.append(caso)
    
    return render_template('casos.html', casos=casos)

if __name__ == '__main__':
    app.run(debug=True)

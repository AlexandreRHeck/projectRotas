from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import mysql.connector

app = Flask(__name__)

# Configurações do MySQL
MYSQL_DATABASE_HOST = '109.106.251.132'
MYSQL_DATABASE_USER = 'techeckc_heck'
MYSQL_DATABASE_PASSWORD = '123456789'
MYSQL_DATABASE_DB = 'techeckc_askcar'


def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        password=MYSQL_DATABASE_PASSWORD,
        database=MYSQL_DATABASE_DB
    )


"""# Configurações do MySQL
app.config['MYSQL_DATABASE_HOST'] = '109.106.251.132'
app.config['MYSQL_DATABASE_USER'] = 'techeckc_heck'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456789'
app.config['MYSQL_DATABASE_DB'] = 'techeckc_askcar'

# Conectar ao MySQL
mysql = mysql.connector.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    database=app.config['MYSQL_DATABASE_DB']
)
"""

# Substitua pela sua chave de API do Google Maps
API_KEY = 'AIzaSyCEZdV-QYB5ddQfO1I4-7ciI9yAlB3nX3A'


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, endereco FROM enderecos WHERE status = 'on'")
    enderecos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', enderecos=enderecos)


@app.route('/add', methods=['POST'])
def add_address():
    conn = get_db_connection()  # Obter a conexão com o banco de dados
    cursor = conn.cursor()  # Criar um cursor a partir dessa conexão
    cursor.execute("INSERT INTO enderecos (endereco) VALUES (%s)", (request.form['endereco'],))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_address(id):
    conn = get_db_connection()  # Obter a conexão com o banco de dados
    cursor = conn.cursor()  # Criar um cursor a partir dessa conexão
    cursor.execute("DELETE FROM enderecos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit_address(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enderecos WHERE id = %s", (id,))
    endereco = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_endereco.html', endereco=endereco)


@app.route('/update/<int:id>', methods=['POST'])
def update_address(id):
    conn = get_db_connection()  # Obter a conexão com o banco de dados
    cursor = conn.cursor()  # Criar um cursor a partir dessa conexão
    cursor.execute("UPDATE enderecos SET endereco = %s WHERE id = %s", (request.form['endereco'], id))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/enderecos')
def enderecos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, endereco, status FROM enderecos")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('enderecos.html', enderecos=data)


@app.route('/atualizar_status', methods=['POST'])
def atualizar_status():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM enderecos")
    todos_ids = [row[0] for row in cursor.fetchall()]

    for id in todos_ids:
        status = 'on' if request.form.get(f'endereco_{id}') else 'off'
        cursor.execute("UPDATE enderecos SET status = %s WHERE id = %s", (status, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('enderecos'))


@app.route('/add_endereco', methods=['POST'])
def add_endereco():
    nome = request.form['nome']
    endereco = request.form['endereco']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO enderecos (nome, endereco, status) VALUES (%s, %s, 'on')", (nome, endereco))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('enderecos'))


@app.route('/atualizar_enderecos', methods=['POST'])
def atualizar_enderecos():
    conn = get_db_connection()
    cursor = conn.cursor()

    enderecos_selecionados = request.form.getlist('enderecos_selecionados')
    action = request.form['action']

    if action == 'Deletar Selecionados':
        for id in enderecos_selecionados:
            cursor.execute("DELETE FROM enderecos WHERE id = %s", (id,))
    elif action == 'Atualizar Status':
        for id in enderecos_selecionados:
            cursor.execute("UPDATE enderecos SET status = IF(status='on', 'off', 'on') WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('enderecos'))


def geocodificar(endereco):
    geocoding_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={API_KEY}'
    response = requests.get(geocoding_url)
    if response.status_code == 200:
        resultado = response.json()
        if resultado['status'] == 'OK':
            localizacao = resultado['results'][0]['geometry']['location']
            return f"{localizacao['lat']},{localizacao['lng']}"
    return ''


def criar_link_mapas(pontos):
    pontos = [p for p in pontos if p]  # Remove strings vazias
    if len(pontos) < 2:
        return "Número insuficiente de pontos para criar uma rota."
    base_url = "https://www.google.com/maps/dir/"
    pontos_intermediarios = '/'.join(pontos[1:-1]) if len(pontos) > 2 else ''
    return base_url + pontos[0] + '/' + pontos_intermediarios + '/' + pontos[-1]


@app.route('/buscar_rota', methods=['POST'])
def buscar_rota():
    conn = get_db_connection()
    cursor = conn.cursor()

    enderecos_selecionados = request.form.getlist('enderecos_selecionados')
    for endereco in enderecos_selecionados:
        cursor.execute("UPDATE enderecos SET status = 'off' WHERE endereco = %s", (endereco,))

    coordenadas = [geocodificar(endereco) for endereco in enderecos_selecionados if endereco]
    link = criar_link_mapas(coordenadas)

    conn.commit()
    cursor.close()
    conn.close()

    return render_template('rota.html', link=link)


if __name__ == '__main__':
    app.run(debug=True)

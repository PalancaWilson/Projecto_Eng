from flask import Flask, jsonify, request
from flask_cors import CORS
from db_config import conectar

app = Flask(__name__)
CORS(app)  # Permite conexões do frontend


@app.route('/')
def home():
    return jsonify({"mensagem": "API ISPSECURITY ativa!"})


@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM usuarios WHERE email=%s AND senha=%s AND tipo=%s"
    cursor.execute(query, (email, senha, tipo))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return jsonify({"status": "sucesso", "usuario": usuario})
    else:
        return jsonify({"status": "erro", "mensagem": "Credenciais inválidas."}), 401


if __name__ == '__main__':
    app.run(debug=True)

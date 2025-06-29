
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from db_config import conexao

app = Flask(__name__)
CORS(app)  # Aplica CORS global

@app.route('/')
def home():
    return jsonify({"mensagem": "API ISPSECURITY ativa!"})


@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()  # <- CORS especificamente na rota
def login():
    if request.method == 'OPTIONS':
        return '', 204  # resposta ao preflight

    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')
    tipo = dados.get('tipo')

    conn = conexao()
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

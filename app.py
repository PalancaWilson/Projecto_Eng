
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from db_config import conectar

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True) # Aplica CORS global


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

    conn =conectar()
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

@app.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo():
    dados = request.get_json()
    matricula = dados.get('matricula')
    proprietario = dados.get('proprietario')
    tipo_usuario = dados.get('tipo_usuario')
    validade = dados.get('validade')

    if not all([matricula, proprietario, tipo_usuario, validade]):
        return jsonify({"status": "erro", "mensagem": "Todos os campos são obrigatórios"}), 400

    conn = conectar()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO veiculos (matricula, proprietario, tipo_usuario, validade)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (matricula, proprietario, tipo_usuario, validade))
        conn.commit()
        return jsonify({"status": "sucesso", "mensagem": "Veículo cadastrado com sucesso!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)

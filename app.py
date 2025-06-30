
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

    query = "SELECT * FROM funcionarios WHERE email=%s AND senha=%s AND cargo=%s"
   
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


@app.route('/dashboard-data', methods=['GET'])
def dashboard_data():
    conn = conectar()
    cursor = conn.cursor()

    # Total de veículos cadastrados
    cursor.execute("SELECT COUNT(*) FROM veiculos_cadastrado")
    total_veiculos = cursor.fetchone()[0]

    # Total de acessos recusados
    cursor.execute("SELECT COUNT(*) FROM acessos WHERE estado = 'Recusado'")
    recusados = cursor.fetchone()[0]

    # Acessos do dia atual
    cursor.execute("SELECT COUNT(*) FROM acessos WHERE DATE(data_acesso) = CURDATE()")
    acessos_dia = cursor.fetchone()[0]

    # Acessos pendentes (se quiser usar estado NULL ou outro critério)
    cursor.execute("SELECT COUNT(*) FROM acessos WHERE estado IS NULL OR estado = ''")
    pendentes = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "total_veiculos": total_veiculos,
        "recusados": recusados,
        "acessos_dia": acessos_dia,
        "pendentes": pendentes
    })


if __name__ == '__main__':
    app.run(debug=True)






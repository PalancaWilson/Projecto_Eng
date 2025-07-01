
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from db_config import conectar

import os
from werkzeug.utils import secure_filename

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
    cursor.execute("SELECT COUNT(*) FROM veiculos_cadastrado WHERE estado IS NULL OR estado = 'Inativo'")
    pendentes = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "total_veiculos": total_veiculos,
        "recusados": recusados,
        "acessos_dia": acessos_dia,
        "pendentes": pendentes
    })


@app.route("/frequentadores", methods=["GET"])
def listar_frequentadores():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_frequentador, nome, tipo FROM frequentadores")
    frequentadores = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(frequentadores)


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo():
    matricula = request.formVeiculo.get('matricula')
    proprietario = request.formVeiculo.get('proprietario')
    tipo_usuario = request.formVeiculo.get('tipo_usuario')
    marca = request.formVeiculo.get('marca')
    modelo = request.formVeiculo.get('modelo')
    estado = request.formVeiculo.get('estado', 'Ativo')
    cadastrado_por = 1  # Simulando usuário logado
    imagem = request.files.get('imagem')
    
    if not all([matricula, proprietario, tipo_usuario]):
        return jsonify({"status": "erro", "mensagem": "Erro ao cadastrar. Tente novamente."}), 400

    # Salvar a imagem se existir
    nome_arquivo = None
    if imagem:
        nome_seguro = secure_filename(imagem.filename)
        caminho = os.path.join(UPLOAD_FOLDER, nome_seguro)
        imagem.save(caminho)
        nome_arquivo = nome_seguro

    conn = conectar()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO veiculos_cadastrado 
            (matricula, proprietario, tipo_usuario, marca, modelo, estado, imagem, cadastrado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            matricula, proprietario, tipo_usuario,
            marca, modelo, estado, nome_arquivo, cadastrado_por
        ))
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





